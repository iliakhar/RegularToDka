from copy import deepcopy

from RegularExpression import *
from NkaCondition import *


class NKA:
    last_cond_id = -1

    def __init__(self, reg: RegularExpression, alphabet: list[str]):
        self.alphabet: list[str] = alphabet
        NkaCondition.alphabet = alphabet
        self.reg = reg
        self.nka_e: list[NkaConditionE] = []
        self.nka: list[NkaCondition] = []
        self.final_conds_ids: list[int] = []
        self.create_nka_e()
        self.create_nka()

    def __str__(self):
        text: str = 'alphabet: '
        for symb in self.alphabet:
            text += str(symb) + ', '
        text = text[:-2] + '\n'
        for ind, cond_id in enumerate(self.nka):
            text += str(ind) + ') ' + cond_id.__str__() + '\n'
        text += 'final conditions: '
        for cond_id in self.final_conds_ids:
            text += str(cond_id) + ', '
        text = text[:-2] + '\n'
        return text

    def create_nka_e(self):
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
                self.nka_e[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                # print(start_id, '\n')
                cur_symb_ind += 1
                continue

            if sub_reg[cur_symb_ind] == '(':
                closed_bracket_ind: int = self.reg.find_closed_bracket(sub_reg, cur_symb_ind, 'round')
                start_end_conds_ids: tuple[int, int] = self.choice_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                self.nka_e[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                cur_symb_ind = closed_bracket_ind + 1
                continue

            if sub_reg[cur_symb_ind] == '[':
                closed_bracket_ind: int = self.reg.find_closed_bracket(sub_reg, cur_symb_ind, 'square')
                start_end_conds_ids: tuple[int, int] = self.cycle_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                self.nka_e[start_id].cond_transition['^'].append(start_end_conds_ids[0])
                start_id = start_end_conds_ids[1]
                cur_symb_ind = closed_bracket_ind + 1
                continue


        return start_id


    def choice_action(self, sub_reg: str) -> tuple[int, int]:
        start_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        end_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        self.nka_e.append(start_cond)
        self.nka_e.append(end_cond)
        self.process_sub_parts(start_cond.id, end_cond.id, sub_reg)
        return start_cond.id, end_cond.id

    def sequence_action(self, symb: str) -> tuple[int, int]:
        start_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        end_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        self.nka_e.append(start_cond)
        self.nka_e.append(end_cond)
        self.nka_e[start_cond.id].cond_transition[symb].append(end_cond.id)
        return start_cond.id, end_cond.id

    def cycle_action(self, sub_reg: str) -> tuple[int, int]:
        start_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        end_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        cycle_start_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        cycle_end_cond: NkaConditionE = NkaConditionE(NKA.get_unique_cond_id())
        self.nka_e.append(start_cond)
        self.nka_e.append(end_cond)
        self.nka_e.append(cycle_start_cond)
        self.nka_e.append(cycle_end_cond)
        self.nka_e[start_cond.id].cond_transition['^'].append(end_cond.id)
        self.nka_e[start_cond.id].cond_transition['^'].append(cycle_start_cond.id)
        self.nka_e[cycle_end_cond.id].cond_transition['^'].append(cycle_start_cond.id)
        self.nka_e[cycle_end_cond.id].cond_transition['^'].append(end_cond.id)

        self.process_sub_parts(cycle_start_cond.id, cycle_end_cond.id, sub_reg)
        return start_cond.id, end_cond.id

    def process_sub_parts(self, start_cond_id: int, end_cond_id: int, sub_reg: str):
        brackets_inds: list[tuple[int, int]] = self.reg.find_outer_brackets(sub_reg)
        separated_regular: list[str] = self.reg.separate_by_plus(sub_reg, brackets_inds)
        print(separated_regular)
        for reg_part in separated_regular:
            conds_ids = self.perform_act(reg_part, start_cond_id)
            self.nka_e[conds_ids].cond_transition['^'].append(end_cond_id)

    def get_e_transitions_path_recurs(self, start_cond: NkaConditionE) -> dict[str: list[int]]:
        if len(start_cond.cond_transition['^']) == 0:
            if start_cond.id == 1:  # final cond
                start_cond.cond_transition['^'].append(-1)  # mark final cond
            return start_cond.cond_transition

        e_path_final_dict: list[dict[str: list[int]]] = []
        for e_path_ind in start_cond.cond_transition['^']:
            if len(self.nka_e[e_path_ind].through_e_transition.keys()) == 0:
                self.nka_e[e_path_ind].through_e_transition = self.get_e_transitions_path_recurs(self.nka_e[e_path_ind])
                if -1 in self.nka_e[e_path_ind].through_e_transition['^']:
                    self.final_conds_ids.append(e_path_ind)
            e_path_final_dict.append(self.nka_e[e_path_ind].through_e_transition)

        return merge_dicts(e_path_final_dict)

    def create_nka(self):
        for cond in self.nka_e:
            if len(cond.through_e_transition.keys()) == 0:
                self.nka_e[cond.id].through_e_transition = self.get_e_transitions_path_recurs(self.nka_e[cond.id])
                if -1 in self.nka_e[cond.id].through_e_transition['^']:
                    self.final_conds_ids.append(cond.id)

                for key, cond_ids in self.nka_e[cond.id].through_e_transition.items():
                    for cond_id in cond_ids:
                        self.nka_e[cond_id].is_important_cond = True

        print(self.final_conds_ids)

        self.nka_e[0].is_important_cond = True
        tmp_final_conds: list[int] = []
        for cond in self.nka_e:
            if cond.is_important_cond:
                if cond.id in self.final_conds_ids:
                    tmp_final_conds.append(cond.id)
                self.nka.append(NkaCondition(cond.id))
                self.nka[-1].cond_transition = cond.through_e_transition
                self.nka[-1].cond_transition.pop('^', None)
        print(tmp_final_conds)
        self.final_conds_ids = tmp_final_conds

        id_dict: dict[int, int] = {}
        for ind, cond in enumerate(self.nka):
            id_dict[cond.id] = ind

        for cond_ind, cond in enumerate(self.nka):
            self.nka[cond_ind].id = id_dict[cond.id]
            for key, vals in cond.cond_transition.items():
                for ind, val in enumerate(vals):
                    self.nka[cond.id].cond_transition[key][ind] = id_dict[val]

        for ind in range(len(self.final_conds_ids)):
            self.final_conds_ids[ind] = id_dict[self.final_conds_ids[ind]]



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