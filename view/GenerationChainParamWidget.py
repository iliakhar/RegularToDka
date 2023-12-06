
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import (QFont, QPixmap, QIcon)
from PyQt5.QtCore import Qt

class GenerationChainParamWidget(QDialog):

    def __init__(self):
        super().__init__()
        self.is_normal_exit = False
        self.fontSmall = QFont('Arial', 13)
        self.fontBig = QFont('Arial', 15)
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 210)
        mainVLay = QVBoxLayout()
        rangeHLay = QHBoxLayout()
        labelVLay = QVBoxLayout()
        spinBoxVLay = QVBoxLayout()
        countTimeHLay = QHBoxLayout()
        acceptHLay = QHBoxLayout()

        mainVLay.setSpacing(10)
        mainVLay.setAlignment(Qt.AlignLeft)

        range_lbl = QLabel('Диапазон:')
        range_lbl.setFont(self.fontBig)

        from_lbl = QLabel('от:')
        from_lbl.setFont(self.fontBig)

        to_lbl = QLabel('до:')
        to_lbl.setFont(self.fontBig)

        count_lbl = QLabel('Колличество цепочек:  ')
        count_lbl.setFont(self.fontBig)

        time_lbl = QLabel('Макс. время генерации:')
        time_lbl.setFont(self.fontBig)

        self.from_spin = self.create_spin_box(30, 100, (0, 100))
        self.to_spin = self.create_spin_box(30, 100, (1, 100))
        self.count_spin = self.create_spin_box(30, 100, (1, 100))
        self.time_spin = self.create_spin_box(30, 100, (1, 100))

        self.count_spin.setValue(5)
        self.time_spin.setValue(5)

        self.accept_btn = QPushButton('Готово')
        self.accept_btn.setContentsMargins(8,2,8,2)
        self.accept_btn.setFont(self.fontBig)
        self.accept_btn.setMinimumHeight(35)


        self.setLayout(mainVLay)
        mainVLay.addLayout(rangeHLay)
        mainVLay.addSpacing(15)
        mainVLay.addLayout(countTimeHLay)
        mainVLay.addLayout(acceptHLay)
        rangeHLay.addWidget(range_lbl)
        rangeHLay.addWidget(from_lbl)
        rangeHLay.addWidget(self.from_spin)
        rangeHLay.addWidget(to_lbl)
        rangeHLay.addWidget(self.to_spin)
        rangeHLay.addStretch(1)
        countTimeHLay.addLayout(labelVLay)
        countTimeHLay.addLayout(spinBoxVLay, 1)
        labelVLay.addWidget(count_lbl)
        labelVLay.addWidget(time_lbl)
        spinBoxVLay.addWidget(self.count_spin)
        spinBoxVLay.addWidget(self.time_spin)
        acceptHLay.addStretch(1)
        acceptHLay.addWidget(self.accept_btn)


        self.accept_btn.clicked.connect(self.click_accept)

    def check_space(self):
        if self.line_with_name.text() != '':
            if self.line_with_name.text()[-1] == ' ':
                self.line_with_name.setText(self.line_with_name.text()[:-1])

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
