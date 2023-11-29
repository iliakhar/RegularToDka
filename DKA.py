from NKA import *


class DkaCondition:
    alphabet: list[str] = []

    def __init__(self, cond_id: int):
        self.id = cond_id
        self.cond_transition: dict[str: int] = {}
        for symb in DkaCondition.alphabet:
            self.cond_transition[symb] = []

    def __str__(self):
        text: str = 'id: ' + str(self.id) + '\n'
        for key, val in self.cond_transition.items():
            text += str(key) + ': ' + str(val) + '\n'
        return text


class DKA:
    last_cond_id = -1

    def __init__(self, nka: NKA):
        self.alphabet: list[str] = nka.alphabet
        DkaCondition.alphabet = nka.alphabet
        self.nka = nka

        self.all_condition: dict[tuple: int] = {}
        self.conditions_queue: list[tuple] = []
        self.dka: list[DkaCondition] = []
        self.create_dka()

    def __str__(self):
        text: str = 'alphabet: '
        for symb in self.alphabet:
            text += str(symb) + ', '
        text = text[:-2] + '\n'
        for ind, cond in enumerate(self.dka):
            text += str(ind) + ') ' + cond.__str__() + '\n'
        return text

    def create_dka(self):
        pass



    @staticmethod
    def get_unique_cond_id():
        NKA.last_cond_id += 1
        return NKA.last_cond_id
