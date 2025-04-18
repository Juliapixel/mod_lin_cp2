import os
import pandas as pd
from time import sleep

# retorna a intensidade do sinal em %, assumindo um limite de 75m de alcançe
def calcular_sinal(distancia: float) -> float:
    return max(((distancia ** 2) * -(16 / 900)) + 100, 0)

def recomendar_acao(intensidade: float) -> str:
    if intensidade < 30:
        return "Tente adicionar um repetidor de sinal Wi-Fi em sua casa"
    if intensidade < 50:
        return "Tente mover o roteador para outro cômodo"
    if intensidade < 75:
        return "A intensidade de sinal será boa"
    return "A intensidade de sinal será muito boa"

dados = pd.DataFrame(columns=["cômodo", "intensidade"])

if os.path.isfile("comodos.csv"):
    dados = pd.read_csv("comodos.csv")

print("Calculadora de sinal Wi-Fi")
print("-----------------------------------------")
while True:
    print("Opções:")
    print("1. Adicionar cômodos")
    print("2. Listar sinais")
    print("3. Limpar dados")
    print("4. Sair")
    print("5. Sair sem salvar")
    print("0. Sobre")

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
                acao = recomendar_acao(float(row["intensidade"]))
                print(f"O cômodo {row["cômodo"]} terá sinal com intensidade de {float(row["intensidade"]):.1f}%")
                print(acao)
                print("-" * len(acao))
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
        case "0":
            print("Calculadora de intensidade de Wi-Fi")
            print()
            print("Esse programa recebe os nomes dos cômodos da sua casa e a distância deles até seu roteador Wi-Fi. Esses dados são usados para prever e classificar a intensidade do sinal esperada e então são salvos no arquivo comodos.csv para uso futuro.")
        case _:
            print("Digite uma opção válida")
