#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Tue Nov  1 23:02:39 2016.

@author: lashkov

"""

import sys
from tkinter.messagebox import showinfo
import matplotlib
import matplotlib.pyplot as plt
from .joke import joke
from .mainapp import App, XLSWImportError, XLWTImportError, BadExtError, NoDataFor1stDom, NoDataFor2ndDom, \
    DataNotObserved

matplotlib.use('Agg')


class Cli:
    """

    """

    def __init__(self, namespace):
        self.app = App()
        self.namespace = namespace
        self.app.open_pdb(self.namespace.input)
        self.add_segment()
        self.run()
        if self.app.nparray is not None:
            if self.app.nparray.shape[0] > 2:
                self.graph()
                self.xvg_stat()
                self.cluster_an()
            self.save_data()
        print(">>>>", joke())

    def add_segment(self):
        """

        """
        if self.namespace.segment1 and self.namespace.segment2:
            print("The first domain:")
            for seg1 in self.namespace.segment1.split('_'):
                seg1 = seg1.strip().split(':')
                try:
                    chain_name_1 = seg1[0]
                    if chain_name_1 == '' or chain_name_1 is None:
                        chain_name_1 = ' '
                    r_num_start_1 = int(seg1[1])
                    r_num_end_1 = int(seg1[2])
                    if r_num_start_1 > r_num_end_1:
                        print('Error! The number of the first residue should be no more than the last!')
                        sys.exit(-1)
                except ValueError:
                    print('Invalid format segment1! Chain:StartNo:EndNo')
                    sys.exit(-1)
                print('Chain {0:s}, residue with {1:d} at {2:d}\n'.format(
                    chain_name_1, r_num_start_1, r_num_end_1))
                for s_1 in range(r_num_start_1, r_num_end_1 + 1):
                    self.app.segment_1.append((chain_name_1, s_1))
            print("The second domain:")
            for seg2 in self.namespace.segment2.split("_"):
                seg2 = seg2.strip().split(':')
                try:
                    chain_name_2 = seg2[0]
                    if chain_name_2 == '' or chain_name_2 is None:
                        chain_name_2 = ' '
                    r_num_start_2 = int(seg2[1])
                    r_num_end_2 = int(seg2[2])
                    if r_num_start_2 > r_num_end_2:
                        print('Error! The number of the first residue should be no more than the last!')
                        sys.exit(-1)
                except ValueError:
                    print('Invalid format segment1! Chain:StartNo:EndNo')
                    sys.exit(-1)
                print('Chain {0:s}, residue with {1:d} at {2:d}\n'.format(
                    chain_name_2, r_num_start_2, r_num_end_2))
                for s_2 in range(r_num_start_2, r_num_end_2 + 1):
                    self.app.segment_2.append((chain_name_2, s_2))
        else:
            print("Segments must be specified!")
            sys.exit(-1)

    def run(self):
        """Main program"""
        try:
            import progressbar2 as progressbar
        except ImportError:
            import progressbar
        hydr = self.namespace.hydrofob
        bar1 = progressbar.ProgressBar(maxval=len(
            self.app.s_array), redirect_stdout=True).start()
        try:
            for t, c_mass_1, c_mass_2, r, n in self.app.trj_cycle(not hydr):
                if t is not None:
                    print('При t = {0:.3f} {1:s}\n'.format(t if t < 1000 else t / 1000, "пс" if t < 1000 else "нс"))
                print(
                    'Coordinates of the center of mass of the first domain: C1 ({0:.3f} \u212b, {1:.3f} \u212b, {2:.3f} \u212b)'.format(
                        c_mass_1[0],
                        c_mass_1[1],
                        c_mass_1[2]) +
                    '\n' +
                    'the second domain: C2 ({0:.3f} \u212b, {1:.3f} \u212b, {2:.3f} \u212b)'.format(
                        c_mass_2[0],
                        c_mass_2[1],
                        c_mass_2[2]) +
                    '\n' +
                    'the distance between domains: {0:.3f} \u212b'.format(r))
                bar1.update(n)
        except NoDataFor1stDom:
            print('Error! Data for the first domain are not collected.')
            sys.exit(-1)
        except NoDataFor2ndDom:
            print('Error! Data for the second domain are not collected.')
            sys.exit(-1)
        except DataNotObserved:
            print('Error! Data are not collected.')
            sys.exit(-1)
        bar1.finish()

    def xvg_stat(self):
        """

        :return:
        """
        try:
            r_min, r_max, r_mean, t_min, t_max, std, perc_25, median, perc_75 = self.app.stat()
        except (ValueError, NameError):
            print('Statistics are not available!')
            return
        print('\nStatistics:\nThe minimum distance between domains = {0:.3f} \u212b (t= {1:.2f} ps)\n'
              'The maximum distance between domains = {2:.3f} \u212b (t= {3:.2f} пc)\n'
              'The average distance between domains= {4:.3f} \u212b\nStandard deviation: {5:.3f} \u212b\n'
              'Quartiles: (25%) = {6:.3f} \u212b, (50%) = {7:.3f} \u212b, (75%) = {8:.3f} \u212b'.format(
            r_min, t_min, r_max, t_max, r_mean, std, perc_25, median, perc_75))

    def cluster_an(self):
        """

        :return:
        """
        n_cluster = self.namespace.n_cluster
        try:
            xhist, yhist, si_score, std_dev = self.app.cluster(n_cluster)
        except ImportError:
            print('Scikit-learn is not installed!')
            return
        except (NameError, ValueError):
            showinfo('Info', 'Data not available for clustering')
            return
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Cluster analysis')
        ax.set_ylabel(r'$\% \ \tau$')
        ax.set_xlabel(r'$\xi,\ \AA$')
        ax.grid(True)
        ax.bar(xhist.flatten(), yhist, width=[3 * x for x in std_dev], align='center')
        print('Clustering:\nThe number of clusters: {0:d}\nSilhouette Coefficient = {1:.2f}\n'
              '(The best value is 1 and the worst value is -1.\n'
              'Values near 0 indicate overlapping clusters.\n'
              'Negative values generally indicate that a sample has been assigned\n'
              'to the wrong cluster, as a different cluster is more similar.)\nКластеры:'.format(len(xhist), si_score))
        for n, cls_center in enumerate(xhist.flatten()):
            print('Cluster No {0:d}: points of the trajectory {1:.1f} %, the position of the centroid - {2:.3f} \u212b, '
                  'RMS = {3:.3f} \u212b'.format(n + 1, yhist[n], cls_center, std_dev[n]))
        if self.namespace.ocluster:
            self.save_graph(fig, self.namespace.ocluster)

    def graph(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('COM distance vs. time')
        ax.set_ylabel(r'$\xi,\ \AA$')
        x, y, ysg = self.app.getgraphdata()
        if (max(x) - min(x)) > 10000:
            ax.set_xlabel(r'$Time,\ ns$')
            x /= 1000
        else:
            ax.set_xlabel(r'$Time,\ ps$')
        ax.plot(x, y, color='black', label='Raw COM distance')
        if len(ysg) == len(x):
            ax.plot(x, ysg, 'r', label='Filtered COM distance')
        else:
            print('Не возможно выполнить сглаживание!')
        ax.grid(True)
        ax.legend(loc='best', frameon=False)
        if self.namespace.ofigure:
            self.save_graph(fig, self.namespace.ofigure)

    def save_data(self):
        """

        :return:
        """
        sa = self.namespace.output
        try:
            self.app.save(sa)
        except OSError:
            print('Не удалось сохранить {0:s}!'.format(sa))
        except (NameError, ValueError):
            print('Данные недоступны!')
        except XLSWImportError:
            print('xlsxwriter не установлен! Сохранение в Microsoft Excel 2007+ невозможно!')
            return
        except XLWTImportError:
            print('xlwt не установлен! Сохранение в Microsoft Excel 97-2003 невозможно!')
        except BadExtError:
            print('Неподдерживаемый формат файла! Поддреживаемые форматы: dat, xsl, xslx')

    @staticmethod
    def save_graph(fig, sa):
        """

        :param fig:
        :param sa:
        :return:
        """
        if fig is None:
            print('График недоступен!\n')
            return
        if sa:
            try:
                plt.savefig(sa, dpi=600)
            except AttributeError:
                print('График недоступен!')
            except ValueError:
                print('Неподдерживаемый формат файла рисунка!\n'
                      'Поддреживаемые форматы: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff.\n')
