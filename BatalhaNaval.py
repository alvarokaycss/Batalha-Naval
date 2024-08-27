from os import system
from random import randint
from time import sleep

def criar_tabuleiro():
    return [[' ~ ' for _ in range(10)] for _ in range(10)]

def mostrar_tabuleiro(tabuleiro):
    for i,linha in enumerate(tabuleiro):
        print(i,*linha)

def ver_input(msg='',minimo=0,maximo=9,letra=False):
    while True:
        try:
            if not letra: 
                num = int(input(msg))
                if minimo <= num <= maximo:
                    return num
                else:
                    print(f'Inserir número entre {minimo} e {maximo}.')
            else:
                letras = ['A','B','C','D','E','F','G','H','I','J']
                letra = input(msg).upper()
                if letra in letras:
                    for pos, let in enumerate(letras):
                        if letra == let:
                            return pos
        except ValueError:
            print('Inserir opção válida.')

def titulo(msg,abc=True):
    print(f'=*'*20,'\n','BATALHA NAVAL'.center(38))
    print('*='*20)
    print()
    print(f'<{msg}>'.center(40))
    if abc == True:
        print('A - B - C - D - E - F - G - H - I - J'.center(43))

def atualizar_tela(tabuleiro_atk,tabuleiro_def):
    
    system('cls')
    titulo('GRELHA DE ATAQUE')
    mostrar_tabuleiro(tabuleiro_atk)
    print('<GRELHA DE DEFESA>'.center(40))
    print('A - B - C - D - E - F - G - H - I - J'.center(43))
    mostrar_tabuleiro(tabuleiro_def)
    
def posicionar_barcos(tabuleiro,barcos='Computador'):
    tamanho_barcos = [5, 4, 3, 2, 1]

    for barco in tamanho_barcos:
        colocado = False
        
        while not colocado:
            caracter = ['~','=']
            
            if barcos == 'Computador':
                
                pos = randint(0, 1)
                linha = randint(0, 9)
                coluna = randint(0, 9)
                
            elif barcos == 'Jogador':
                
                system('cls')
                titulo('GRELHA DE DEFESA')
                mostrar_tabuleiro(tabuleiro)
                print('TAMANHO DOS BARCOS: '.center(26),*tamanho_barcos)
                print('<POSICIONAMENTO DOS BARCOS>\n'.center(40))   
                pos = ver_input('HORIZONTAL [0] - VERTICAL [1]: ',0,1)
                coluna = ver_input('ESCOLHA A LETRA: ', letra=True)
                linha = ver_input('ESCOLHA O NÚMERO: ')
                
            # VARIÁVEL DE VERIFICAÇÃO DA POSIÇÃO
            ocupado = False
            
            if pos == 0:  # POSIÇÃO HORIZONTAL
                if coluna + barco <= 10:
                    for parte in range(barco):
                        if tabuleiro[linha][coluna + parte] != f' {caracter[0]} ':
                            ocupado = True
                            break
                        
                    if not ocupado:
                        for parte in range(barco):
                            tabuleiro[linha][coluna + parte] = f' {caracter[1]} '
                        colocado = True
                            
            else:  # POSIÇÃO VERTICAL
                if linha + barco <= 10:
                    for parte in range(barco):
                        if tabuleiro[linha + parte][coluna] != f' {caracter[0]} ':
                            ocupado = True
                            break
                        
                    if not ocupado:
                        for parte in range(barco):
                            tabuleiro[linha + parte][coluna] = f' {caracter[1]} '
                        colocado = True
                        
def ataque(tabuleiro_atk,tabuleiro_def,tabuleiro_pc):
    
    vencedor = {'Jogador':False,'Computador':False}
    historico = []
    rodada = 0
    caracter = ['~','=']
    
    while not vencedor['Jogador'] and not vencedor['Computador']:
        
        # ATAQUE DO JOGADOR
        atualizar_tela(tabuleiro_atk,tabuleiro_def)
        print(f'{rodada+1}° Rodada - Escolha onde atacar:')
        coluna = ver_input('ESCOLHA A LETRA: ',letra=True)
        linha = ver_input('ESCOLHA O NÚMERO: ')
        atualizar_tela(tabuleiro_atk,tabuleiro_def)
        
        if tabuleiro_pc[linha][coluna] == f' {caracter[1]} ':
            tabuleiro_atk[linha][coluna] = ' X '
            tabuleiro_pc[linha][coluna] = f' {caracter[0]} '
        else:
            tabuleiro_atk[linha][coluna] = ' O '
        
        print('Atacando...')
        sleep(1.5)
        atualizar_tela(tabuleiro_atk,tabuleiro_def)

        
        # CONDIÇÃO DE PARADA (Jogador)
        vencedor['Jogador']= True
        for lista in tabuleiro_pc:
            for item in lista:
                if item == f' {caracter[1]} ':
                    vencedor['Jogador'] = False
                    break
            if not vencedor['Jogador']:
                break
        
        # ATAQUE DO COMPUTADOR                                                                    
        while True:
            linha = randint(0, 9)
            coluna = randint(0, 9)
            pos = (linha,coluna)
            if pos not in historico:
                historico.append(pos)
                break
        
        print('Oponente atacando...')
        sleep(1.5)
        
        if tabuleiro_def[linha][coluna] == f' {caracter[1]} ':
            tabuleiro_def[linha][coluna] = ' X '
        else:
            tabuleiro_def[linha][coluna] = ' O '
        
        atualizar_tela(tabuleiro_atk,tabuleiro_def)
        
        # CONDIÇÃO DE PARADA (Computador)
        vencedor['Computador'] = True
        for lista_tab in tabuleiro_def:
            for item in lista_tab:
                if item == f' {caracter[1]} ':
                    vencedor['Computador'] = False
                    break
            if not vencedor['Computador']:
                break
            
        rodada += 1
        
    print('Temos um vencedor..!')
    sleep(3)
    if vencedor['Jogador'] == True and vencedor['Computador'] == True:
        print('O JOGO EMPATOU!!')
        sleep(1.5)
    elif vencedor['Computador'] == True:
        print('O COMPUTADOR VENCEU!!')
        sleep(1.5)
    else:
        print('PARABÉNS VOCÊ GANHOU!!')
        sleep(1.5)
                                                                 
def jogo():
    
    while True:
        system('cls')
        titulo('DIGITE: "JOGAR" ou "SAIR"', abc=False)
        print('</',end='> ')
        menu = input().upper()
        
        if menu == 'JOGAR':
            print('Carregando...')
            sleep(2.5)
            # FASE: TABULEIRO E POSIÇÃO DOS BARCOS DA IA
            tabuleiro_IA = criar_tabuleiro()
            posicionar_barcos(tabuleiro_IA,'Computador')
            
            # FASE: TABULEIROS JOGADOR E POSIÇÃO DOS BARCOS JOGADOR
            tabuleiro_ATK = criar_tabuleiro()
            tabuleiro_DEF = criar_tabuleiro()
            posicionar_barcos(tabuleiro_DEF,'Jogador')

            #FASE: BATALHA NAVAL
            ataque(tabuleiro_ATK,tabuleiro_DEF,tabuleiro_IA)
            atualizar_tela(tabuleiro_ATK,tabuleiro_DEF)
            
        elif menu == 'SAIR':
            system('cls')
            print('Saindo...')
            sleep(1.5)
            break
        
jogo()
