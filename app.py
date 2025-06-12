import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import smtplib
from email.message import EmailMessage
import csv
import re
import numpy as np
from db import init_db, registrar_solicitacao
import sqlite3

# Configurações iniciais
CSV_UNIFICADA = 'CSV/BaseUnificada.csv'
EMAIL_DESTINO = 'joaocarlosrh23@gmail.com'
DB_PATH = 'carimbos.db'

# Inicializar banco de dados
init_db()

# Sidebar para navegação
pagina = st.sidebar.selectbox('Escolha a página:', ['Gerar Carimbo', 'Relatórios'])

if pagina == 'Gerar Carimbo':
    st.title('Gerador de Carimbo')
    codigo = st.text_input('Digite o código (número do VD):')

    @st.cache_data
    def carregar_dados():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('SELECT * FROM base_unificada', conn)
        conn.close()
        return df

    def safe_str(val):
        if pd.isna(val) or val is None:
            return ''
        return str(val)

    def buscar_registros(df, codigo):
        codigo_num = re.sub(r'\D', '', str(codigo))
        mask = df['VD'].astype(str).apply(lambda x: codigo_num == re.sub(r'\D', '', x))
        return df[mask]

    def campos_faltando(linha):
        obrigatorios = {
            'Operadora': linha.get('Operadora', ''),
            'Designação': linha.get('Circuito/Designação', ''),
            'ID VIVO': linha.get('ID VIVO', ''),
            'ENDEREÇO': linha.get('ENDEREÇO', ''),
            'CIDADE': linha.get('CIDADE', ''),
            'UF': linha.get('UF', ''),
            'CEP': linha.get('CEP', '')
        }
        return [campo for campo, valor in obrigatorios.items() if not valor or str(valor).strip() == '-' or str(valor).strip() == 'nan']

    def gerar_carimbo(linha):
        largura, altura = 800, 420
        img = Image.new('RGB', (largura, altura), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 18)
            font_bold = ImageFont.truetype("arialbd.ttf", 18)
            font_title = ImageFont.truetype("arialbd.ttf", 22)
        except:
            font = ImageFont.load_default()
            font_bold = font
            font_title = font
        # Cores
        azul = (153, 204, 255)
        azul_escuro = (102, 153, 204)
        azul_cel = (0, 176, 240)
        amarelo = (255, 242, 153)
        amarelo_escuro = (255, 221, 51)
        vermelho = (204, 0, 0)
        cinza = (230, 230, 230)
        preto = (0, 0, 0)
        branco = (255, 255, 255)
        # Layout
        draw.rectangle([0, 0, largura, 40], fill=azul_escuro)  # Título
        draw.text((largura//2-200, 8), "CARIMBO DE ABERTURA DE CHAMADO POR E-MAIL", fill=branco, font=font_title)
        # Linhas principais
        y = 40
        h = 40
        campos = [
            ("VD", safe_str(linha['VD'])),
            ("OPERADORA", safe_str(linha['Operadora'])),
            ("DESIGNAÇÃO", safe_str(linha['Circuito/Designação'])),
            ("ID VANTIVE", safe_str(linha.get('ID VIVO', ''))),
            ("ENDEREÇO", safe_str(linha['ENDEREÇO'])),
            ("CIDADE", safe_str(linha['CIDADE'])),
            ("FILIAL", safe_str(linha['LOJAS']))
        ]
        for i, (label, valor) in enumerate(campos):
            cor = azul_cel if i in [1,2,3,4,5,6] else azul
            draw.rectangle([0, y, largura, y+h], fill=cor)
            draw.text((20, y+10), label, fill=preto, font=font_bold)
            draw.text((220, y+10), valor, fill=preto, font=font)
            y += h
        # Horário
        draw.rectangle([0, y, largura, y+40], fill=amarelo)
        draw.text((20, y+10), "HORÁRIO DE FUNCIONAMENTO", fill=preto, font=font_bold)
        draw.text((320, y+10), "SEG.À SEX.", fill=preto, font=font)
        draw.text((520, y+10), "07 ÀS 20", fill=preto, font=font)
        y += 40
        # Contato
        draw.rectangle([0, y, largura, y+40], fill=vermelho)
        draw.text((20, y+10), "CONTATO COMMAND CENTER", fill=branco, font=font_bold)
        draw.text((320, y+10), "Telefone: (11) 3274-7527", fill=branco, font=font)
        draw.text((520, y+10), "E-mail: central.comando@dpsp.com.br", fill=branco, font=font)
        y += 40
        # Mensagem
        draw.rectangle([0, y, largura, y+30], fill=amarelo_escuro)
        draw.text((20, y+5), "MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS", fill=preto, font=font_bold)
        y += 30
        # Rodapé
        draw.rectangle([0, y, largura, altura], fill=branco)
        draw.text((20, y+5), f"LOJA {safe_str(linha['VD'])} FAVOR LIGAR PARA CONFIRMAR...", fill=preto, font=font)
        return img

    def enviar_email(imagem, destinatario):
        # Placeholder para envio de e-mail
        pass

    df = carregar_dados()
    registros = None
    linha_selecionada = None

    if codigo:
        registros = buscar_registros(df, codigo)
        if not registros.empty:
            opcoes = [f"{safe_str(row['Operadora'])} | {safe_str(row['Circuito/Designação'])} | {safe_str(row['ID VIVO'])} | {safe_str(row['LOJAS'])}" for _, row in registros.iterrows()]
            idx = st.selectbox('Selecione o registro:', range(len(opcoes)), format_func=lambda i: opcoes[i])
            linha_selecionada = registros.iloc[idx]
            if st.button('Pré-visualizar Carimbo'):
                # Verifica se há dados principais
                principais = [safe_str(linha_selecionada['Operadora']), safe_str(linha_selecionada['Circuito/Designação']), safe_str(linha_selecionada.get('ID VIVO', ''))]
                if not any(principais):
                    st.warning('Este registro não possui dados suficientes para gerar o carimbo. Selecione outro ou revise a base.')
                else:
                    faltando = campos_faltando(linha_selecionada.to_dict())
                    if faltando:
                        st.warning(f"Este registro não possui dados suficientes para gerar o carimbo. Campos faltando: {', '.join(faltando)}. Selecione outro ou revise a base.")
                    else:
                        carimbo = gerar_carimbo(linha_selecionada)
                        buf = io.BytesIO()
                        carimbo.save(buf, format='PNG')
                        st.image(buf.getvalue(), caption='Pré-visualização do Carimbo')
                        if st.button('Enviar por e-mail'):
                            # Aqui registramos a solicitação no banco
                            registrar_solicitacao(
                                vd=safe_str(linha_selecionada['VD']),
                                operadora=safe_str(linha_selecionada['Operadora']),
                                designacao=safe_str(linha_selecionada['Circuito/Designação']),
                                id_vantive=safe_str(linha_selecionada.get('ID VIVO', '')),
                                endereco=safe_str(linha_selecionada['ENDEREÇO']),
                                cidade=safe_str(linha_selecionada['CIDADE']),
                                filial=safe_str(linha_selecionada['LOJAS']),
                                email_destino=EMAIL_DESTINO,
                                status_envio='Simulado'
                            )
                            st.success('Carimbo enviado por e-mail e registrado no banco! (Envio real a implementar)')
        else:
            st.warning('Nenhum registro encontrado para este código.')

elif pagina == 'Relatórios':
    st.title('Relatórios de Solicitações')
    # Conectar ao banco e buscar dados
    conn = sqlite3.connect(DB_PATH)
    df_rel = pd.read_sql_query('SELECT * FROM solicitacoes ORDER BY datahora DESC', conn)
    conn.close()

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_data = st.date_input('Filtrar por data', [])
    with col2:
        filtro_vd = st.text_input('Filtrar por VD')
    with col3:
        filtro_operadora = st.text_input('Filtrar por Operadora')

    df_filtrado = df_rel.copy()
    # Filtro por data
    if filtro_data:
        if isinstance(filtro_data, list) and len(filtro_data) == 2:
            df_filtrado = df_filtrado[(df_filtrado['datahora'] >= str(filtro_data[0])) & (df_filtrado['datahora'] <= str(filtro_data[1]))]
        elif not isinstance(filtro_data, list):
            df_filtrado = df_filtrado[df_filtrado['datahora'].str.startswith(str(filtro_data))]
    # Filtro por VD
    if filtro_vd:
        df_filtrado = df_filtrado[df_filtrado['vd'].str.contains(filtro_vd, case=False, na=False)]
    # Filtro por Operadora
    if filtro_operadora:
        df_filtrado = df_filtrado[df_filtrado['operadora'].str.contains(filtro_operadora, case=False, na=False)]

    st.dataframe(df_filtrado)
    st.markdown('---')
    st.download_button('Exportar para CSV', df_filtrado.to_csv(index=False).encode('utf-8'), file_name='relatorio_solicitacoes.csv', mime='text/csv') 