import random
import time


class RegularExpression:
    def __init__(self):
        self.bracket_types: dict[str:tuple[str, str]] = {'round': ('(', ')'), 'square': ('[', ']'), 'mix': ('([', ')]')}
        self.regular: str = ''
        self.alphabet: list[str] = []
        self.split_regular: list[str] = []

        self.max_cycle_repeats: int = 30
        self.step_repeats_changed = 4
        self.sample_length_range: tuple[int, int] = (-1, -1)

    def set_regular(self,  regular='', alphabet: list[str] = ''):
        self.regular = regular
        self.alphabet = alphabet
        format_error: str = self.check_regular_format()
        if format_error == '':
            self.reform_cycles()
        else:
            self.regular = ''
            self.alphabet = []
        return format_error

    def check_bracket_count(self, regular: str) -> bool:
        bracket_count: int = 0
        for symb in regular:
            if symb == '(':
                bracket_count += 1
            elif symb == ')':
                bracket_count -= 1
                if bracket_count < 0:
                    return False
        return bracket_count == 0

    def reform_cycles(self):
        regular_reverse = self.regular[::-1]
        for i, symb in enumerate(regular_reverse):
            if symb == '*':
                end: int = len(regular_reverse)-i - 1
                bracket_count = 0
                for j, symb in enumerate(regular_reverse[i:]):
                    if symb == ')':
                        bracket_count += 1
                    elif symb == '(':
                        bracket_count -= 1
                        if bracket_count == 0:
                            start = len(regular_reverse) - j - 1 - i
                            self.regular = self.regular[:start]+'['+self.regular[start+1:end-1]+']'+self.regular[end+1:]
                            break

    def find_outer_brackets(self, regular_part: str, bracket_type: str = 'mix') -> list[tuple[int, int]]:
        brackets: tuple[str, str] = self.bracket_types[bracket_type]
        bracket_count: int = 0
        brackets_inds: list[tuple[int, int]] = []
        start_bracket: int = -1
        for ind, symb in enumerate(regular_part):
            if symb in brackets[0]:
                if bracket_count == 0:
                    start_bracket = ind
                bracket_count += 1
            elif symb in brackets[1]:
                bracket_count -= 1
                if bracket_count == 0:
                    brackets_inds.append((start_bracket, ind))
        return brackets_inds

    def find_closed_bracket(self, regular_part: str, open_bracket_ind: int, bracket_type: str = 'mix') -> int:
        brackets: tuple[str, str] = self.bracket_types[bracket_type]
        bracket_count: int = 0
        for ind, symb in enumerate(regular_part[open_bracket_ind:]):
            if symb in brackets[0]:
                bracket_count += 1
            elif symb in brackets[1]:
                bracket_count -= 1
                if bracket_count == 0:
                    return open_bracket_ind + ind
        return -1

    def separate_by_plus(self, reg_part: str,  brackets_inds: list[tuple[int, int]]) -> list[str]:
        reg_part_copy: str = reg_part[:]
        for item in brackets_inds:
            symbs_for_overwriting = '^'*(item[1]-item[0]+1)
            reg_part_copy = reg_part_copy[0:item[0]]+symbs_for_overwriting+reg_part_copy[item[1]+1:]
        inds_to_separate: list[int] = [-1] + [ind for ind, symb in enumerate(reg_part_copy) if symb == '+'] + [None]
        separated_regular = self.split_line_by_inds(reg_part, inds_to_separate)
        return separated_regular



    def generate_samples(self, length_range: tuple[int, int], number_of_list: int, max_time_sec: int = 5) -> list[str]:
        samples: list[str] = []
        start_time: float = time.perf_counter()
        self.sample_length_range = length_range
        while len(samples) < number_of_list:
            sample: str = self.choice_action(self.regular)
            # print(sample, len(samples), self.max_cycle_repeats)
            if (sample not in samples) and (length_range[0] < len(sample) < length_range[1]):
                samples.append(sample)
            if time.perf_counter() - start_time > max_time_sec:
                break
        print()
        return samples

    def perform_act(self, sub_reg: str) -> str:
        cur_symb_ind: int = 0
        sub_sample: str = ''
        while True:
            if cur_symb_ind >= len(sub_reg):
                break

            if sub_reg[cur_symb_ind] in self.alphabet:
                sub_sample += sub_reg[cur_symb_ind]
                cur_symb_ind += 1
                continue

            if sub_reg[cur_symb_ind] == '(':
                closed_bracket_ind: int = self.find_closed_bracket(sub_reg, cur_symb_ind, 'round')
                sub_sample += self.choice_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                cur_symb_ind = closed_bracket_ind + 1
                continue

            if sub_reg[cur_symb_ind] == '[':
                closed_bracket_ind: int = self.find_closed_bracket(sub_reg, cur_symb_ind, 'square')
                sub_sample += self.cycle_action(sub_reg[cur_symb_ind+1:closed_bracket_ind])
                cur_symb_ind = closed_bracket_ind + 1
                continue

        return sub_sample

    def get_number_of_split(self, sub_reg: str) -> int:
        brackets_inds: list[tuple[int, int]] = self.find_outer_brackets(sub_reg)
        separated_regular: list[str] = self.separate_by_plus(sub_reg, brackets_inds)
        return len(separated_regular)

    def choice_action(self, sub_reg: str) -> str:
        brackets_inds: list[tuple[int, int]] = self.find_outer_brackets(sub_reg)
        separated_regular: list[str] = self.separate_by_plus(sub_reg, brackets_inds)
        sub_sample: str = ''
        choosen_part_ind: int = random.randint(0, len(separated_regular)-1)
        sub_sample += self.perform_act(separated_regular[choosen_part_ind])
        return sub_sample

    def cycle_action(self, sub_reg: str) -> str:
        cycle_repeat = random.randint(0, self.max_cycle_repeats)
        sub_sample: str = ''
        # print(cycle_repeat, end=': ')
        for _ in range(cycle_repeat):
            sub_sample += self.choice_action(sub_reg)
            # print(sub_sample, end=', ')
        # print()
        return sub_sample

    def check_regular_format(self) -> str:
        if ('++' in self.regular) or ('+)' in self.regular) or (self.regular[0] == '+') or (self.regular[-1] == '+'):
            return 'Недопустимоe использование +'
        if '()' in self.regular:
            return 'Недопустимоe использовать пустые скобки'
        if not self.check_bracket_count(self.regular):
            return "Кол-во '(' не соответствует кол-ву ')'"

        accepted_symbs: str = '()*+'
        for ind, symb in enumerate(self.regular):
            if (symb not in self.alphabet) and (symb not in accepted_symbs):
                return f"Символа '{symb}' нет в алфавите"
            if symb == '*':
                if ind == 0:
                    return f"Недопустимое использование '*'"
                if self.regular[ind-1] != ')':
                    return f"Недопустимое использование '*'"
        return ''

    @staticmethod
    def split_line_by_inds(line: str, inds: list[int]):
        return [line[inds[i]+1:inds[i + 1]] for i in range(len(inds) - 1)]
