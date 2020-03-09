from itertools import cycle
import operator

with open('entrada.txt', 'r') as entrada:
    global paginas, processos, pos_processos
    paginas = int(entrada.readline())
    processos = [int(num) for num in entrada]
    pos_processos = {k: 0 for k in processos}
    global ciclo
    ciclo = cycle([i for i in range(paginas)])


def FIFO(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:num_quadros]):
        quadros[i] = processo
        falta_de_quadros += 1

    for i, processo_atual in enumerate(processos[num_quadros:]):
        if processo_atual in quadros:
            continue
        quadro = next(ciclo)
        quadros[quadro] = processo_atual
        falta_de_quadros += 1

    print(f'FIFO {falta_de_quadros}')


# Função que retorna o processo que deve ser substituido no Ótimo
def PegarProcesso(posicoes, processos, pagina):
    max = 0
    lista = []
    p = (None, None)
    for proc in posicoes:
        if proc in pagina:
            if posicoes[proc] == 0 and proc in pagina:
                lista.append([proc, 0])
            if posicoes[proc] > max:
                max = posicoes[proc]
                p = (proc, posicoes[proc] - 1)

    if len(lista) > 1:
        for pr in processos[::-1]:
            count = 0
            for i in lista:
                if i[1]:
                    count += 1
                    # essa checagem de uns na lista serve para não ter que percorrer todos os processos anteriores se todos os processos
            if count == len(lista):  # necessarios ja foram encontrados
                break

            if [pr, 0] in lista:
                p = (pr, posicoes[pr])
                lista[lista.index([pr, 0])][1] = 1

    elif len(lista) == 1:
        p = (lista[0][0], posicoes[lista[0][0]])

    return p


def Otimo(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:num_quadros]):
        quadros[i] = processo
        falta_de_quadros += 1

    for i, processo_atual in enumerate(processos[num_quadros:]):
        if processo_atual in quadros:
            continue
        pos_processos = {k: 0 for k in processos}
        for pos, processo_futuro in enumerate(processos[i + num_quadros + 1:]):
            if processo_futuro != processo_atual and pos_processos[processo_futuro] <= 0:
                pos_processos[processo_futuro] = pos + 1

        quadro_subst = PegarProcesso(
            pos_processos, processos[:i + num_quadros], quadros)
        quadros[quadros.index(int(quadro_subst[0]))] = processo_atual

        falta_de_quadros += 1

    print(f'OTM {falta_de_quadros}')


def LRU(num_quadros, processos):
    quadros = [0]*num_quadros
    falta_de_quadros = 0
    for i, processo in enumerate(processos[:num_quadros]):
        quadros[i] = processo
        falta_de_quadros += 1

    for i, processo_atual in enumerate(processos[num_quadros:], start=num_quadros):
        if processo_atual in quadros:
            continue

        pos_processos = {}
        for index, processo_passado in enumerate(processos[:i]):
            if processo_passado in quadros:
                pos_processos[processo_passado] = index

        quadro_subst = min(pos_processos, key=pos_processos.get)
        quadros[quadros.index(quadro_subst)] = processo_atual

        falta_de_quadros += 1

    print(f'LRU {falta_de_quadros}')


FIFO(paginas, processos)
Otimo(paginas, processos)
LRU(paginas, processos)
