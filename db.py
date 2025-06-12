import sqlite3
from datetime import datetime

def init_db(db_path='carimbos.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datahora TEXT,
            vd TEXT,
            operadora TEXT,
            designacao TEXT,
            id_vantive TEXT,
            endereco TEXT,
            cidade TEXT,
            filial TEXT,
            email_destino TEXT,
            status_envio TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_solicitacao(vd, operadora, designacao, id_vantive, endereco, cidade, filial, email_destino, status_envio, db_path='carimbos.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO solicitacoes (datahora, vd, operadora, designacao, id_vantive, endereco, cidade, filial, email_destino, status_envio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        vd, operadora, designacao, id_vantive, endereco, cidade, filial, email_destino, status_envio
    ))
    conn.commit()
    conn.close() 