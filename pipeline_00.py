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

# Função para ler um arquivo CSV e retornar um DataFrame Duckdb


def ler_csv(caminho_do_arquivo):
    return duckdb.read_csv(caminho_do_arquivo)


# Função para adicionar uma coluna de total de vendas
def transformar(df):
    # Executa a consulta SQL que inclui a nova coluna, operando sobre a tabela virtual
    df_transformado = duckdb.sql(
        "SELECT *, quantidade * valor AS total_vendas FROM df").df()
    # Remove o registro da tabela virtual para limpeza
    print(df_transformado)
    return df_transformado

# Função para converter o Duckdb em Pandas e salvar o DataFrame no PostgreSQL


def salvar_no_postgres(df, tabela):
    # Ex: 'postgresql://user:password@localhost:5432/database_name'
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    # Salvar o DataFrame no PostgreSQL
    df.to_sql(tabela, con=engine, if_exists='append', index=False)
    print("salvo no banco de dados...")


if __name__ == "__main__":
    url_pasta = os.getenv("URL_PASTA")
    diretorio_local = './pasta_gdown'

    # baixar_pasta_google_drive(url_pasta, diretorio_local)
    arquivos_csv = listar_arquivos_csv(diretorio_local)
    print(arquivos_csv)
    df_duckdb = ler_csv(arquivos_csv)
    print(df_duckdb)
    print(type(df_duckdb))
    df = transformar(df_duckdb)
    print(type(df))
    salvar_no_postgres(df, "vendas_calculado")
