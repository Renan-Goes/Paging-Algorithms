with open("exemplo.txt", "r") as f:
    processos = [[int(num) for num in i.split(' ')] for i in f]

def FCFS(lista):
    listaSorted = sorted(lista, key = lambda x: x[0])
    numProcessos = len(listaSorted)
    espera = 0
    resposta = 0
    retorno = 0
    tempo = 0

    for i in range(0, len(listaSorted)):
        if i == 0:
            retorno = listaSorted[0][1]
            tempo = retorno
                        
        else:
            espera += tempo - listaSorted[i][0]
            tempo += listaSorted[i][1]
            retorno += tempo - listaSorted[i][0]
            
    print('FCFS', retorno/numProcessos, espera/numProcessos, espera/numProcessos)

def SJF(lista):
    lista.sort()
    filaEspera = []
    numProcessos = len(lista)
    espera = 0
    resposta = 0
    retorno = 0
    count = 0

    while len(lista) > 0:
        tempo = lista[0][0]
        while lista[0][0] == tempo:
            filaEspera.append([lista[0][1], lista[0][0]])
            del lista[0]
            if len(lista) <= 0:
                break
        filaEspera.sort()

        while len(filaEspera) > 0:
            resposta += tempo - filaEspera[0][1]
            retorno += (tempo - filaEspera[0][1]) + filaEspera[0][0]
            tempoAnterior = tempo
            tempo += filaEspera[0][0]
            aux = filaEspera[0][0]
            del filaEspera[0]

            if len(lista) > 0:
                while lista[0][0] <= tempo:
                    filaEspera.append([lista[0][1], lista[0][0]])
                    del lista[0]
                    if len(lista) <= 0:
                        break

            filaEspera.sort()

    print('SJF', retorno/numProcessos, resposta/numProcessos, resposta/numProcessos)

def RR(listaa, quantum):
    lista = sorted(listaa, key = lambda x: x[0])
    filaEspera = list()

    for n in lista:
        n.append(n[0])
        n.append(0)
    numProcessos = len(lista)
    espera = 0
    resposta = 0
    retorno = 0
    count = 0

    while len(lista) > 0:
        tempo = lista[0][0]
        while lista[0][0] == tempo:
            filaEspera.append([lista[0][1], lista[0][0], lista[0][0], 0])
            del lista[0]
            if len(lista) <= 0:
                break

        while len(filaEspera) > 0:
            if filaEspera[0][0] <= quantum:
                tempo += filaEspera[0][0]
                retorno += tempo - filaEspera[0][2]
                espera += filaEspera[0][0]*(len(filaEspera) - 1)
                del filaEspera[0]
                if len(lista) > 0:
                    while lista[0][0] <= tempo:
                        filaEspera.append([lista[0][1], lista[0][0], lista[0][2], 0])
                        del lista[0]
                        if len(lista) <= 0:
                            break

            else:
                if filaEspera[0][3] == 0:
                    resposta += tempo - filaEspera[0][2]
                espera += quantum*(len(filaEspera) - 1)
                tempo += quantum

                if len(lista) > 0:
                    while lista[0][0] <= tempo:
                        filaEspera.append([lista[0][1], lista[0][0], lista[0][2], 0])
                        del lista[0]
                        if len(lista) <= 0:
                            break
                
                processoAtual = filaEspera[0]
                del filaEspera[0]
                filaEspera.append([processoAtual[0] - quantum, tempo, processoAtual[2], 1])

    print('RR ', retorno/numProcessos, resposta/numProcessos, espera/numProcessos)

def SJFComPreempcao(lista):    
    lista.sort()
    for i in range(0, len(lista)):
        lista[i].append(lista[i][0])
    listaSorted = lista.copy()
    numProcessos = len(lista)
    retorno = 0
    espera = 0
    resposta = 0
    processoAtual = listaSorted.pop(0)
    del lista[0]
    tempo = lista[0][0]
    ajuda = 0
    count = 0
    flag = 1

    while (len(lista) > 0):
        for count in range(0, len(lista)):
            if processoAtual[1] + tempo - lista[count][0] > lista[count][1] and processoAtual[1] + tempo - lista[count][0] >= 0:
                tempo += lista[count][0] - processoAtual[0] 
                espera += tempo    
                listaSorted.append([lista[count][0], processoAtual[1] - listaSorted[count][0], processoAtual[2]])
                processoAtual = lista[count]
                listaSorted.remove(lista[count])
                resposta += tempo - processoAtual[2]
                flag = 0
            
            elif processoAtual[1] + tempo - lista[count][0] <= lista[count][1] and processoAtual[1] + tempo - lista[count][0] >= 0:
                listaSorted.append([tempo + processoAtual[1], lista[count][1], lista[count][2]])
                listaSorted.remove(lista[count])

        tempo += processoAtual[1]
        
        espera += processoAtual[1]*len(lista)

        retorno += tempo - processoAtual[2]

        listaSorted.sort(key = lambda x: x[1])

        while  tempo < listaSorted[ajuda][0]:
            ajuda += 1
            
        processoAtual = listaSorted[ajuda]
        del listaSorted[ajuda]

        if processoAtual[0] != tempo:
            flag = 0

        if flag == 1:
            resposta += tempo - processoAtual[2]

        lista = listaSorted.copy()
        ajuda = 0
        flag = 1

    tempo += processoAtual[1]
    retorno += tempo - processoAtual[2]
    print(retorno/numProcessos, resposta/numProcessos, espera/numProcessos)


FCFS(processos[:])
SJF(processos[:])
RR(processos[:], 2)