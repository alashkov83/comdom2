# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comdom2_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QTabWidget, QPlainTextEdit, QPushButton, QFrame, \
    QProgressBar, QLabel, QMenuBar, QAction, QMenu, QStatusBar, QFileDialog, QErrorMessage, QMessageBox
from PyQt5.QtCore import QRect, Qt, QSize, QCoreApplication
from .joke import joke
from .mainapp import App, XLSWImportError, XLWTImportError, BadExtError, NoDataFor1stDom, NoDataFor2ndDom, \
    DataNotObserved, SmothPlotError

class QtGui(QMainWindow):

    def __init__(self, namespace):
        super().__init__()
        self.setupUi()
        if namespace.input:
            self.open_pdb(namespace.input)
        self.app = App()
        self.show()


    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1034, 849)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(0, 0, 231, 231))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName("tab_1")
        self.plainTextEdit_2 = QPlainTextEdit(self.tab_1)
        self.plainTextEdit_2.setGeometry(QRect(0, 20, 230, 120))
        self.plainTextEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.plainTextEdit_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton_3 = QPushButton(self.tab_1)
        self.pushButton_3.setGeometry(QRect(0, 150, 97, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self.tab_1)
        self.pushButton_4.setGeometry(QRect(120, 150, 97, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.plainTextEdit_3 = QPlainTextEdit(self.tab_2)
        self.plainTextEdit_3.setGeometry(QRect(0, 20, 230, 120))
        self.plainTextEdit_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.plainTextEdit_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit_3.setUndoRedoEnabled(False)
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.pushButton = QPushButton(self.tab_2)
        self.pushButton.setGeometry(QRect(0, 150, 97, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QRect(120, 150, 97, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(230, 0, 800, 600))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(800, 600))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QRect(231, 607, 800, 192))
        self.plainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(10, 280, 211, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(80, 250, 71, 17))
        self.label.setTextFormat(Qt.RichText)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QRect(70, 320, 97, 27))
        self.pushButton_5.setObjectName("pushButton_5")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1034, 25))
        self.menubar.setObjectName("menubar")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuRun = QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionOpen_PDB = QAction(self)
        self.actionOpen_PDB.setObjectName("actionOpen_PDB")
        self.actionOpen_PDB.triggered.connect(self.open_pdb)
        self.actionSave_Plot = QAction(self)
        self.actionSave_Plot.setObjectName("actionSave_Plot")
        self.actionSave_as = QAction(self)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_Log = QAction(self)
        self.actionSave_Log.setObjectName("actionSave_Log")
        self.actionQuit = QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAll_residues = QAction(self)
        self.actionAll_residues.setObjectName("actionAll_residues")
        self.actionOnly_hydrophobic_residues = QAction(self)
        self.actionOnly_hydrophobic_residues.setObjectName("actionOnly_hydrophobic_residues")
        self.actionPlot_grid = QAction(self)
        self.actionPlot_grid.setObjectName("actionPlot_grid")
        self.actionPlot_legend = QAction(self)
        self.actionPlot_legend.setObjectName("actionPlot_legend")
        self.actionPlot_smoothing = QAction(self)
        self.actionPlot_smoothing.setObjectName("actionPlot_smoothing")
        self.actionStatistics = QAction(self)
        self.actionStatistics.setObjectName("actionStatistics")
        self.actionClustering = QAction(self)
        self.actionClustering.setObjectName("actionClustering")
        self.actionAbout = QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.about)
        self.menu.addAction(self.actionOpen_PDB)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSave_Plot)
        self.menu.addAction(self.actionSave_as)
        self.menu.addAction(self.actionSave_Log)
        self.menu.addSeparator()
        self.menu.addAction(self.actionQuit)
        self.menuRun.addAction(self.actionAll_residues)
        self.menuRun.addAction(self.actionOnly_hydrophobic_residues)
        self.menuOptions.addAction(self.actionPlot_grid)
        self.menuOptions.addAction(self.actionPlot_legend)
        self.menuOptions.addAction(self.actionPlot_smoothing)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionStatistics)
        self.menuOptions.addAction(self.actionClustering)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)

    def about(self):
        """

        """
        QMessageBox.about(self,
                          'About',
                          'The dependence of the distance between the centers of mass of protein domains on the time of MD')

    def open_pdb(self, input_pdb=None):
        """

        :param input_pdb:
        :return:
        """
        if input_pdb:
            pdb = input_pdb
        else:
            opt = QFileDialog.Options()
            pdb, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;PDB files (*.pdb)", options=opt)
        if pdb:
            try:
                self.app.open_pdb(pdb)
            except FileNotFoundError:
                return
            else:
                pass
        else:
            return

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Comdom 2"))
        self.pushButton_3.setText(_translate("MainWindow", "Add range"))
        self.pushButton_4.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Domain 1"))
        self.pushButton.setText(_translate("MainWindow", "Add range"))
        self.pushButton_2.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Domain 2"))
        self.label.setText(_translate("MainWindow", "<b>Progress</b>"))
        self.pushButton_5.setText(_translate("MainWindow", "Stop!"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_PDB.setText(_translate("MainWindow", "Open PDB"))
        self.actionSave_Plot.setText(_translate("MainWindow", "Save Plot"))
        self.actionSave_as.setText(_translate("MainWindow", "Save Data"))
        self.actionSave_Log.setText(_translate("MainWindow", "Save Log"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAll_residues.setText(_translate("MainWindow", "All residues"))
        self.actionOnly_hydrophobic_residues.setText(_translate("MainWindow", "Only hydrophobic residues"))
        self.actionPlot_grid.setText(_translate("MainWindow", "Plot grid"))
        self.actionPlot_legend.setText(_translate("MainWindow", "Plot legend"))
        self.actionPlot_smoothing.setText(_translate("MainWindow", "Plot smoothing"))
        self.actionStatistics.setText(_translate("MainWindow", "Statistics"))
        self.actionClustering.setText(_translate("MainWindow", "Clustering"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
