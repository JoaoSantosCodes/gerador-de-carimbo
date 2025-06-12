import subprocess
import sys

steps = [
    ("Convertendo Excel para CSV...", [sys.executable, 'converter_e_revisar_excel.py']),
    ("Unificando planilhas...", [sys.executable, 'CSV/unificar_planilhas.py']),
    ("Importando para o banco SQLite...", [sys.executable, 'importa_baseunificada_sqlite.py'])
]

for msg, cmd in steps:
    print(f"\n=== {msg} ===")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Erro ao executar: {cmd}")
        sys.exit(result.returncode)

print("\nProcesso concluído com sucesso!") 