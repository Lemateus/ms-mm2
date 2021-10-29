from monteCarlo import MonteCarlo
from math import inf
from Distribuicoes import distribuicao
from estatisticas import Est
from NumeroAleatorio import nAleatorio
from Gera_Dados import geraTempo
import heapq as hp
import queue


def simulador(
    estatisticas,
    nClientes: int,
    filaMax: int,
    tecDist: str,
    tecArgs, 
    tsDist: str,
    tsArgs 
) -> None:

    if tecDist!='deterministica':
        dados_tec = geraTempo(tecDist, tecArgs)
        monteCarloTec = MonteCarlo(dados_tec)
        monteCarloTec.geraClasses()
    
    if tsDist!='deterministica':
        dados_ts = geraTempo(tsDist, tsArgs)
        monteCarloTs = MonteCarlo(dados_ts)
        monteCarloTs.geraClasses()

    return executaSimulacao(
        estatisticas,
        nClientes=nClientes,
        filaMax=filaMax,
        proximoTec=lambda: distribuicao('deterministica')(**tecArgs) if(tecDist=='deterministica') else monteCarloTec.geraNumero(),
        proximoTs=lambda: distribuicao('deterministica')(**tsArgs) if(tsDist=='deterministica') else monteCarloTs.geraNumero(),
    )

def executaSimulacao(
    estatisticas,
    nClientes: int,
    filaMax: int,
    proximoTec, # ()->float
    proximoTs, # ()->float
) -> None:

    tr = 0 # tempo atual
    ocupado1 = False # estado do servidor 1
    ocupado2 = False # estado do servidor 2
    tf = 0 # tamanho da fila
    hc = 0 # hora do próximo evento de chegada
    hs = 99999999999 # hora do próximo evento de saída
    tf = 0 # tamanho da fila
    ultimo_evento_fila = 0
    media_pessoas_fila = 0

    hc = tr + proximoTec()

    h_saida = []
    hp.heappush(h_saida, (999999999, 1))

    fila = queue.Queue()
    n_cliente_fila = 0

    idx = 0

    clientes = []

    cliente = 0
    while(cliente<=nClientes):
        if(hc<=h_saida[0][0]):      # próxima chegada acontece antes de próxima saída
            tr = hc
            if(tf<filaMax):
                if not ocupado1 or not ocupado2:
                    if not ocupado1:
                        ocupado1 = True
                        ts = proximoTs()
                        hp.heappush(h_saida, (tr+ts, 1))
                        clientes.append([hc, ts, tr+ts, 1])
                        idx += 1
                    else:
                        ocupado2 = True
                        ts = proximoTs()
                        hp.heappush(h_saida, (tr+ts, 2))
                        clientes.append([hc, ts, tr+ts, 2])
                        idx += 1
                    
                else:
                    media_pessoas_fila += (tr-ultimo_evento_fila)*tf
                    ultimo_evento_fila = tr
                    fila.put(idx)
                    idx += 1
                    tf += 1
                    clientes.append([hc, -1, -1, -1])

            hc = tr + proximoTec()

        else:
            tr = h_saida[0][0]
            aux = h_saida[0][1]
            hp.heappop(h_saida)

            cliente += 1

            if(tf>0):
                tf -= 1
                a = fila.get()
                media_pessoas_fila += (tr-ultimo_evento_fila)*tf
                ultimo_evento_fila = tr
                ts = proximoTs()
                clientes[a][1] = ts
                hp.heappush(h_saida, (tr+ts, aux))
                clientes[a][2] = tr+ts
                clientes[a][3] = aux
            else:
                if aux == 1:
                    ocupado1 = False
                else: ocupado2 = False
                hp.heappush(h_saida, (99999999999,1))

    nf = media_pessoas_fila / clientes[nClientes-1][2]
    estatisticas.Imprime(nClientes, clientes, nf)

    