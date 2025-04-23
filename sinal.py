import os
import pandas as pd
from time import sleep

# retorna a intensidade do sinal em %, assumindo um limite de 75m de alcançe
def calcular_sinal(distancia: float) -> float:
    return max(((distancia ** 2) * -(16 / 900)) + 100, 0)

# cria uma recomendação para o usuário a partir da intensidade do sinal em %
def recomendar_acao(intensidade: float) -> str:
    if intensidade < 30:
        return "Tente adicionar um repetidor de sinal Wi-Fi em sua casa"
    if intensidade < 50:
        return "Tente mover o roteador para outro cômodo"
    if intensidade < 80:
        return "A intensidade de sinal será boa"
    return "A intensidade de sinal será muito boa"

def imprimir_dados(comodo: str, intensidade: float):
    acao = recomendar_acao(intensidade)
    print(f"O cômodo {comodo} terá sinal com intensidade de {intensidade:.1f}%")
    print(acao)
    print("-" * len(acao))

dados = pd.DataFrame(columns=["cômodo", "intensidade"])

# carregar os dados do arquivo se ele existir
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

            imprimir_dados(nome, intensidade)

            novo = pd.DataFrame({"cômodo": [nome], "intensidade": [intensidade]})
            # pandas retorna um erro se concatenarmos um DataFrame a um DataFrame vazio
            if len(dados) > 0:
                dados = pd.concat([dados, novo])
            else:
                dados = novo
        case "2":
            for _, row in dados.iterrows():
                # checa se os valores existem na linha atual
                if row["cômodo"] is not None and row["intensidade"] is not None:
                    imprimir_dados(row["cômodo"], float(row["intensidade"]))
                    sleep(1)
        case "3":
            dados = pd.DataFrame(columns=dados.columns)
        case "4":
            if len(dados) > 0:
                dados.to_csv("comodos.csv")
            elif os.path.isfile("comodos.csv") and len(dados) == 0:
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
