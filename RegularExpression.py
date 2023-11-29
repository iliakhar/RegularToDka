
class RegularExpression:
    def __init__(self, regular=''):
        self.bracket_types: dict[str:tuple[str, str]] = {'round': ('(', ')'), 'square': ('[', ']'), 'mix': ('([', ')]')}
        self.regular: str = regular
        self.split_regular: list[str] = []
        self.reform_cycles()

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

    def split_line_by_inds(self, line: str, inds: list[int]):
        return [line[inds[i]+1:inds[i + 1]] for i in range(len(inds) - 1)]

    def separate_by_plus(self, reg_part: str,  brackets_inds: list[tuple[int, int]]) -> list[str]:
        reg_part_copy: str = reg_part[:]
        for item in brackets_inds:
            symbs_for_overwriting = '^'*(item[1]-item[0]+1)
            reg_part_copy = reg_part_copy[0:item[0]]+symbs_for_overwriting+reg_part_copy[item[1]+1:]
        inds_to_separate: list[int] = [-1] + [ind for ind, symb in enumerate(reg_part_copy) if symb == '+'] + [None]
        separated_regular = self.split_line_by_inds(reg_part, inds_to_separate)
        return separated_regular

