import itertools
import sys
from dataclasses import dataclass, field

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import copy

from GraphWidget import *
from CheckWidget import *
from TableWidget import *
from DkaCreationWidget import *

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fontBig = QFont('Arial', 15)
        self.fontSmall = QFont('Arial', 13)
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Преобразователь')
        # self.setWindowIcon(QIcon('icon/table_icon.png'))
        self.move(300, 300)
        self.resize(1200, 700)
        self.setMinimumWidth(1400)

        mainHLay = QHBoxLayout()

        self.dka_wid = DkaCreationWidget()
        self.tab_wid = QTabWidget()

        self.dka_table = TableWidget()
        self.dka_graph = GraphWidget()
        self.dka_check = CheckWidget()

        self.tab_wid.addTab(self.dka_table, "Таблица")
        self.tab_wid.addTab(self.dka_graph, "Граф")
        self.tab_wid.addTab(self.dka_check, "Проверка")
        self.tab_wid.setFont(self.fontBig)

        mainHLay.addWidget(self.dka_wid,1)
        mainHLay.addWidget(self.tab_wid,3)
        self.setLayout(mainHLay)

        self.dka_wid.changeDka.connect(self.change_dka)

    def change_dka(self, reg: RegularExpression):
        self.dka_table.create_table(deepcopy(self.dka_wid.dka))
        self.dka_graph.set_dka(deepcopy(self.dka_wid.dka))

        self.dka_check.clear_widget()
        self.dka_check.dka = deepcopy(self.dka_wid.dka)
        self.dka_check.reg = reg
