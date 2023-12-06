from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from model.DKA import *
from GenerationChainParamWidget import *
from AddChainWidget import *

class ChainInfo:
    def __init__(self):
        self.chain_str: str = ''
        self.chain_result: str = ''
        self.chain_transitions: list[str] = []

class CheckWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fontBig = QFont('Arial', 15)
        self.fontSmall = QFont('Arial', 13)
        self.chains_info: list[ChainInfo] = []

        self.dka: DKA() = None
        self.reg: RegularExpression = RegularExpression()
        self.InitUi()

    def InitUi(self):
        mainVLay = QVBoxLayout()
        generationHLay = QHBoxLayout()
        chainVLay = QVBoxLayout()
        checkVLay = QVBoxLayout()
        resultHLay = QHBoxLayout()
        btnHLay = QHBoxLayout()

        # mainVLay.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        chainVLay.setAlignment(Qt.AlignLeft)
        checkVLay.setAlignment(Qt.AlignLeft)
        mainVLay.setSpacing(10)

        generation_frame = QFrame()
        generation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        generation_frame.setLayout(generationHLay)

        chain_label = QLabel('Цепочки:')
        chain_label.setFont(self.fontBig)

        check_label = QLabel('Проверка:')
        check_label.setFont(self.fontBig)

        result_label = QLabel('Итог:')
        result_label.setFont(self.fontBig)

        self.chain_list_wid = QListWidget()
        self.chain_list_wid.setFont(self.fontBig)

        self.check_list_wid = QListWidget()
        self.check_list_wid.setFont(self.fontBig)

        self.result_line = QLineEdit()
        self.result_line.setMinimumHeight(30)
        self.result_line.setReadOnly(True)
        self.result_line.setFont(self.fontBig)

        generate_chain_btn = self.create_btn('Сгенерировать', self.fontBig, 40, self.generate_chains)
        add_chain_btn = self.create_btn('Добавить', self.fontBig, 40, self.generate_one_chain)
        del_chain_btn = self.create_btn('Удалить', self.fontBig, 40, self.del_chain)

        mainVLay.addWidget(generation_frame)
        mainVLay.addLayout(btnHLay)
        generationHLay.addLayout(chainVLay, 1)
        generationHLay.addLayout(checkVLay, 2)
        chainVLay.addWidget(chain_label)
        chainVLay.addWidget(self.chain_list_wid)
        checkVLay.addWidget(check_label)
        checkVLay.addWidget(self.check_list_wid)
        checkVLay.addLayout(resultHLay)
        resultHLay.addWidget(result_label)
        resultHLay.addWidget(self.result_line)
        btnHLay.addWidget(generate_chain_btn)
        btnHLay.addWidget(add_chain_btn)
        btnHLay.addWidget(del_chain_btn)
        self.setLayout(mainVLay)

        self.chain_list_wid.currentItemChanged.connect(self.show_check_result)

    def show_check_result(self):
        cur_ind: int = self.chain_list_wid.currentRow()
        self.result_line.setText(self.chains_info[cur_ind].chain_result)
        self.check_list_wid.clear()
        for line in self.chains_info[cur_ind].chain_transitions:
            self.check_list_wid.addItem(line[0] + ', ' + line[1])

    def generate_chains(self):
        if self.dka != None:
            dlg = GenerationChainParamWidget()
            dlg.setWindowTitle("Генерация цепочек")
            dlg.exec()
            if dlg.is_normal_exit:
                length_range = (int(dlg.from_spin.text()), int(dlg.to_spin.text()))
                number_of_list = int(dlg.count_spin.text())
                max_time_sec = int(dlg.time_spin.text())
                chains = self.reg.generate_samples(length_range, number_of_list, max_time_sec)

                self.clear_widget()
                for chain in chains:
                    self.add_chain(chain)

    def generate_one_chain(self):
        if self.dka != None:
            dlg: AddChainWidget = AddChainWidget()
            dlg.setWindowTitle("Генерация цепочки")
            dlg.exec()
            if dlg.is_normal_exit:
                chain = dlg.chain_line.text()
                self.add_chain(chain)

    def add_chain(self, chain: str):
        self.chains_info.append(ChainInfo())
        self.chains_info[-1].chain_str = chain
        check_result = self.dka.check_chain(chain)
        self.chains_info[-1].chain_result = check_result[0]
        self.chains_info[-1].chain_transitions = check_result[1]
        self.chain_list_wid.addItem(chain)

    def del_chain(self):
        if len(self.chains_info) > 0:
            cur_ind: int = self.chain_list_wid.currentRow()
            self.chain_list_wid.takeItem(cur_ind)
            self.chains_info.pop(cur_ind)

    def clear_widget(self):
        self.chain_list_wid.clear()
        self.chains_info.clear()
        self.check_list_wid.clear()
        self.result_line.clear()

    def create_btn(self, title: str, font: QFont, minH: int, func) -> QPushButton:
        btn = QPushButton(title)
        btn.setFont(font)
        btn.setMinimumHeight(minH)
        btn.clicked.connect(func)
        return btn