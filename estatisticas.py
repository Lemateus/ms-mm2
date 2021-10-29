from tabulate import tabulate
from matplotlib import pyplot as plt

def Imprime(nClientes, clientes):
    cabecalho = ["ID", "TEC", "Hr_Chegada", "TS", "Inicio_Serviço", "Fim_Serviço", "Tempo_Fila", "Tempo_Sistema", "Tempo_Ocioso"]
    
    est = []
    tmp_ocioso = 0
    tmp_ocioso_acumolado = 0
    tf_acumulado = 0
    tempo_sistema_acumulado = 0
    for id in range(nClientes):
        aux = clientes[id]
        tec = aux[0] if(id==0) else aux[0]-clientes[id-1][0]
        tf = (aux[2]-aux[1])-aux[0]
        tf = tf if(abs(tf)>1e-5) else 0
        tf_acumulado += tf

        encontrou = False
        for i in range(id-1, -1, -1):
            if(clientes[i][3]==clientes[id][3]):
                encontrou = True
                tmp_ocioso = aux[0] - clientes[i][2]
                break
        
        if not encontrou:
            tmp_ocioso = aux[0]
        
        if tmp_ocioso<1e-5:
            tmp_ocioso = 0

        tmp_ocioso_acumolado += tmp_ocioso

        a = [id+1, tec, aux[0], aux[1], aux[2]-aux[1], aux[2], tf, aux[2]-aux[0], tmp_ocioso]

        tempo_sistema_acumulado += aux[2]-aux[0]
        est.append(a)


    print(tabulate(est, cabecalho))
    print("Taxa Média de Ocupação do Servidor   =  {:.2f}".format(1-(tmp_ocioso_acumolado/(clientes[nClientes-1][2]*2))) )
    print("Tempo Médio de uma Entidade na Fila  =  {:.2f} min".format(tf_acumulado/nClientes))
    print("Tempo Medio no Sistema               =  {:.2f} min".format(tempo_sistema_acumulado/nClientes))
        