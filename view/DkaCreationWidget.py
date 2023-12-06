from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from model.RegularExpression import *
from model.DKA import *

class DkaCreationWidget(QWidget):
    changeDka = pyqtSignal(RegularExpression)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fontBig = QFont('Arial', 15)
        self.fontSmall = QFont('Arial', 13)
        self.dka = DKA()
        self.InitUi()

    def InitUi(self):

        mainVLay = QVBoxLayout()
        btnHLay = QHBoxLayout()

        mainVLay.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        mainVLay.setSpacing(10)

        alphabet_label = QLabel('Алфавит:')
        alphabet_label.setFont(self.fontBig)

        reg_label = QLabel('Регулярное выражение:')
        reg_label.setFont(self.fontBig)

        self.alphabet_line = QLineEdit()
        self.alphabet_line.setFont(self.fontBig)
        self.alphabet_line.setMinimumHeight(35)
        self.alphabet_line.setMaximumWidth(220)

        self.reg_line = QLineEdit()
        self.reg_line.setFont(self.fontBig)
        self.reg_line.setMinimumHeight(35)

        save_reg_btn = self.create_btn('Сохранить', self.fontBig, 40, self.save_regular)
        load_reg_btn = self.create_btn('Загрузить', self.fontBig, 40, self.load_regular)
        create_dka_btn = self.create_btn('Составить ДКА', self.fontBig, 40, self.create_dka)

        mainVLay.addWidget(alphabet_label)
        mainVLay.addWidget(self.alphabet_line)
        mainVLay.addSpacing(20)
        mainVLay.addWidget(reg_label)
        mainVLay.addWidget(self.reg_line)
        mainVLay.addSpacing(20)
        mainVLay.addLayout(btnHLay)
        mainVLay.addWidget(create_dka_btn)
        btnHLay.addWidget(save_reg_btn)
        btnHLay.addWidget(load_reg_btn)
        self.setLayout(mainVLay)

        self.alphabet_line.textChanged.connect(self.check_alphabet_format)

    def check_lines(self) -> bool:
        msg = QMessageBox()
        msg.setWindowTitle("Information MessageBox")

        alphabet: list[str] = list(self.alphabet_line.text().strip())
        if len(alphabet) > len(set(alphabet)):
            msg.setText('Недопустимо дублировать символы в алфавите')
            msg.exec()
            return False
        if (alphabet == '') or (self.reg_line.text() == ''):
            msg.setText('Заполните пустые строки')
            msg.exec()
            return False
        return True

    def save_regular(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information MessageBox")
        if not self.check_lines():
            return
        reg = RegularExpression()
        alphabet: list[str] = list(self.alphabet_line.text().strip())
        error_format = reg.set_regular(self.reg_line.text(), alphabet)
        if error_format != '':
            msg.setText(error_format)
            msg.exec()
            return

        filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
        if filename == '':
            msg.setText('Файл не выбран')
            msg.exec()
            return
        with open(filename, 'w') as f:
            text_to_save: str = self.alphabet_line.text() + '\n' + self.reg_line.text()
            f.write(text_to_save)


    def load_regular(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information MessageBox")
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", ".", "Text Files (*.txt);;All Files (*)")
        if filename == '':
            msg.setText('Файл не выбран')
            msg.exec()
            return

        with open(filename, 'r') as f:
            alphabet_str: str = f.readline().removesuffix('\n')
            reg_str: str = f.readline().removesuffix('\n')
            if (alphabet_str == '') or (reg_str == ''):
                msg.setText('Неверный формат файла')
                msg.exec()
                return
            reg = RegularExpression()
            alphabet: list[str] = list(alphabet_str)
            error_format = reg.set_regular(reg_str, alphabet)
            if error_format != '':
                msg.setText(error_format)
                msg.exec()
                return
            self.reg_line.setText(reg_str)
            self.alphabet_line.setText(alphabet_str)


    @pyqtSlot()
    def create_dka(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information MessageBox")
        if not self.check_lines():
            return
        reg = RegularExpression()
        alphabet: list[str] = list(self.alphabet_line.text().strip())
        error_format = reg.set_regular(self.reg_line.text(), alphabet)
        if error_format != '':
            msg.setText(error_format)
            msg.exec()
            return

        nka: NKA = NKA()
        nka.init_nka(reg, alphabet)
        self.dka.init_dka(nka)
        self.changeDka.emit(reg)

    def create_btn(self, title: str, font: QFont, minH: int, func) -> QPushButton:
        btn = QPushButton(title)
        btn.setFont(font)
        btn.setMinimumHeight(minH)
        btn.clicked.connect(func)
        return btn

    def check_alphabet_format(self):
        unaccepted_symbs: str = '()[]+*'
        text: str = self.sender().text()
        if len(text) != 0:
            if (text[-1] in text[:-1]) or (text[-1] in unaccepted_symbs):
                self.sender().setText(text[:-1])
