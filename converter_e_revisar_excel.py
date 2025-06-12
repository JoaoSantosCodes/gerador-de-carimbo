import pandas as pd
import os

excel_dir = 'Excel'
csv_dir = 'CSV'

arquivos = [f for f in os.listdir(excel_dir) if f.endswith('.xlsx') or f.endswith('.xls')]

for arquivo in arquivos:
    caminho_excel = os.path.join(excel_dir, arquivo)
    nome_csv = os.path.splitext(arquivo)[0] + '.csv'
    caminho_csv = os.path.join(csv_dir, nome_csv)
    print(f'\nLendo: {caminho_excel}')
    df = pd.read_excel(caminho_excel)
    print(f'Colunas: {list(df.columns)}')
    print('Primeiras linhas:')
    print(df.head())
    df.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
    print(f'Arquivo CSV salvo em: {caminho_csv}') 