#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Tue Nov  1 23:02:39 2016.

@author: lashkov

"""

import sys
from tkinter.messagebox import showinfo

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .joke import joke
from .mainapp import App, XLSWImportError, XLWTImportError, BadExtError, NoDataFor1stDom, NoDataFor2ndDom, \
    DataNotObserved


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
            print("Первый домен:")
            for seg1 in self.namespace.segment1.split('_'):
                seg1 = seg1.strip().split(':')
                try:
                    chain_name_1 = seg1[0]
                    if chain_name_1 == '' or chain_name_1 is None:
                        chain_name_1 = ' '
                    r_num_start_1 = int(seg1[1])
                    r_num_end_1 = int(seg1[2])
                    if r_num_start_1 > r_num_end_1:
                        print('Ошибка! Номер первого а.о. должен быть не больше последнего!')
                        sys.exit(-1)
                except ValueError:
                    print('Неверный формат segment1! Chain:StartNo:EndNo')
                    sys.exit(-1)
                print('Цепь {0:s}, а.о. с {1:d} по {2:d}\n'.format(
                    chain_name_1, r_num_start_1, r_num_end_1))
                for s_1 in range(r_num_start_1, r_num_end_1 + 1):
                    self.app.segment_1.append((chain_name_1, s_1))
            print("Второй домен:")
            for seg2 in self.namespace.segment2.split("_"):
                seg2 = seg2.strip().split(':')
                try:
                    chain_name_2 = seg2[0]
                    if chain_name_2 == '' or chain_name_2 is None:
                        chain_name_2 = ' '
                    r_num_start_2 = int(seg2[1])
                    r_num_end_2 = int(seg2[2])
                    if r_num_start_2 > r_num_end_2:
                        print('Ошибка! Номер первого а.о. должен быть не больше последнего!')
                        sys.exit(-1)
                except ValueError:
                    print('Неверный формат segment2! Chain:StartNo:EndNo')
                    sys.exit(-1)
                print('Цепь {0:s}, а.о. с {1:d} по {2:d}'.format(
                    chain_name_2, r_num_start_2, r_num_end_2))
                for s_2 in range(r_num_start_2, r_num_end_2 + 1):
                    self.app.segment_2.append((chain_name_2, s_2))
        else:
            print("Сегменты должны быть заданы!")
            sys.exit(-1)

    def run(self):
        """Основной алгоритм программы"""
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
                    'Координаты центра масс первого домена: C1 ({0:.3f} \u212b, {1:.3f} \u212b, {2:.3f} \u212b)'.format(
                        c_mass_1[0],
                        c_mass_1[1],
                        c_mass_1[2]) +
                    '\n' +
                    'второго домена: C2 ({0:.3f} \u212b, {1:.3f} \u212b, {2:.3f} \u212b)'.format(
                        c_mass_2[0],
                        c_mass_2[1],
                        c_mass_2[2]) +
                    '\n' +
                    'расстояние между доменами: {0:.3f} \u212b'.format(r))
                bar1.update(n)
        except NoDataFor1stDom:
            print('Ошибка! Данные для первого домена не собраны!')
            sys.exit(-1)
        except NoDataFor2ndDom:
            print('Ошибка! Данные для второго домена не собраны!')
            sys.exit(-1)
        except DataNotObserved:
            print('Ощибка! Данные не собраны!')
            sys.exit(-1)
        bar1.finish()

    def xvg_stat(self):
        """

        :return:
        """
        try:
            r_min, r_max, r_mean, t_min, t_max, std, perc_25, median, perc_75 = self.app.stat()
        except (ValueError, NameError):
            print('Статистика недоступна!')
            return
        print('\nСтатистика:\nМинимальное расстояние между доменами равно: {0:.3f} \u212b (t= {1:.2f} пc)\n'
              'Максимальное расстояние между доменами равно: {2:.3f} \u212b (t= {3:.2f} пc)\n'
              'Среднее расстояние между доменами равно: {4:.3f} \u212b\nСтандартное отклонение: {5:.3f} \u212b\n'
              'Квартили: (25%) = {6:.3f} \u212b, (50%) = {7:.3f} \u212b, (75%) = {8:.3f} \u212b'.format(
            r_min, t_min, r_max, t_max, r_mean, std, perc_25, median, perc_75))

    def cluster_an(self):
        """

        :return:
        """
        n_cluster = self.namespace.n_cluster
        try:
            xhist, yhist, si_score, std_dev = self.app.cluster(n_cluster)
        except ImportError:
            print('Библиотека scikit-learn не установлена!')
            return
        except (NameError, ValueError):
            showinfo('Информация', 'Данные недоступны для кластерногого анализа')
            return
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Cluster analysis')
        ax.set_ylabel(r'$\% \ \tau$')
        ax.set_xlabel(r'$\xi,\ \AA$')
        ax.grid(True)
        ax.bar(xhist.flatten(), yhist, width=[3 * x for x in std_dev], align='center')
        print('Кластерный анализ:\nКоличество кластеров равно {0:d}\nSilhouette Coefficient = {1:.2f}\n'
              '(The best value is 1 and the worst value is -1.\n'
              'Values near 0 indicate overlapping clusters.\n'
              'Negative values generally indicate that a sample has been assigned\n'
              'to the wrong cluster, as a different cluster is more similar.)\nКластеры:'.format(len(xhist), si_score))
        for n, cls_center in enumerate(xhist.flatten()):
            print('Кластер № {0:d}: точек траектории {1:.1f} %, положение центроида - {2:.3f} \u212b, '
                  'СКО = {3:.3f} \u212b'.format(n + 1, yhist[n], cls_center, std_dev[n]))
        if self.namespace.ocluster:
            self.save_graph(fig, self.namespace.ocluster)

    def graph(self):
        """Графулька без эксэльки"""
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
