import json
from Simulacao import simulador
from estatisticas import Est

from Simulacao import executaSimulacao


def main():
    with open("config/parametros-simulacao.json", "r") as arqConfig:
        paramSimulacao = json.load(arqConfig)
    
        if "filaMax" in paramSimulacao and  paramSimulacao["filaMax"] == "inf":
            paramSimulacao["filaMax"] = paramSimulacao["nClientes"]

    estatisticas = Est()
    for count in range(20):
        simulador(estatisticas, **paramSimulacao)
    estatisticas.Graficos(20)
    
    
if __name__ == "__main__":
    main()