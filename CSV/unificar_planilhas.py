import pandas as pd
import os
import csv
import unicodedata

# Função para extrair apenas números de uma string
def extrair_numero(texto):
    if pd.isna(texto):
        return ''
    return ''.join(filter(str.isdigit, str(texto)))

# Função para obter valor seguro de uma coluna
def safe_get(row, col):
    return row[col] if col in row and pd.notna(row[col]) else ''

# Função para detectar o separador do CSV
def detectar_separador(caminho):
    with open(caminho, 'r', encoding='utf-8-sig') as f:
        amostra = f.read(2048)
        sniffer = csv.Sniffer()
        delimitador = sniffer.sniff(amostra).delimiter
    return delimitador

# Função para carregar CSV ou Excel automaticamente
def carregar_arquivo(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext in ['.xlsx', '.xls']:
        print(f'Lendo arquivo Excel: {caminho}')
        return pd.read_excel(caminho)
    else:
        sep = detectar_separador(caminho)
        print(f'Lendo arquivo CSV: {caminho} (sep={sep})')
        return pd.read_csv(caminho, sep=sep, encoding='utf-8-sig')

# Caminhos dos arquivos
CSV_LOJAS = 'CSV/Relação-de-Lojas.csv'
CSV_INV = 'CSV/Inventário.csv'
CSV_SAIDA = 'CSV/BaseUnificada.csv'

# Carregar os arquivos
print('Carregando arquivos...')
df_lojas = carregar_arquivo(CSV_LOJAS)
df_inv = carregar_arquivo(CSV_INV)

# Limpar colunas Unnamed
print('Limpando colunas extras...')
df_lojas = df_lojas.loc[:, ~df_lojas.columns.str.contains('^Unnamed')]
df_inv = df_inv.loc[:, ~df_inv.columns.str.contains('^Unnamed')]

# Normalizar nomes das colunas (remover espaços, aspas e corrigir encoding)
df_lojas.columns = df_lojas.columns.str.strip().str.replace('"', '').str.replace("'", '')
df_inv.columns = df_inv.columns.str.strip().str.replace('"', '').str.replace("'", '')

print('Colunas em df_lojas:', df_lojas.columns.tolist())
print('Colunas em df_inv:', df_inv.columns.tolist())

# Encontrar a coluna PEOP de forma robusta
def normalizar_nome(col):
    col = col.strip().upper().replace('.', '').replace(' ', '')
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    return col

col_peop = None
for col in df_lojas.columns:
    if normalizar_nome(col) == 'PEOP':
        col_peop = col
        break
if not col_peop:
    print('Colunas disponíveis:', df_lojas.columns.tolist())
    raise Exception("Coluna PEOP não encontrada! Verifique o nome exato no arquivo de lojas.")

# Lista para armazenar as linhas unificadas e incompletas
linhas = []
vd_incompletos = []

print('Processando dados...')
# Encontrar as colunas obrigatórias de forma robusta
campos_obrigatorios = ['PEOP', 'ENDERECO', 'CIDADE', 'UF', 'CEP']
colunas_encontradas = {}
for campo in campos_obrigatorios:
    for col in df_lojas.columns:
        if normalizar_nome(col) == campo:
            colunas_encontradas[campo] = col
            break
    if campo not in colunas_encontradas:
        print('Colunas disponíveis:', df_lojas.columns.tolist())
        raise Exception(f"Coluna obrigatória '{campo}' não encontrada! Verifique o nome exato no arquivo de lojas.")

for idx, loja in df_lojas.iterrows():
    peop_num = extrair_numero(loja[colunas_encontradas['PEOP']])
    inventarios = df_inv[df_inv['People'].astype(str).apply(lambda x: peop_num in extrair_numero(x))]
    
    if inventarios.empty:
        linha = {
            'VD': peop_num,
            **loja.to_dict(),
            'Operadora': '',
            'Circuito/Designação': '',
            'Novo Circuito/Designação': '',
            'ID VIVO': '',
            'Novo ID Vivo': ''
        }
        linhas.append(linha)
        vd_incompletos.append({'VD': peop_num, 'Motivo': 'Sem inventário correspondente'})
    else:
        for _, inv in inventarios.iterrows():
            circuito = safe_get(inv, 'Novo Circuito/Designação') if str(safe_get(inv, 'Novo Circuito/Designação')).strip() and str(safe_get(inv, 'Novo Circuito/Designação')).strip() != '-' else safe_get(inv, 'Circuito/Designação')
            id_vivo = safe_get(inv, 'Novo ID Vivo') if str(safe_get(inv, 'Novo ID Vivo')).strip() and str(safe_get(inv, 'Novo ID Vivo')).strip() != '-' else safe_get(inv, 'ID VIVO')
            linha = {
                'VD': peop_num,
                **loja.to_dict(),
                'Operadora': safe_get(inv, 'Operadora'),
                'Circuito/Designação': circuito,
                'ID VIVO': id_vivo
            }
            linhas.append(linha)
            obrigatorios = [
                linha['VD'],
                linha['Operadora'],
                linha['Circuito/Designação'],
                linha['ID VIVO'],
                loja[colunas_encontradas['ENDERECO']],
                loja[colunas_encontradas['CIDADE']],
                loja[colunas_encontradas['UF']],
                loja[colunas_encontradas['CEP']]
            ]
            if not all(obrigatorios):
                vd_incompletos.append({'VD': peop_num, 'Motivo': 'Campos obrigatórios ausentes'})

# Criar DataFrame final
print('Criando DataFrame final...')
colunas_saida = ['VD'] + list(df_lojas.columns) + ['Operadora', 'Circuito/Designação', 'ID VIVO']
df_saida = pd.DataFrame(linhas, columns=colunas_saida)

# Remover colunas Unnamed do DataFrame final
df_saida = df_saida.loc[:, ~df_saida.columns.str.contains('^Unnamed')]

# Depuração
print('\nColunas do DataFrame final:', df_saida.columns.tolist())
print('\nPrimeiras linhas:')
print(df_saida.head())

# Salvar CSV com encoding utf-8-sig e delimitador ;
print('\nSalvando arquivos...')
df_saida.to_csv(CSV_SAIDA, index=False, encoding='utf-8-sig', sep=';')

# Checagem: garantir que VD está presente
if 'VD' not in df_saida.columns:
    raise Exception('A coluna VD não foi criada corretamente!')

# Salvar relatório de VDs incompletos
if vd_incompletos:
    df_incompletos = pd.DataFrame(vd_incompletos)
    df_incompletos.to_csv('CSV/VDs_incompletos.csv', index=False, encoding='utf-8-sig', sep=';')
    print(f'\nRelatório de VDs incompletos salvo em CSV/VDs_incompletos.csv ({len(vd_incompletos)} registros)')

print(f'\nArquivo {CSV_SAIDA} gerado com sucesso!') 