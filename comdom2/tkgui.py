#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Tue Nov  1 23:02:39 2016.

@author: lashkov

"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askyesno
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askinteger
from tkinter.simpledialog import askstring

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from .joke import joke
from .mainapp import App, XLSWImportError, XLWTImportError, BadExtError, NoDataFor1stDom, NoDataFor2ndDom, \
    DataNotObserved


class TkGui(tk.Tk):
    """GUI"""

    def __init__(self, namespace):
        super().__init__()
        self.title('ComDom 2')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.close_win)
        self.menu()
        fra1 = ttk.Frame(self)
        fra1.grid(row=0, rowspan=2, column=0)
        lab1 = ttk.LabelFrame(fra1, text='The first domain', labelanchor='n', borderwidth=5)
        lab1.grid(row=0, column=0, pady=5, padx=5)
        but1 = ttk.Button(lab1, text='Add a range', command=self.seg1)
        but1.grid(row=0, column=0, padx=10)
        but12 = ttk.Button(lab1, text='Reset', command=self.sbros_1)
        but12.grid(row=0, column=1, padx=10)
        fra11 = ttk.Frame(fra1)
        fra11.grid(row=1, column=0, pady=10, padx=10)
        self.tx1 = tk.Text(fra11, width=30, height=5)
        scr1 = ttk.Scrollbar(fra11, command=self.tx1.yview)
        self.tx1.configure(yscrollcommand=scr1.set, state='disabled')
        self.tx1.pack(side=tk.LEFT)
        self.tx1.bind('<Enter>', lambda e: self._bound_to_mousewheel(e, self.tx1))
        self.tx1.bind('<Leave>', self._unbound_to_mousewheel)
        scr1.pack(side=tk.RIGHT, fill=tk.Y)
        lab2 = ttk.LabelFrame(fra1, text='The second domain', labelanchor='n', borderwidth=5)
        lab2.grid(row=2, column=0, pady=5, padx=5)
        but2 = ttk.Button(lab2, text='Add a range', command=self.seg2)
        but2.grid(row=0, column=0, padx=10)
        but22 = ttk.Button(lab2, text='Reset', command=self.sbros_2)
        but22.grid(row=0, column=1, padx=10)
        fra12 = ttk.Frame(fra1)
        fra12.grid(row=3, column=0, pady=10, padx=10)
        self.tx2 = tk.Text(fra12, width=30, height=5)
        scr2 = ttk.Scrollbar(fra12, command=self.tx2.yview)
        self.tx2.configure(yscrollcommand=scr2.set, state='disabled')
        self.tx2.pack(side=tk.LEFT)
        self.tx2.bind('<Enter>', lambda e: self._bound_to_mousewheel(e, self.tx2))
        self.tx2.bind('<Leave>', self._unbound_to_mousewheel)
        scr2.pack(side=tk.RIGHT, fill=tk.Y)
        lab3 = ttk.Label(fra1, text='Progress:')
        lab3.grid(row=4, column=0, columnspan=4, pady=5)
        s = ttk.Style()
        s.configure('My.TButton', font=('Helvetica', 10), foreground='red')
        but3 = ttk.Button(fra1, text='Stop!', style='My.TButton', command=self.stop)
        but3.grid(row=6, column=0, columnspan=2, pady=10)
        self.pb = ttk.Progressbar(fra1, orient='horizontal', mode='determinate', length=240)
        self.pb.grid(row=5, column=0, columnspan=2)
        self.fra2 = ttk.Frame(self, width=660, height=515)
        self.fra2.grid(row=0, column=1)
        fra3 = ttk.Frame(self)
        fra3.grid(row=1, column=1, pady=10)
        self.tx = tk.Text(fra3, width=80, height=5)
        scr = ttk.Scrollbar(fra3, command=self.tx.yview)
        self.tx.configure(yscrollcommand=scr.set, state='disabled')
        self.tx.pack(side=tk.LEFT)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        self.tx.bind('<Enter>', lambda e: self._bound_to_mousewheel(e, self.tx))
        self.tx.bind('<Leave>', self._unbound_to_mousewheel)
        self.stop_flag = False
        self.run_flag = False
        self.fig = None
        self.canvas = None
        self.toolbar = None
        self.grid = False
        self.legend = False
        self.smoth = False
        self.all_res = True
        if namespace.input:
            self.open_pdb(namespace.input)
        showinfo(';-)', joke())
        self.app = App()

    def _bound_to_mousewheel(self, event, tx):
        self.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, tx))
        self.bind_all('<Button-4>', lambda e: self._on_mousewheel(e, tx))
        self.bind_all('<Button-5>', lambda e: self._on_mousewheel(e, tx))
        self.bind_all('<Up>', lambda e: self._on_mousewheel(e, tx))
        self.bind_all('<Down>', lambda e: self._on_mousewheel(e, tx))

    def _unbound_to_mousewheel(self, event):
        self.unbind_all("<MouseWheel>")
        self.unbind_all('<Button-4>')
        self.unbind_all('<Button-5>')
        self.unbind_all('<Up>')
        self.unbind_all('<Down>')

    @staticmethod
    def _on_mousewheel(event, tx):
        if event.num == 4 or event.keysym == 'Up':
            tx.yview_scroll(-1, "units")
        elif event.num == 5 or event.keysym == 'Down':
            tx.yview_scroll(1, "units")
        else:
            tx.yview_scroll(int(-1 * (event.delta / 120)), "units")

    @staticmethod
    def about():
        """

        """
        showinfo('About',
                 'The dependence of the distance between the centers of mass of protein domains on the time of MD')

    def menu(self):
        """Method of initialize menu"""
        m = tk.Menu(self)  # creates a Menu object for main window
        self.config(menu=m)  # the window is configured with the menu for it
        fm = tk.Menu(m)  # creates a menu item with the placement on the main menu (m)
        # item is located on the main menu (m)
        m.add_cascade(label='File', menu=fm)
        # a list of commands of a menu item
        fm.add_command(label='Open PDB', command=self.open_pdb)
        fm.add_command(label='Save plot', command=self.save_graph)
        fm.add_command(label='Save as...', command=self.save_data)
        fm.add_command(label='Save LOG', command=self.save_log)
        fm.add_command(label='Quit', command=self.close_win)
        rm = tk.Menu(m)  # creates a menu item with the placement on the main menu (m)
        # item is located on the main menu (m)
        m.add_cascade(label='Run', menu=rm)
        rm.add_command(label='All residues', command=self.run)
        rm.add_command(label='Only hydrophobic residues', command=self.trj_cycle_hf)
        om = tk.Menu(m)  # creates a menu item with the placement on the main menu (m)
        # item is located on the main menu (m)
        m.add_cascade(label='Options', menu=om)
        om.add_command(label='Plot grid', command=self.grid_set)
        om.add_command(label='Plot legend', command=self.legend_set)
        om.add_command(label='Smoothing', command=self.smoth_set)
        om.add_command(label='Statistics', command=self.xvg_stat)
        om.add_command(label='Clustering', command=self.cluster_an)
        m.add_command(label='About', command=self.about)

    def close_win(self):
        """Self-destruct with a question"""
        if askyesno('Quit', 'Are your sure?'):
            self.destroy()

    def xvg_stat(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        try:
            r_min, r_max, r_mean, t_min, t_max, std, perc_25, median, perc_75 = self.app.stat()
        except NameError:
            showerror('Error!', 'Data unavailable')
            return
        except ValueError:
            showerror('Error', 'Statistics unavailable')
            return
        showinfo('Statistics', 'The minimum distance between domains = {0:.3f} \u212b (t= {1:.2f} пc)\n'
                               'The maximum distance between domains = {2:.3f} \u212b (t= {3:.2f} пc)\n'
                               'The average distance between domains = {4:.3f} \u212b\n'
                               'The standard deviation = {5:.3f} \u212b\n'
                               'Quartiles: (25%) = {6:.3f} \u212b, (50%) = {7:.3f} \u212b, '
                               '(75%) = {8:.3f} \u212b'.format(
            r_min, t_min, r_max, t_max, r_mean, std, perc_25, median, perc_75))
        self.tx.configure(state='normal')
        self.tx.insert(tk.END, 'The minimum distance between domains = {0:.3f} \u212b (t= {1:.2f} пc)\n'
                               'The maximum distance between domains = {2:.3f} \u212b (t= {3:.2f} пc)\n'
                               'The average distance between domains= {4:.3f} \u212b\n'
                               'The standard deviation= {5:.3f} \u212b\n'
                               'Quartiles: (25%) = {6:.3f} \u212b, (50%) = {7:.3f} \u212b, '
                               '(75%) = {8:.3f} \u212b'.format(
            r_min, t_min, r_max, t_max, r_mean, std, perc_25, median, perc_75))
        self.tx.configure(state='disabled')

    def cluster_an(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        n_cluster = askinteger('Number of clusters', 'Enter the number of clusters (0-auto, MeanShift)')
        while n_cluster is None:
            n_cluster = askinteger('Number of clusters', 'Enter the number of clusters (0-auto, MeanShift)')
        try:
            xhist, yhist, si_score, std_dev = self.app.cluster(n_cluster)
        except ImportError:
            showerror('Error!', 'Scikit-learn is not installed!')
            return
        except (NameError, ValueError):
            showerror('Error!', 'Data unavailable')
            return
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title('Clustering')
        ax.set_ylabel(r'$\% \ \tau$')
        ax.set_xlabel(r'$\xi,\ \AA$')
        ax.grid(self.grid)
        ax.bar(xhist.flatten(), yhist, width=[3 * x for x in std_dev], align='center')
        win_cls = tk.Toplevel(self)
        win_cls.title("Clustering {:s}".format('MeanShift' if n_cluster == 0 else 'KMeans'))
        win_cls.minsize(width=640, height=600)
        win_cls.resizable(False, False)
        fra4 = ttk.Frame(win_cls)
        fra4.grid(row=0, column=0)
        canvas = FigureCanvasTkAgg(fig, master=fra4)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, fra4)
        toolbar.update()
        canvas._tkcanvas.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
        fra5 = ttk.Frame(win_cls)
        fra5.grid(row=1, column=0)
        tx = tk.Text(fra5, width=85, height=10)
        scr = ttk.Scrollbar(fra5, command=self.tx.yview)
        tx.configure(yscrollcommand=scr.set)
        tx.pack(side=tk.LEFT)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        tx.configure(state='normal')
        tx.insert(tk.END, 'The number of clusters = {0:d}\nSilhouette Coefficient = {1:.2f}\n'
                          '(The best value is 1 and the worst value is -1.\n'
                          'Values near 0 indicate overlapping clusters.\n'
                          'Negative values generally indicate that a sample has been assigned\n'
                          'to the wrong cluster, as a different cluster is more similar.'
                          ')\nClusters:'.format(len(xhist), si_score))
        for n, cls_center in enumerate(xhist.flatten()):
            tx.insert(tk.END,
                      '\nCluster No {0:d}: points of the trajectory {1:.1f} %,'
                      ' position of the centroid - {2:.3f} \u212b, '
                      'RMS = {3:.3f} \u212b'.format(n + 1, yhist[n], cls_center, std_dev[n]))
        self.tx.configure(state='disabled')

    def save_data(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        opt = {'parent': self, 'filetypes': [('DAT', '.dat'), ('Microsoft Excel 97-2003 (xls)', '.xls'),
                                             ('Microsoft Excel 2007+ (xslx)', '.xslx')],
               'initialfile': 'summary_distances.dat', 'title': 'Save as...'}
        sa = asksaveasfilename(**opt)
        try:
            self.app.save(sa)
        except OSError:
            showerror('Error!', 'Failed to save {0:s}'.format(sa))
            return
        except (NameError, ValueError):
            showerror('Error!', 'Data unavailable')
            return
        except XLSWImportError:
            showerror('Error!', 'xlsxwriter is not installed! Saving in Microsoft Excel 2007+ impossible!')
            return
        except XLWTImportError:
            showerror('Error!', 'xlwt is not installed! Saving in Microsoft Excel 97-2003 impossible!')
            return
        except BadExtError:
            showerror('Error!', 'Unsupported file format!')
            return

    def save_log(self):
        """

        """
        opt = {'parent': self, 'filetypes': [('LOG', '.log'), ], 'initialfile': 'myfile.log', 'title': 'Save LOG'}
        sa = asksaveasfilename(**opt)
        if sa:
            letter = self.tx.get(1.0, tk.END)
            try:
                with open(sa, 'w') as f:
                    f.write(letter)
            except FileNotFoundError:
                pass

    def save_graph(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        if self.fig is None:
            showerror('Error!', 'Plot unavailable!')
            return
        opt = {'parent': self, 'filetypes': [('All supported formats', (
               '.eps', '.jpeg', '.jpg', '.pdf', '.pgf', '.png', '.ps', '.raw', '.rgba', '.svg', '.svgz', '.tif',
               '.tiff')), ], 'initialfile': 'myfile.png', 'title': 'Save plot'}
        sa = asksaveasfilename(**opt)
        if sa:
            try:
                self.fig.savefig(sa, dpi=600)
            except FileNotFoundError:
                return
            except AttributeError:
                showerror('Error!', 'Plot unavailable!')
            except ValueError:
                showerror('Unsupported file format of the picture!',
                          'Supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff.')

    def grid_set(self):
        """

        :return:
        """
        self.grid = bool(askyesno('Plot grid', 'Display?'))
        if self.run_flag:
            return
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass
        try:
            self._graph()
        except AttributeError:
            pass

    def legend_set(self):
        """

        :return:
        """
        self.legend = bool(askyesno('Plot legend', 'Display?'))
        if self.run_flag:
            return
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass
        try:
            self._graph()
        except AttributeError:
            pass

    def smoth_set(self):
        """

        :return:
        """
        self.smoth = bool(askyesno('Smoothing according to Savitsky-Golay', 'Display?'))
        if self.app.nparray is None:
            return
        if self.run_flag:
            return
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass
        try:
            self._graph()
        except AttributeError:
            pass

    def _graph(self):
        self.fig = None
        self.fig = Figure()
        ax = self.fig.add_subplot(111)
        x, y, ysg = self.app.getgraphdata()
        ax.set_title('COM distance vs. time')
        ax.set_ylabel(r'$\xi,\ \AA$')
        if (max(x) - min(x)) > 10000:
            ax.set_xlabel(r'$Time,\ ns$')
            x /= 1000
        else:
            ax.set_xlabel(r'$Time,\ ps$')
        ax.plot(x, y, color='black', label='Raw COM distance')
        if self.smoth:
            if len(ysg) == len(x):
                ax.plot(x, ysg, 'r', label='Filtered COM distance')
            else:
                showerror('Error!', 'It is not possible to perform smoothing!')
                self.smoth = False
        ax.grid(self.grid)
        if self.legend:
            ax.legend(loc='best', frameon=False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.fra2)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.fra2)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, side=tk.TOP, expand=1)

    def open_pdb(self, input_pdb=None):
        """

        :param input_pdb:
        :return:
        """
        if self.run_flag and not self.stop_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        if input_pdb:
            pdb = input_pdb
        else:
            opt = {'filetypes': [('PDB', ('.pdb', '.PDB', '.ent')), ('All files', '.*')]}
            pdb = askopenfilename(**opt)
        if pdb:
            try:
                self.app.open_pdb(pdb)
            except FileNotFoundError:
                return
            else:
                showinfo('Info', 'File was read!')
        else:
            return
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass
        self.tx1.configure(state='normal')
        self.tx1.delete('1.0', tk.END)
        self.tx1.configure(state='disabled')
        self.tx2.configure(state='normal')
        self.tx2.delete('1.0', tk.END)
        self.tx2.configure(state='disabled')
        self.pb['value'] = 0
        self.pb.update()
        self.fig = None
        self.tx.configure(state='normal')
        self.tx.delete('1.0', tk.END)
        self.tx.configure(state='disabled')

    def stop(self):
        """Stop I said!"""
        if self.stop_flag:
            self.run()
        else:
            self.tx.configure(state='disabled')
            self.stop_flag = True

    def seg1(self):
        """Set residues in the first domain"""
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        chain_name_1 = askstring('The first domain', 'Chain name: ')
        if chain_name_1 == '' or chain_name_1 is None:
            chain_name_1 = ' '
        r_num_start_1 = askinteger('The first domain', 'The number of the first residue: ')
        r_num_end_1 = askinteger('The first domain', 'The number of the last residue:: ')
        if (r_num_start_1 is None) or (r_num_end_1 is None):
            return
        if r_num_start_1 > r_num_end_1:
            showerror('Error!', 'The number of the first residue should be no more than the last! ')
            return
        self.tx1.configure(state='normal')
        self.tx1.insert(tk.END, 'Chain {0:s}, residues with {1:>4d} to {2:>4d}\n'.format(chain_name_1, r_num_start_1,
                                                                                         r_num_end_1))
        self.tx1.configure(state='disabled')
        for s_1 in range(r_num_start_1, r_num_end_1 + 1):
            self.app.segment_1.append((chain_name_1, s_1))

    def seg2(self):
        """Set residues in the second domain"""
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        chain_name_2 = askstring('The second domain', 'Chain name: ')
        if chain_name_2 == '' or chain_name_2 is None:
            chain_name_2 = ' '
        r_num_start_2 = askinteger('The second domain', 'The number of the first residue: ')
        r_num_end_2 = askinteger('The second domain', 'The number of the last residue: ')
        if (r_num_start_2 is None) or (r_num_end_2 is None):
            return
        if r_num_start_2 > r_num_end_2:
            showerror('Error!', 'The number of the first residue should be no more than the last! ')
            return
        self.tx2.configure(state='normal')
        self.tx2.insert(tk.END, 'Chain {0:s}, residues with {1:>4d} to {2:>4d}\n'.format(chain_name_2, r_num_start_2,
                                                                                         r_num_end_2))
        self.tx2.configure(state='disabled')
        for s_2 in range(r_num_start_2, r_num_end_2 + 1):
            self.app.segment_2.append((chain_name_2, s_2))

    def sbros_1(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        self.app.segment_1.clear()
        self.tx1.configure(state='normal')
        self.tx1.delete('1.0', tk.END)
        self.tx1.configure(state='disabled')

    def sbros_2(self):
        """

        :return:
        """
        if self.run_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        self.app.segment_2.clear()
        self.tx2.configure(state='normal')
        self.tx2.delete('1.0', tk.END)
        self.tx2.configure(state='disabled')

    def trj_cycle_hf(self):
        """

        """
        self.all_res = False
        showinfo('Attention!', 'Non-standard amino acids and ligands\nwill be accepted as hydrophobic!')
        self.run()

    def run(self):
        """The main algorithm of the program"""
        if self.run_flag and not self.stop_flag:
            showerror('Error!', 'The calculation is still running!')
            return
        if self.app.s_array is None:
            showerror('Error!', 'File was not download!')
            return
        self.run_flag = True
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass
        if not self.stop_flag:
            self.tx.configure(state='normal')
            self.tx.delete('1.0', tk.END)
            self.tx.configure(state='disabled')
            self.pb['maximum'] = len(self.app.s_array)
        else:
            self.stop_flag = False
        try:
            for t, c_mass_1, c_mass_2, r, n in self.app.trj_cycle(self.all_res):
                self.tx.configure(state='normal')
                if t is not None:
                    self.tx.insert(tk.END, 'At t = {0:.3f} {1:s}\n'.format(
                        t if t < 1000 else t / 1000, "ps" if t < 1000 else "ns"))
                self.tx.insert(tk.END, 'Coordinates of the center of mass of the first domain:'
                               'C1 ({0:.3f} \u212b, {1:.3f} \u212b, {2:.3f} \u212b)\n'
                               'the second domain: C2({3: .3f} \u212b, {4: .3f} \u212b, {5: .3f} \u212b\n'
                               'the distance between domains: {6:.3f} \u212b\n').format(
                               c_mass_1[0], c_mass_1[1], c_mass_1[2], c_mass_2[0], c_mass_2[1], c_mass_2[2], r)
                self.tx.configure(state='disabled')
                self.pb['value'] = n
                self.pb.update()
                if self.stop_flag:
                    self.run_flag = False
                    break
        except NoDataFor1stDom:
            showerror('Error!', 'Data for the first domain was not collected!')
            showinfo('Attention!', 'Residues ranges was not cleaned!')
            self.pb['value'] = 0
            self.pb.update()
            self.run_flag = False
            return
        except NoDataFor2ndDom:
            showerror('Error!', 'Data for the second domain was not collected!')
            showinfo('Attention!', 'Residues ranges was not cleaned!')
            self.pb['value'] = 0
            self.pb.update()
            self.run_flag = False
            return
        except DataNotObserved:
            showerror('Error!', 'Data was not collected!')
            showinfo('Attention!', 'Residues ranges was not cleaned!')
            self.pb['value'] = 0
            self.pb.update()
            self.run_flag = False
            return
        if self.app.nparray is not None:
            if self.app.nparray.shape[0] > 2:
                try:
                    self.canvas.get_tk_widget().destroy()
                    self.toolbar.destroy()
                except AttributeError:
                    pass
                self._graph()
        self.all_res = True
        showinfo('Attention!', 'Residues ranges was not cleaned!')
