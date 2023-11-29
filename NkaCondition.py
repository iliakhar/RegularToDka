

class NkaCondition:
    alphabet: list[str] = []

    def __init__(self, cond_id: int):
        self.id = cond_id
        self.cond_transition: dict[str: list[int]] = {}
        for symb in NkaCondition.alphabet:
            self.cond_transition[symb] = []


    def __str__(self):
        text: str = 'id: ' + str(self.id) + '\n'
        for key, val in self.cond_transition.items():
            text += str(key) + ': '
            for conds in val:
                text += str(conds) + ', '
            text = text[:-2] + '\n'
        return text


class NkaConditionE(NkaCondition):

    def __init__(self, cond_id: int):
        super().__init__(cond_id)
        self.cond_transition['^'] = []
        self.through_e_transition: dict[str: list[int]] = {}
        self.is_important_cond = False
