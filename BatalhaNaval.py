from os import system
from random import randint
from time import sleep
from typing import List, Tuple


def criar_tabuleiro() -> List[List[str]]:
    return [[' ~ ' for _ in range(10)] for _ in range(10)]


def mostrar_tabuleiro(tabuleiro: List[List[str]]) -> None:
    for i, linha in enumerate(tabuleiro):
        print(i, *linha)


def ver_input(msg: str = '', minimo: int = 0, maximo: int = 9, letra: bool = False) -> int:
    while True:
        try:
            if not letra:
                num = int(input(msg))
                if minimo <= num <= maximo:
                    return num
                print(f'Insira um número entre {minimo} e {maximo}.')
            else:
                letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                letra_input = input(msg).upper()
                if letra_input in letras:
                    return letras.index(letra_input)
        except ValueError:
            print('Insira uma opção válida.')


def titulo(msg: str, abc: bool = True) -> None:
    print(f'=*' * 20, '\n', 'BATALHA NAVAL'.center(38))
    print('*=' * 20)
    print(f'<{msg}>'.center(40))
    if abc:
        print('A - B - C - D - E - F - G - H - I - J'.center(43))


def atualizar_tela(tabuleiro_atk: List[List[str]], tabuleiro_def: List[List[str]]) -> None:
    system('cls')
    titulo('GRELHA DE ATAQUE')
    mostrar_tabuleiro(tabuleiro_atk)
    print('<GRELHA DE DEFESA>'.center(40))
    print('A - B - C - D - E - F - G - H - I - J'.center(43))
    mostrar_tabuleiro(tabuleiro_def)


def posicionar_barcos(tabuleiro: List[List[str]], jogador: str = 'Computador') -> None:
    tamanhos_barcos = [5, 4, 3, 2, 1]

    for barco in tamanhos_barcos:
        colocado = False
        while not colocado:
            pos, linha, coluna = definir_posicao_inicial(jogador, tabuleiro, barco)
            if pos == 0:  # Horizontal
                colocado = tentar_colocar_horizontal(tabuleiro, linha, coluna, barco)
            else:  # Vertical
                colocado = tentar_colocar_vertical(tabuleiro, linha, coluna, barco)


def definir_posicao_inicial(jogador: str, tabuleiro: List[List[str]], barco: int) -> Tuple[int, int, int]:
    if jogador == 'Computador':
        pos = randint(0, 1)
        linha = randint(0, 9)
        coluna = randint(0, 9)
    else:
        system('cls')
        titulo('GRELHA DE DEFESA')
        mostrar_tabuleiro(tabuleiro)
        print('TAMANHO DOS BARCOS: ', *[5, 4, 3, 2, 1])
        print('<POSICIONAMENTO DOS BARCOS>\n')
        pos = ver_input('HORIZONTAL [0] - VERTICAL [1]: ', 0, 1)
        coluna = ver_input('ESCOLHA A LETRA: ', letra=True)
        linha = ver_input('ESCOLHA O NÚMERO: ')
    return pos, linha, coluna


def tentar_colocar_horizontal(tabuleiro: List[List[str]], linha: int, coluna: int, barco: int) -> bool:
    if coluna + barco <= 10 and all(tabuleiro[linha][coluna + i] == ' ~ ' for i in range(barco)):
        for i in range(barco):
            tabuleiro[linha][coluna + i] = ' = '
        return True
    return False


def tentar_colocar_vertical(tabuleiro: List[List[str]], linha: int, coluna: int, barco: int) -> bool:
    if linha + barco <= 10 and all(tabuleiro[linha + i][coluna] == ' ~ ' for i in range(barco)):
        for i in range(barco):
            tabuleiro[linha + i][coluna] = ' = '
        return True
    return False


def ataque(tabuleiro_atk: List[List[str]], tabuleiro_def: List[List[str]], tabuleiro_pc: List[List[str]]) -> None:
    vencedor = {'Jogador': False, 'Computador': False}
    historico = []
    rodada = 0

    while not vencedor['Jogador'] and not vencedor['Computador']:
        vencedor['Jogador'] = jogador_ataca(tabuleiro_atk, tabuleiro_pc)
        if vencedor['Jogador']:
            break
        vencedor['Computador'] = computador_ataca(tabuleiro_def, historico)

        rodada += 1

    mostrar_resultado(vencedor)


def jogador_ataca(tabuleiro_atk: List[List[str]], tabuleiro_pc: List[List[str]]) -> bool:
    atualizar_tela(tabuleiro_atk, tabuleiro_pc)
    print('Escolha onde atacar:')
    coluna = ver_input('ESCOLHA A LETRA: ', letra=True)
    linha = ver_input('ESCOLHA O NÚMERO: ')

    if tabuleiro_pc[linha][coluna] == ' = ':
        tabuleiro_atk[linha][coluna] = ' X '
        tabuleiro_pc[linha][coluna] = ' ~ '
    else:
        tabuleiro_atk[linha][coluna] = ' O '

    return not any(' = ' in linha for linha in tabuleiro_pc)


def computador_ataca(tabuleiro_def: List[List[str]], historico: List[Tuple[int, int]]) -> bool:
    while True:
        linha, coluna = randint(0, 9), randint(0, 9)
        if (linha, coluna) not in historico:
            historico.append((linha, coluna))
            break

    if tabuleiro_def[linha][coluna] == ' = ':
        tabuleiro_def[linha][coluna] = ' X '
    else:
        tabuleiro_def[linha][coluna] = ' O '

    return not any(' = ' in linha for linha in tabuleiro_def)


def mostrar_resultado(vencedor: dict) -> None:
    print('Temos um vencedor!')
    sleep(3)
    if vencedor['Jogador'] and vencedor['Computador']:
        print('O JOGO EMPATOU!')
    elif vencedor['Computador']:
        print('O COMPUTADOR VENCEU!')
    else:
        print('PARABÉNS, VOCÊ GANHOU!')


def jogo() -> None:
    while True:
        system('cls')
        titulo('DIGITE: "JOGAR" ou "SAIR"', abc=False)
        opcao = input('</> ').upper()

        if opcao == 'JOGAR':
            print('Carregando...')
            sleep(2.5)

            tabuleiro_ia = criar_tabuleiro()
            posicionar_barcos(tabuleiro_ia, 'Computador')

            tabuleiro_atk = criar_tabuleiro()
            tabuleiro_def = criar_tabuleiro()
            posicionar_barcos(tabuleiro_def, 'Jogador')

            ataque(tabuleiro_atk, tabuleiro_def, tabuleiro_ia)

        elif opcao == 'SAIR':
            system('cls')
            print('Saindo...')
            sleep(1.5)
            break


if __name__ == "__main__":
    jogo()
