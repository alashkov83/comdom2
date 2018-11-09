# coding=utf-8
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Tue Nov  1 23:02:39 2016.

@author: lashkov

"""

import os.path
from functools import lru_cache
from math import factorial

import numpy as np
from matplotlib.figure import Figure
from periodictable import formula


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    rate: int
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


class XLSWImportError(ImportError):
    pass


class XLWTImportError(ImportError):
    pass


class BadExtError(FileNotFoundError):
    pass


class NoDataFor1stDom(AttributeError):
    pass


class NoDataFor2ndDom(AttributeError):
    pass


class DataNotObserved(ValueError):
    pass


class SmothPlotError(ValueError):
    pass


class App:
    """Class of program logic"""

    def __init__(self):
        self.segment_1 = []
        self.segment_2 = []
        self.s_array = None
        self.nparray = None
        self.all_res = True

    @staticmethod
    def cmass(str_nparray: np.ndarray) -> list:
        """Calculate the position of the center of mass."""
        center = np.average(str_nparray[:, 0:3], axis=0, weights=str_nparray[:, 3])
        return center

    @staticmethod
    @lru_cache()
    def mass(element: str) -> float:
        """The mass of the atom. Use a dictionary for frequently types of atoms accelerates calculations."""
        elements = {
            ' H': 1.0,
            ' C': 12.0,
            ' N': 14.0,
            ' O': 16.0,
            ' P': 31.0,
            ' S': 32.0,
            ' F': 19.0}
        return elements.get(element, round(formula(element).mass))

    def stat(self):
        """Big lie ie statistics"""
        if self.nparray is None:
            raise ValueError
        t = self.nparray[:, 0]
        r = self.nparray[:, 1]
        r_min = min(r)
        r_max = max(r)
        r_mean = r.mean()
        t_min = t[np.argmin(r)]
        t_max = t[np.argmax(r)]
        std = np.std(r)
        perc_25 = np.percentile(r, 25)
        median = np.percentile(r, 50)
        perc_75 = np.percentile(r, 75)
        return r_min, r_max, r_mean, t_min, t_max, std, perc_25, median, perc_75

    def cluster(self, n_cluster: int, grid: bool=True):
        """

        :param grid:
        :param n_cluster:
        :return:
        """
        # Scikit - learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825 - 2830, 2011.
        from sklearn.cluster import MeanShift
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score, calinski_harabaz_score
        if self.nparray is None:
            raise ValueError
        r = self.nparray[:, 1]
        if n_cluster == 0:
            ap = MeanShift().fit(r.reshape(-1, 1))
        elif n_cluster > 0:
            ap = KMeans(n_cluster).fit(r.reshape(-1, 1))
        else:
            raise ValueError
        yhist = []
        for n in range(len(ap.cluster_centers_)):
            yhist.append(100 * len(list(filter(lambda x: x == n, ap.labels_))) / len(ap.labels_))
        xhist = ap.cluster_centers_
        # The Silhouette Coefficient is calculated using the mean intra-cluster distance
        # (a) and the mean nearest-cluster distance (b) for each sample.
        # The best value is 1 and the worst value is -1.
        # Values near 0 indicate overlapping clusters.
        # Negative values generally indicate that a sample has been assigned
        # to the wrong cluster, as a different cluster is more similar.
        if len(ap.cluster_centers_) > 1:
            si_score = silhouette_score(r.reshape(-1, 1), ap.labels_)
            calinski = calinski_harabaz_score(r.reshape(-1, 1), ap.labels_)
        else:
            si_score = 1.0
            calinski = -1
        zipped = list(zip(r.flatten(), ap.labels_))
        std_dev = []
        for n in range(len(ap.cluster_centers_)):
            std_dev.append(np.std([x[0] for x in zipped if x[1] == n]))
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title('Clustering')
        ax.set_ylabel(r'$\% \ \tau$')
        ax.set_xlabel(r'$\xi,\ \AA$')
        ax.grid(grid)
        ax.bar(xhist.flatten(), yhist, width=[3 * x for x in std_dev], align='center')
        return xhist, yhist, si_score, calinski, std_dev, fig

    def save(self, sa):
        """

        :param sa:
        """
        ext = os.path.splitext(sa)[1][1:].strip().lower()
        if self.nparray is None:
            raise ValueError
        t = self.nparray[:, 0]
        r_a = self.nparray[:, 1]
        if sa:
            if ext == 'dat':
                r_n = r_a / 10
                n_nparray = np.column_stack((t, r_n))
                np.savetxt(sa, n_nparray, delimiter='\t', fmt=['%d', '%.3f'])
            elif ext == 'xslx':
                try:
                    from xlsxwriter import Workbook
                except ImportError:
                    raise XLSWImportError
                wb = Workbook(sa)
                ws = wb.add_worksheet("summary_distances")
                ws.write_row(0, 0, ('Time, ps', 'COM, \u212b'))
                ws.write_column(1, 0, t)
                ws.write_column(1, 1, r_a)
                wb.close()
            elif ext == 'xls':
                try:
                    from xlwt import Workbook as Workbook
                except ImportError:
                    raise XLWTImportError
                wb = Workbook()
                ws = wb.add_sheet("summary_distances")
                ws.write(0, 0, 'Time, ps')
                ws.write(0, 1, 'COM, \u212b')
                for i, t_i in enumerate(t, start=1):
                    ws.write(i, 0, t_i)
                for j, r_a_j in enumerate(r_a, start=1):
                    ws.write(j, 1, r_a_j)
                wb.save(sa)
            else:
                raise BadExtError

    # noinspection PyAugmentAssignment
    def getgraphdata(self, smoth=True, grid=True, legend=True):
        """

        :return:
        """
        x = self.nparray[:, 0]
        y = self.nparray[:, 1]
        ysg = savitzky_golay(y, window_size=31, order=4)
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title('COM distance vs. time')
        ax.set_ylabel(r'$\xi,\ \AA$')
        if (max(x) - min(x)) > 10000:
            ax.set_xlabel(r'$Time,\ ns$')
            x = x / 1000
        else:
            ax.set_xlabel(r'$Time,\ ps$')
        ax.plot(x, y, color='black', label='Raw COM distance')
        if smoth:
            if len(ysg) == len(x):
                ax.plot(x, ysg, 'r', label='Filtered COM distance')
            else:
                raise SmothPlotError
        ax.grid(grid)
        if legend:
            ax.legend(loc='best', frameon=False)
        return fig

    def open_pdb(self, filename):
        """

        :param filename:
        """
        with open(filename) as f:
            self.s_array = f.readlines()
        self.segment_1 = []
        self.segment_2 = []

    def trj_cycle(self, all_res=True):
        """Main program"""
        if self.s_array is None:
            raise ValueError
        t_array = []
        r_array = []
        xyzm_array_1 = []
        xyzm_array_2 = []
        hydrfob = ('ALA', 'VAL', 'PRO', 'LEU', 'ILE', 'PHE', 'MET', 'TRP')
        all_aa = ('ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN',
                  'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR')
        model_flag = False
        for n, s in enumerate(self.s_array):
            if s.find('t=') != -1:
                t = float(s[s.find('t=') + 2:-1])
                t_array.append(t)
            elif s[0:5] == 'MODEL':
                model_flag = True
            elif (s[0:6] == 'ATOM  ') and ((s[21], int(s[22:26])) in self.segment_1) and (
                    (all_res is True) or ((str(s[17:20]) in hydrfob) or (str(s[17:20]) not in all_aa))):
                xyzm_1 = [float(s[30:38]), float(s[38:46]),
                          float(s[46:54]), self.mass(s[76:78])]
                xyzm_array_1 = np.concatenate((xyzm_array_1, xyzm_1))
            elif (s[0:6] == 'ATOM  ') and ((s[21], int(s[22:26])) in self.segment_2) and (
                    (all_res is True) or ((str(s[17:20]) in hydrfob) or (str(s[17:20]) not in all_aa))):
                xyzm_2 = [float(s[30:38]), float(s[38:46]),
                          float(s[46:54]), self.mass(s[76:78])]
                xyzm_array_2 = np.concatenate((xyzm_array_2, xyzm_2))
            elif s[0:6] == 'ENDMDL' or (s[0:3] == 'END' and model_flag is False):
                try:
                    xyzm_array_1.shape = (-1, 4)
                except AttributeError:
                    raise NoDataFor1stDom
                try:
                    xyzm_array_2.shape = (-1, 4)
                except AttributeError:
                    raise NoDataFor2ndDom
                c_mass_1 = self._cmass(xyzm_array_1)
                c_mass_2 = self._cmass(xyzm_array_2)
                r = (((c_mass_1[0] - c_mass_2[0]) ** 2) + ((c_mass_1[1] -
                                                            c_mass_2[1]) ** 2) + ((c_mass_1[2] -
                                                                                   c_mass_2[2]) ** 2)) ** 0.5
                r_array.append(r)
                if len(r_array) > 1:
                    if len(t_array) == 0:
                        t_array = list(range(0, len(r_array)))
                    self.nparray = np.column_stack((t_array, r_array))
                elif len(r_array) == 0:
                    raise DataNotObserved
                if not t_array:
                    t = None
                del xyzm_array_1
                del xyzm_array_2
                xyzm_array_1 = []
                xyzm_array_2 = []
                yield t, c_mass_1, c_mass_2, r, n
