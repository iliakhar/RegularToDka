from model.NKA import *
import numpy as np
import pandas as pd


class DKA:
    last_cond_id = -1

    def __init__(self):

        self.alphabet: list[str] = []
        self.nka: NKA = None
        self.all_condition_tuples: list[tuple] = []
        self.all_condition_names: list[str] = []

        self.dka_table: pd.DataFrame = None
        self.empty_row: list[str] = []
        self.final_conds: list[str] = []

    def init_dka(self, nka: NKA):
        DKA.last_cond_id = -1
        self.alphabet = nka.alphabet
        self.nka = nka
        self.dka_table = pd.DataFrame(dict.fromkeys(self.alphabet, []))
        self.empty_row = ['_'] * len(self.alphabet)
        self.final_conds = []
        self.all_condition_tuples = []
        self.all_condition_names = []

        self.thompson_algorithm()
        self.find_final_conds()


    def __str__(self):
        text: str = self.dka_table.__str__() + '\n\n'
        text += 'final conditions: '
        for cond in self.final_conds:
            text += cond + ', '
        text = text[:-2] + '\n'
        return text

    def thompson_algorithm(self):

        cur_cond_name: str = DKA.get_unique_cond_name()
        self.all_condition_tuples.append((0,))
        self.all_condition_names.append(cur_cond_name)
        conditions_queue: list[tuple] = [(0,)]
        self.dka_table.loc[cur_cond_name] = self.empty_row
        # print(self.nka)
        while len(conditions_queue) != 0:
            # print('Q: ', conditions_queue)
            conds: tuple = conditions_queue.pop(0)
            cur_cond_ind: int = self.all_condition_tuples.index(conds)
            cur_cond_name = self.all_condition_names[cur_cond_ind]

            transitions_list: list[dict] = []
            for cond in conds:
                transitions_list.append(self.nka.nka_transitions[cond].cond_transition)

            all_transitions_dict = merge_dicts(transitions_list)
            # print(all_transitions_dict)
            all_transitions_dict = delete_duplicates_in_dict_vals(all_transitions_dict)
            # print(all_transitions_dict)
            for symb in self.alphabet:
                transitions: tuple = tuple(all_transitions_dict[symb])
                # print(symb, transitions)
                if len(transitions) != 0:
                    if transitions not in self.all_condition_tuples:
                        self.all_condition_tuples.append(transitions)
                        conditions_queue.append(transitions)
                        cond_name: str = DKA.get_unique_cond_name()
                        self.all_condition_names.append(cond_name)
                        self.dka_table.loc[cond_name] = self.empty_row
                        # print('create:', symb, cur_cond_name, cond_name)
                        self.dka_table[symb].loc[cur_cond_name] = cond_name
                    else:
                        cond_ind = self.all_condition_tuples.index(transitions)
                        cond_name: str = self.all_condition_names[cond_ind]
                        # print('connect:', symb, cur_cond_name, cond_name)
                        self.dka_table[symb].loc[cur_cond_name] = cond_name
            # print(self)
            # print()

    def find_final_conds(self):
        for ind, conds in enumerate(self.all_condition_tuples):
            if len(set(conds) & set(self.nka.final_conds_ids)) != 0:
                self.final_conds.append(self.all_condition_names[ind])

    def check_chain(self, chain) -> tuple[str, list[tuple[str, str]]]:
        chain_check_lst: list[tuple[str, str]] = []

        current_cond = 'q0'
        for ind, symb in enumerate(chain):
            chain_check_lst.append((current_cond, chain[ind:]))
            if symb not in self.alphabet:
                return f'В цепочке присутствует посторонний символ: {symb}', chain_check_lst
            next_cond: str = self.dka_table[symb].loc[current_cond]
            if next_cond == '_':
                return f'Не допустисый переход: {current_cond} {symb} → {next_cond}', chain_check_lst
            current_cond = next_cond
        chain_check_lst.append((current_cond, ''))
        if chain_check_lst[-1][0] not in self.final_conds:
            return f'Состояние {chain_check_lst[-1][0]} не соответствует финальному состоянию', chain_check_lst
        return 'Проверка прошла успешно', chain_check_lst

    @staticmethod
    def get_unique_cond_name() -> str:
        DKA.last_cond_id += 1
        return 'q' + str(DKA.last_cond_id)
