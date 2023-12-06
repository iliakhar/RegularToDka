from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont, QPixmap, QIcon)

class AddChainWidget(QDialog):

    def __init__(self):
        super().__init__()
        self.is_normal_exit = False
        self.fontSmall = QFont('Arial', 13)
        self.fontBig = QFont('Arial', 15)
        self.initUI()

    def initUI(self):
        self.setMaximumHeight(180)
        mainVLay = QVBoxLayout()
        chainHLay = QHBoxLayout()
        acceptHLay = QHBoxLayout()

        mainVLay.setSpacing(10)

        chain_lbl = QLabel('Цепочка:')
        chain_lbl.setFont(self.fontBig)

        self.chain_line = QLineEdit()
        self.chain_line.setFont(self.fontBig)

        self.accept_btn = QPushButton('Готово')
        self.accept_btn.setContentsMargins(8,2,8,2)
        self.accept_btn.setFont(self.fontBig)
        self.accept_btn.setMinimumHeight(35)


        self.setLayout(mainVLay)
        mainVLay.addLayout(chainHLay)
        mainVLay.addLayout(acceptHLay)
        chainHLay.addWidget(chain_lbl)
        chainHLay.addWidget(self.chain_line)
        acceptHLay.addStretch(1)
        acceptHLay.addWidget(self.accept_btn)

        self.accept_btn.clicked.connect(self.click_accept)
        self.chain_line.textChanged.connect(self.check_format)

    def check_format(self):
        if self.chain_line.text() != '':
            if self.chain_line.text()[-1] == '_':
                self.chain_line.setText(self.chain_line.text()[:-1])

    def click_accept(self):
        self.is_normal_exit = True
        self.close()

    def create_spin_box(self, min_h: int, max_w: int, range_spin: tuple[int, int]) -> QSpinBox:
        spin = QSpinBox()
        spin.setFont(self.fontBig)
        spin.setMinimumHeight(min_h)
        spin.setMaximumWidth(max_w)
        spin.setRange(range_spin[0], range_spin[1])
        return spin
