from ConvertingRegularToDka import *
from NKA import *
from DKA import *


def main():
    # regular: str = 'c+(b(d+e)c+a)*ba(a+c+d)*a(c+b)bc+a'
    regular: str = '(ab+b)*abab(a+c)*ab'
    # regular: str = 'a(e+a(b+c)*)e'
    reg: RegularExpression = RegularExpression(regular)
    nka: NKA = NKA(reg, ['a', 'b', 'c', 'd', 'e'])
    # print(nka)
    dka: DKA = DKA(nka)
    print(dka)



if __name__ == "__main__":
    main()
