from itertools import cycle
import operator

with open('entrada.txt', 'r') as entrada:
    global paginas, processos, pos_processos
    paginas = int(entrada.readline())
    processos = [int(num) for num in entrada]
    pos_processos = {k: 0 for k in processos}
    global ciclo
    ciclo = cycle([i for i in range(paginas)])

#print(paginas)
#print(pos_processos)

# for i, j in enumerate(ciclo):
#     if i == paginas:
#         break
#     print(j)

# print(processos, '\n')

def FIFO(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:4]):
        quadros[i] = processo
        falta_de_quadros += 1
    
    for i, processo_atual in enumerate(processos[4:]):
        if processo_atual in quadros:
            continue
        quadro = next(ciclo)
        quadros[quadro] = processo_atual
        falta_de_quadros += 1
    
    print(f'FIFO {falta_de_quadros}')

def CicloOtimo(num):
    if num + 1 == 4:
        return 0
    return num + 1

def PegarProcesso(posicoes, processos, pagina):
    max = 0
    lista = []
    for proc in posicoes:
        if posicoes[proc] == 0 and proc in pagina:
            lista.append([proc, 0])
            #print('Lista: {}'.format(lista))
        if posicoes[proc] > max:
            max = posicoes[proc]
            p = (proc, posicoes[proc] - 1)
    
    if len(lista) > 1:
        #print(f'Mais de um processo com 0, numero de processos com 0: {len(lista)}')
        for pr in processos[::-1]:
            count = 0
            for i in lista:
                if i[1]:
                    count += 1
                                                #essa checagem de uns na lista serve para não ter que percorrer todos os processos anteriores se todos os processos
            if count == len(lista):             #necessarios ja foram encontrados
                #print('Finalizou')
                break

            if [pr, 0] in lista:
                p = (pr, posicoes[pr])
                lista[lista.index([pr, 0])][1] = 1
                #print('Processo pego: {} --- Lista atual: {}'.format(p, lista))

    elif len(lista) == 1:
        p = (lista[0], posicoes[lista[0]])
        
    return p


def Otimo(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:4]):
        quadros[i] = processo
        falta_de_quadros += 1
        #print('Quadros: {}\nFalta de quadros: {}\n'.format(quadros, falta_de_quadros))
    
    for i, processo_atual in enumerate(processos[4:]):
        #print('\nTodos os processos futuros: {} --- Processo atual: {}, sua posicao: {}'.format(processos[i + 5:], processo_atual, i + 4))
        if processo_atual in quadros:
            continue
        pos_processos = {k: 0 for k in processos}
        for pos, processo_futuro in enumerate(processos[i + 5:]):
            if processo_futuro != processo_atual and pos_processos[processo_futuro] <= 0:
                pos_processos[processo_futuro] = pos + 1
                #print('Processo futuro: {} --- Posicao: {}'.format(processo_futuro, pos_processos[processo_futuro]))
                
            
        #print('Quadros antes: {} --- Processos e suas posicoes mais proximas: {}'.format(quadros, pos_processos))
        quadro_subst = PegarProcesso(pos_processos, processos[:i + 4], quadros)
        quadros[quadros.index(int(quadro_subst[0]))] = processo_atual

        #print('Quadros: {} --- Quadro que foi substituido: {}\n'.format(quadros, quadro_subst))
        falta_de_quadros += 1

    print(f'OTM {falta_de_quadros}')

def LRU(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:4]):
        quadros[i] = processo
        falta_de_quadros += 1
    
    for i, processo_atual in enumerate(processos[4:], start = 4):
        if processo_atual in quadros:
            continue
        
        pos_processos = {}
        #print(f'Processos passados: {processos[:i]} --- Processo atual: {processo_atual} --- Quadros: {quadros}')
        for index, processo_passado in enumerate(processos[:i]):
            #print(f'Processo passado: {processo_passado}')
            if processo_passado in quadros:
                pos_processos[processo_passado] = index
        
        quadro_subst = min(pos_processos, key=pos_processos.get)
        #print(f'Processo {quadro_subst} foi substituido por {processo_atual}')
        quadros[quadros.index(quadro_subst)] = processo_atual
        #print(f'Quadro agora: {quadros}')

        falta_de_quadros += 1

    print(f'LRU {falta_de_quadros}')      


FIFO(paginas, processos)
Otimo(paginas, processos)
LRU(paginas, processos)