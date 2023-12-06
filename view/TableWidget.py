from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import pandas as pd
from model.DKA import *

class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fontBig = QFont('Arial', 15)
        self.fontSmall = QFont('Arial', 13)
        self.dka: DKA = None
        self.InitUi()

    def InitUi(self):

        mainVLay = QVBoxLayout()
        mainVLay.setAlignment(Qt.AlignLeft)

        self.table = QTableWidget()

        save_btn = QPushButton('Сохранить Дка')
        save_btn.setContentsMargins(8, 2, 8, 2)
        save_btn.setFont(self.fontBig)
        save_btn.setMinimumHeight(35)
        save_btn.setMaximumWidth(280)

        mainVLay.addWidget(self.table)
        mainVLay.addWidget(save_btn)
        self.setLayout(mainVLay)

        save_btn.clicked.connect(self.save_dka)

    def create_table(self, dka: DKA):
        self.dka = dka
        self.table.clear()
        self.table.setRowCount(dka.dka_table.shape[0])
        self.table.setColumnCount(dka.dka_table.shape[1])
        self.table.setHorizontalHeaderLabels(dka.dka_table.columns)

        for i in range(dka.dka_table.shape[0]):
            for j in range(dka.dka_table.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(dka.dka_table.iloc[i, j])))
        self.table.setVerticalHeaderLabels(dka.dka_table.index)

    def save_dka(self):
        if self.dka != None:
            msg = QMessageBox()
            msg.setWindowTitle("Information MessageBox")

            filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.csv);;All Files (*)")
            if filename == '':
                msg.setText('Файл не выбран')
                msg.exec()
                return
            self.dka.dka_table.to_csv(filename, index=True, sep=';')

