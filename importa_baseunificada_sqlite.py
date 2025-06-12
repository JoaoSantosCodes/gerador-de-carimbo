import pandas as pd
import sqlite3
import os

csv_path = os.path.join('CSV', 'BaseUnificada.csv')
db_path = 'carimbos.db'
table_name = 'base_unificada'

# Lê o CSV
print(f'Lendo {csv_path}...')
df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')
print(f'Colunas: {list(df.columns)}')
print('Primeiras linhas:')
print(df.head())

# Conecta ao banco
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Cria a tabela (dropa se já existir)
print(f'Criando tabela {table_name}...')
c.execute(f'DROP TABLE IF EXISTS {table_name}')

# Gera o comando CREATE TABLE dinamicamente
cols_types = ', '.join([f'"{col}" TEXT' for col in df.columns])
c.execute(f'CREATE TABLE {table_name} ({cols_types})')

# Insere os dados
print('Inserindo dados...')
df.to_sql(table_name, conn, if_exists='append', index=False)

conn.commit()
conn.close()
print('Importação concluída!') 