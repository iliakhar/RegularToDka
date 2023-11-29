from RegularExpression import *


class NkaCondition:
    alphabet: list[str] = []

    def __init__(self, cond_id: int):
        self.id = cond_id
        self.cond_transition: dict[str: set[int]] = {}
        for symb in NkaCondition.alphabet:
            self.cond_transition[symb] = []
        self.cond_transition['^'] = []
        self.through_e_transition: list[int] = []

    def __str__(self):
        text: str = 'id: ' + str(self.id) + '\n'
        for key, val in self.cond_transition.items():
            text += str(key) + ': '
            for conds in val:
                text += str(conds) + ', '
            text = text[:-2] + '\n'
        text += 'e-path: '
        for conds_ids in self.through_e_transition:
            text += str(conds_ids) + ', '
        text = text[:-2] + '\n'
        return text


class NKA:
    last_cond_id = -1

    def __init__(self, reg: RegularExpression, alphabet: list[str]):
        self.alphabet: list[str] = alphabet
        NkaCondition.alphabet = alphabet
        self.reg = reg
        self.nka: list[NkaCondition] = []
        self.create_nka()
        self.create_paths_through_e_transitions()

    def __str__(self):
        text: str = 'alphabet: '
        for symb in self.alphabet:
            text += str(symb) + ', '
        text = text[:-2] + '\n'
        for ind, cond in enumerate(self.nka):
            text += str(ind) + ') ' + cond.__str__() + '\n'
        return text

    def create_nka(self):
        print(self.reg.regular)
        self.choice_action(self.reg.regular[:])

    def perform_act(self, sub_reg: str, start_cond_id: int) -> int:
        cur_symb_ind: int = 0
        start_id: int = start_cond_id
        while True:
            if cur_symb_ind >= len(sub_reg):
                break
            if cur_symb_ind == 0:
                pass

            if sub_reg[cur_symb_ind] in self.alphabet:
                start_end_conds_ids: tuple[int, int] = self.sequence_action(sub_reg[cur_symb_ind])
                # print(start_end_conds_ids, start_id)
                self.nka[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                # print(start_id, '\n')
                cur_symb_ind += 1
                continue

            if sub_reg[cur_symb_ind] == '(':
                closed_bracket_ind: int = self.reg.find_closed_bracket(sub_reg, cur_symb_ind, 'round')
                start_end_conds_ids: tuple[int, int] = self.choice_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                self.nka[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                cur_symb_ind = closed_bracket_ind + 1
                continue

            if sub_reg[cur_symb_ind] == '[':
                closed_bracket_ind: int = self.reg.find_closed_bracket(sub_reg, cur_symb_ind, 'square')
                start_end_conds_ids: tuple[int, int] = self.cycle_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                self.nka[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                cur_symb_ind = closed_bracket_ind + 1
                continue


        return start_id


    def choice_action(self, sub_reg: str) -> tuple[int, int]:
        start_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        end_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        self.nka.append(start_cond)
        self.nka.append(end_cond)
        self.process_sub_parts(start_cond.id, end_cond.id, sub_reg)
        return start_cond.id, end_cond.id

    def sequence_action(self, symb: str) -> tuple[int, int]:
        start_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        end_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        self.nka.append(start_cond)
        self.nka.append(end_cond)
        self.nka[start_cond.id].cond_transition[symb].append(end_cond.id)
        return start_cond.id, end_cond.id

    def cycle_action(self, sub_reg: str) -> tuple[int, int]:
        start_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        end_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        cycle_start_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        cycle_end_cond: NkaCondition = NkaCondition(NKA.get_unique_cond_id())
        self.nka.append(start_cond)
        self.nka.append(end_cond)
        self.nka.append(cycle_start_cond)
        self.nka.append(cycle_end_cond)
        self.nka[start_cond.id].cond_transition['^'].append(end_cond.id)
        self.nka[start_cond.id].cond_transition['^'].append(cycle_start_cond.id)
        self.nka[cycle_end_cond.id].cond_transition['^'].append(cycle_start_cond.id)
        self.nka[cycle_end_cond.id].cond_transition['^'].append(end_cond.id)

        self.process_sub_parts(cycle_start_cond.id, cycle_end_cond.id, sub_reg)
        return start_cond.id, end_cond.id

    def process_sub_parts(self, start_cond_id: int, end_cond_id: int, sub_reg: str):
        brackets_inds: list[tuple[int, int]] = self.reg.find_outer_brackets(sub_reg)
        separated_regular: list[str] = self.reg.separate_by_plus(sub_reg, brackets_inds)
        print(separated_regular)
        for reg_part in separated_regular:
            conds_ids = self.perform_act(reg_part, start_cond_id)
            self.nka[conds_ids].cond_transition['^'].append(end_cond_id)

    def get_e_transitions_path_recurs(self, start_cond: NkaCondition) -> list[int]:
        if len(start_cond.cond_transition['^']) == 0:
            return [start_cond.id]

        e_path_final_val: set = set()
        for e_path_ind in start_cond.cond_transition['^']:
            if len(self.nka[e_path_ind].through_e_transition) == 0:
                self.nka[e_path_ind].through_e_transition = self.get_e_transitions_path_recurs(self.nka[e_path_ind])
            e_path_final_val.update(self.nka[e_path_ind].through_e_transition)

        return list(e_path_final_val)

    def create_paths_through_e_transitions(self):
        for cond in self.nka:
            if len(cond.cond_transition['^']) != 0:
                self.nka[cond.id].through_e_transition = self.get_e_transitions_path_recurs(self.nka[cond.id])

    @staticmethod
    def get_unique_cond_id():
        NKA.last_cond_id += 1
        return NKA.last_cond_id


def merge_dicts(dicts_list: list[dict[str:list[int]]]):
    merged_dict: dict[str:list[int]] = {}
    keys: set[str] = set()
    for dict in dicts_list:
        keys.update(dict.keys())
    for key in keys:
        merged_dict[key] = []
    for dict in dicts_list:
        for key, value in dict.items():

            merged_dict[key] += value
    return merged_dict