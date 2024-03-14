import os
import gdown
import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Função para baixar uma pasta do Google Drive


def baixar_pasta_google_drive(url_pasta, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local,
                          quiet=False, use_cookies=False)

# Função para listar arquivos CSV no diretório especificado


def listar_arquivos_csv(diretorio):
    arquivos_csv = []
    todos_os_arquivos = os.listdir(diretorio)
    for arquivo in todos_os_arquivos:
        if arquivo.endswith(".csv"):
            caminho_completo = os.path.join(diretorio, arquivo)
            arquivos_csv.append(caminho_completo)
    return arquivos_csv


if __name__ == "__main__":
    url_pasta = os.getenv("URL_PASTA")
    diretorio_local = './pasta_gdown'

    baixar_pasta_google_drive(url_pasta, diretorio_local)
    arquivos_csv = listar_arquivos_csv(diretorio_local)
    print(arquivos_csv)
