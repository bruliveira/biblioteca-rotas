import os
import json

def carregar_dados(arquivo):
    caminho_arquivo = os.path.join("data", arquivo)
    with open(caminho_arquivo, "r") as arquivo_json:
        return json.load(arquivo_json)


def salvar_dados(arquivo, dados):
    caminho_arquivo = os.path.join("data", arquivo)
    with open(caminho_arquivo, "w") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4)
