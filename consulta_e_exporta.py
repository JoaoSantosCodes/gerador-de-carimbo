import sqlite3
import pandas as pd

# Parâmetros de filtro (edite conforme necessário)
FILTRO_CIDADE = None  # Exemplo: 'SÃO PAULO'
FILTRO_OPERADORA = None  # Exemplo: 'VIVO'
FILTRO_STATUS = None  # Exemplo: 'ATIVA'

# Conexão
conn = sqlite3.connect('carimbos.db')
query = 'SELECT * FROM base_unificada WHERE 1=1'

if FILTRO_CIDADE:
    query += f" AND CIDADE LIKE '%{FILTRO_CIDADE}%'"
if FILTRO_OPERADORA:
    query += f" AND Operadora LIKE '%{FILTRO_OPERADORA}%'"
if FILTRO_STATUS:
    query += f" AND STATUS LIKE '%{FILTRO_STATUS}%'"

print('Executando consulta:')
print(query)
df = pd.read_sql_query(query, conn)
print(f'Foram encontrados {len(df)} registros.')

# Exporta para CSV
if len(df) > 0:
    df.to_csv('resultado_consulta.csv', index=False, encoding='utf-8-sig')
    print('Resultado exportado para resultado_consulta.csv')
else:
    print('Nenhum registro encontrado.')

conn.close() 