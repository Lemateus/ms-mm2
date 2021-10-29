from numpy import ceil
from tabulate import tabulate
from matplotlib import pyplot as plt
import math

class Est:
    def __init__(self):
        self.oc_serv = []
        self.ent_fila = []
        self.tmp_sis = []
        self.num_fila = []
        self.caso = 1

    def Imprime(self, nClientes, clientes, nf):
        cabecalho = ["ID", "TEC", "Hr_Chegada", "TS", "Inicio_Serviço", "Fim_Serviço", "Tempo_Fila", "Tempo_Sistema", "Tempo_Ocioso"]
        
        est = []
        tmp_ocioso = 0
        tmp_ocioso_acumulado = 0
        tf_acumulado = 0
        tempo_sistema_acumulado = 0
        max_tf = 0

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

            tmp_ocioso_acumulado += tmp_ocioso
            max_tf = max(max_tf, tf)

            a = [id+1, tec, aux[0], aux[1], aux[2]-aux[1], aux[2], tf, aux[2]-aux[0], tmp_ocioso]

            tempo_sistema_acumulado += aux[2]-aux[0]
            est.append(a)

        self.oc_serv.append(1-(tmp_ocioso_acumulado/(clientes[nClientes-1][2]*2)))
        self.ent_fila.append((tf_acumulado/nClientes))
        self.tmp_sis.append(tempo_sistema_acumulado/nClientes)
        self.num_fila.append(nf)
        

        if self.caso == 1:
            print("Primeira Simulação:\n")

            print(tabulate(est, cabecalho))
            print("\nTaxa Média de Ocupação do Servidor   =  {:.2f}".format(1-(tmp_ocioso_acumulado/(clientes[nClientes-1][2]*2))) )
            print("Tempo Médio de uma Entidade na Fila  =  {:.2f} min".format(tf_acumulado/nClientes))
            print("Tempo Medio no Sistema               =  {:.2f} min".format(tempo_sistema_acumulado/nClientes))
            print("Número Médio de Entidades na Fila    =  {:.2f}".format(nf))

        self.caso += 1


    def Calculo_Intervalo(self, valores):
        tam = len(valores)

        media = 0
        media = sum(valores)/tam

        s = 0
        for x in valores:
            s += x*x
        s -= tam*media*media
        s /= (tam-1)
        s = math.sqrt(s)

        h = 2.093 * s/math.sqrt(tam)

        return [media-h, media+h]
        

    def Graficos(self, nRepeticoes):

        plt.subplot(221)
        plt.bar([x for x in range(1, nRepeticoes+1)], [x*100 for x in self.oc_serv])
        plt.axis([0, nRepeticoes+1, 0, 100])
        plt.xlabel('Instância')
        plt.ylabel('Tempo de Ocupação em %')

        plt.subplot(222)
        plt.bar([x for x in range(1, nRepeticoes+1)], self.ent_fila)
        plt.xlabel('Instância')
        plt.ylabel('Tempo Médio na Fila (min)')

        plt.subplot(223)
        plt.bar([x for x in range(1, nRepeticoes+1)], self.num_fila)
        plt.xlabel('Instância')
        plt.ylabel('Num Médio Entidades na Fila')

        plt.subplot(224)
        plt.bar([x for x in range(1, nRepeticoes+1)], self.tmp_sis)
        plt.xlabel('Instância')
        plt.ylabel('Tempo Médio no Sis (min)')


        # Confiança Estatística

        print("\nIntervalos com 95% de Confiança\n")

        aux = self.Calculo_Intervalo(self.oc_serv)
        print("Taxa Média de Ocupação do Servidor: [{:.3f}, {:.3f}]".format(aux[0], aux[1]))

        aux = self.Calculo_Intervalo(self.ent_fila)
        print("Tempo Médio de uma Entidade na Fila: [{:.3f}, {:.3f}]".format(aux[0], aux[1]))

        aux = self.Calculo_Intervalo(self.num_fila)
        print("Num Médio de Entidades na Fila: [{:.3f}, {:.3f}]".format(aux[0], aux[1]))

        aux = self.Calculo_Intervalo(self.tmp_sis)
        print("Tempo Medio no Sistema: [{:.3f}, {:.3f}]".format(aux[0], aux[1]))


        plt.show()
