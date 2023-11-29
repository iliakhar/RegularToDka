from ConvertingRegularToDka import *
from NKA import *

def main():
    regular: str = 'c+(b(d+e)c+a)*ba(a+c+d)*a(c+b)bc+a'
    regular: str = 'a(e+a)b'
    reg: RegularExpression = RegularExpression(regular)
    nka: NKA = NKA(reg, ['a', 'b', 'c', 'd', 'e'])
    print(nka)



if __name__ == "__main__":
    main()
