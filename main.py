from colorama import init, Fore
from math import pi, sqrt

init()

# Constants
tau_str = u'\u03c4'
delta_str = u'\u0394'
betta_str = u'\u03b2'
decrement_str = u'\u1e9f'
console_input = False


def dump_result(R: float, d_R: float, T: float, d_T: float,
                betta: float, d_betta: float, T0: float, d_T0: float,
                decrement: float,Q: float,
                L: float, d_L: float, C: float, d_C: float,
                filename: str):
    file_res = f'R[Om] = {R}\n' \
               f'{delta_str}R[Om] = {d_R}\n\n' \
               f'T[mks] = {T*10**6}\n' \
               f'{delta_str}T[mks] = {d_T*10**6}\n\n' \
               f'{betta_str}[MHz] = {betta*10**-6}\n' \
               f'{delta_str}{betta_str}[MHz] = {d_betta*10**-6}\n\n' \
               f'T0[mks] = {T0*10**6}\n' \
               f'{delta_str}T0[mks] = {d_T0*10**6}\n\n' \
               f'{decrement_str} = {decrement}\n\n' \
               f'Q = {Q}\n\n' \
               f'L[mGn] = {L*10**3}\n' \
               f'{delta_str}L[mGn] = {d_L*10**3}\n\n' \
               f'C[nF] = {C*10**9}\n' \
               f'{delta_str}C[nF] = {d_C*10**9}\n\n'

    cons_res = f'{Fore.GREEN}R[Om] = {Fore.CYAN}{R*10**3}\n' \
               f'{Fore.GREEN}{delta_str}R[Om] = {Fore.CYAN}{d_R*10**3}\n\n' \
               f'{Fore.GREEN}T[mks] = {Fore.CYAN}{T*10**6}\n' \
               f'{Fore.GREEN}{delta_str}T[mks] = {Fore.CYAN}{d_T*10**6}\n\n' \
               f'{Fore.GREEN}{betta_str}[Hz] = {Fore.CYAN}{betta}\n' \
               f'{Fore.GREEN}{delta_str}{betta_str}[Hz] = {Fore.CYAN}{d_betta}\n\n' \
               f'{Fore.GREEN}{decrement_str} = {Fore.CYAN}{decrement}\n\n' \
               f'{Fore.GREEN}Q = {Fore.CYAN}{Q}\n\n' \
               f'{Fore.GREEN}L[Gn] = {Fore.CYAN}{L}\n' \
               f'{Fore.GREEN}{delta_str}L[Gn] = {Fore.CYAN}{d_L}\n\n' \
               f'{Fore.GREEN}C[F] = {Fore.CYAN}{C}\n' \
               f'{Fore.GREEN}{delta_str}C[f] = {Fore.CYAN}{d_C}\n\n'

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(file_res)


def secure_input(name: str, units: str) -> float:
    isBadInput = True
    tmp = 0.0
    while isBadInput:
        try:
            tmp = input(f"{Fore.GREEN}{name}[{units}] = {Fore.WHITE}")
            if units[:2] == 'mk':
                tmp = float(tmp) / (10 ** 6)
            elif units[:1] == 'm' and len(units) != 1:
                tmp = float(tmp) / (10 ** 3)
            else:
                tmp = float(tmp)
            isBadInput = False
        except ValueError:
            print(f"{Fore.RED}Ошибка ввода. Попробуйте снова\n")
    return tmp


def get_d_t0(T_: float, delta_T: float, betta_: float, delta_betta: float) -> float:
    first = 8 * (pi ** 3) * delta_T
    second = (4 * pi * pi / (T_ * T_) + betta_ * betta_) ** 1.5 * T_**3
    third = 2 * pi * delta_betta
    fourth = (betta_ * betta_ + 4 * pi * pi / (T_ * T_)) ** 1.5
    tmp = (first / second) ** 2 + (third / fourth) ** 2
    return sqrt(tmp)


def get_d_l(R: float, d_R: float, betta: float, d_betta: float) -> float:
    first = d_R / (2 * betta)
    second = d_betta * R / (2 * betta * betta)
    return sqrt(first * first + second * second)


def get_d_c(T0: float, d_T0: float, L: float, d_L: float) -> float:
    first = ((d_T0 * T0) / (2 * pi * pi * L)) ** 2
    second = (d_L * T0 * T0 / (4 * pi * pi * L * L)) ** 2
    return sqrt(first + second)


def main():
    if console_input:
        T = secure_input('T', 'mks')
        d_T = secure_input(f'{delta_str}T', 'mks')
        tau = secure_input(tau_str, 'mks')
        d_tau = secure_input(f'{delta_str}{tau_str}', 'mks')
        A1 = secure_input('A1', 'mV')
        d_A1 = secure_input(f'{delta_str}A1', 'mv')
        A2 = secure_input('A2', 'mV')
        d_A2 = secure_input(f'{delta_str}A2', 'mv')
        Ne = secure_input('Ne', '-')
        R = secure_input('R', 'Om')
        d_R = secure_input(f'{delta_str}R', 'Om')
    else:
        T = 2.825*10**-6
        d_T = 0.001*10**-6
        tau = 11.3*10**-6
        d_tau = 0.01*10**-6
        A1 = 0.111
        d_A1 = 0.001
        A2 = 0.079
        d_A2 = d_A1
        Ne = 4
        R = 55
        d_R = 3

    betta = 1 / tau
    T0 = 2 * pi / sqrt(4 * pi * pi / (T * T) + betta * betta)
    decrement = 1 / Ne
    Q = pi / decrement
    L = R / (2 * betta)
    C = T0 ** 2 / (4 * pi * pi * L)

    decrement_401_5 = betta * T
    Q_401_8 = 2 * pi * A1/T * A1/T / (A1/T * A1/T - A2/T * A2/T)

    # Погрешности
    d_betta = d_tau / (tau * tau)
    d_T0 = get_d_t0(T, d_T, betta, d_betta)
    d_L = get_d_l(R, d_R, betta, d_betta)
    d_C = get_d_c(T0, d_T0, L, d_L)

    dump_result(R, d_R, T, d_T, betta, d_betta, T0, d_T0, decrement_401_5, Q, L, d_L, C, d_C, 'result.txt')
    print(Q_401_8)
if __name__ == '__main__':
    main()