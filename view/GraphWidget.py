from collections import defaultdict, Counter

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import *
from pyvis.network import Network
import pyvis._version
import networkx as nx

from model.DKA import *


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.m_output = QWebEngineView()

        lay = QVBoxLayout(self)
        lay.addWidget(self.m_output)
        self.setLayout(lay)

    @staticmethod
    def generate_graph(dka: DKA, path: str):
        G = nx.MultiDiGraph()
        for i in dka.dka_table.index:
            G.add_node(i, label=i)

        for i in dka.dka_table.index:
            row_dict = dka.dka_table.loc[i].to_dict().items()
            for key, val in row_dict:
                if val != '_':
                    G.add_edge(i, val, label=key, physics=False)
        # for i in dt[:]

        scale = 7
        scale *= dka.dka_table.size
        pos: dict = nx.circular_layout(G, scale=scale)

        nt = Network(directed=True, bgcolor='#222222', font_color='white', height='1100px')
        nt.options.edges.smooth.type = "curvedCW"
        nt.options.edges.smooth.roundness = 0.4

        nG = nx.MultiDiGraph()
        for i in G.nodes:
            nG.add_node(i,
                        lable=i,
                        shape='circle',
                        color="blue",
                        x=pos[i][0],
                        y=pos[i][1],
                        physics=True,
                        )
        nG.add_node('q0', color="green")
        for cond in dka.final_conds:
            nG.add_node(cond, color="red")
        labels = defaultdict(list)

        for key in dka.dka_table.index:
            val: dict = dka.dka_table.loc[key].to_dict()
            states: list = list(val.values())
            count = Counter(states)
            for i in dka.dka_table.columns:
                state = val[i]
                if state != '_':
                    m_state = count[state]
                    if m_state >= 1:
                        labels[(key, state)].append(i)

        for i in dka.dka_table.index:
            for key, val in dka.dka_table.loc[i].to_dict().items():
                if val != '_':
                    nG.add_edge(i,
                                val,
                                label=",".join(labels[(i, val)]),
                                physics=False,
                                )

        if pyvis._version.__version__ > '0.1.9':
            nt.from_nx(nG, show_edge_weights=False)
        else:
            nt.from_nx(nG)

        # nt.show_buttons(filter_=['physics'])
        # nt.show_buttons()
        nt.save_graph(path)

    @QtCore.pyqtSlot()
    def set_dka(self, dt: DKA):
        filename = "graph.html"
        path = filename
        self.generate_graph(dt, path)
        with open(path, "r") as file:
            html: str = file.read()
        self.m_output.setHtml(html, QUrl(path))
