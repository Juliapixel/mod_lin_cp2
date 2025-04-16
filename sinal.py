import os
import pandas as pd
from time import sleep
import math

# retorna a intensidade do sinal em dBm (decibel-miliwatt)
def calcular_sinal(distancia: float) -> float:
    # TODO: achar uma fórmula menos idiota e que funciona
    # intensidade em w/m^2, assumindo um roteador de 500mW
    energia = 0.5 / (4 * math.pi * (distancia ** 2))
    # intensidade do sinal em dBm
    intensidade = 10 * math.log10(energia / 0.001)
    return intensidade

def recomendar_acao(intensidade: float) -> str:
    if intensidade < -80:
        return "Tente adicionar um repetidor de sinal Wi-Fi em sua casa"
    if intensidade < -60:
        return "Tente mover o roteador para outro cômodo"
    if intensidade < -40:
        return "A intensidade de sinal será boa"
    return "A intensidade de sinal será muito boa"

dados = pd.DataFrame(columns=["cômodo", "intensidade"])

if os.path.isfile("comodos.csv"):
    dados = pd.read_csv("comodos.csv")

while True:
    print("Opções:")
    print("1. Adicionar cômodos")
    print("2. Listar sinais")
    print("3. Limpar dados")
    print("4. Sair")
    print("5. Sair sem salvar")

    match input("Escolha uma: "):
        case "1":
            nome = input("Nome do cômodo: ")
            dist = float(input("Distância do roteador (em m): "))
            intensidade = calcular_sinal(dist)
            novo = pd.DataFrame({"cômodo": [nome], "intensidade": [intensidade]})
            # pandas retorna um erro se concatenarmos um DataFrame a um DataFrame vazio
            if len(dados) > 0:
                dados = pd.concat([dados, novo])
            else:
                dados = novo
        case "2":
            for _, row in dados.iterrows():
                print(f"O cômodo {row["cômodo"]} terá sinal com intensidade de {float(row["intensidade"]):.1f}dBm")
                print(recomendar_acao(float(row["intensidade"])))
                print("----------------------------------")
                sleep(1)
        case "3":
            dados = pd.DataFrame(columns=dados.columns)
        case "4":
            if len(dados) > 0:
                dados.to_csv("comodos.csv")
            elif os.path.isfile("comodos.csv"):
                os.remove("comodos.csv")
            break
        case "5":
            break
