from NKA import *
from DKA import *


def main():
    regular: str = 'c+(b(d+e)c+a)*ba(a+c+d)*a(c+b)bc+a'
    # regular: str = '(ab+b)*abab(a+c)*ab'
    alphabet = ['a', 'b', 'c', 'd', 'e']
    # regular: str = 'a(e+a(b+c)*)e'
    reg: RegularExpression = RegularExpression()
    reg.set_regular(regular, alphabet)
    samples = reg.generate_samples((0, 10), 10)
    print(samples)
    nka: NKA = NKA()
    nka.init_nka(reg, alphabet)
    dka: DKA = DKA()
    dka.init_dka(nka)
    print(dka)

    # samples.append('badaabb')
    # for sample in samples:
    #     chain_info = dka.check_chain(sample)
    #     for item in chain_info[1]:
    #         print(item)
    #     print(chain_info[0])
    #     print()






if __name__ == "__main__":
    main()
