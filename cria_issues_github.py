import requests
import re

# ATENÇÃO: Nunca deixe seu token salvo neste arquivo!
# Use uma variável de ambiente ou insira manualmente ao rodar.
GITHUB_TOKEN = input('Digite seu GitHub Personal Access Token: ').strip()
REPO = 'JoaoSantosCodes/gerador-de-carimbo'
ISSUES_FILE = 'issues_sugestoes.md'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

with open(ISSUES_FILE, encoding='utf-8') as f:
    content = f.read()

# Regex para capturar cada issue sugerida
matches = re.findall(r'- \*\*\[(.*?)\] (.*?)\*\*\n(  - .+?)(?=\n- |\n##|\Z)', content, re.DOTALL)

for label, title, body in matches:
    body = re.sub(r'^  - ', '', body, flags=re.MULTILINE).strip()
    data = {
        'title': f'[{label}] {title}',
        'body': body,
        'labels': [label.lower()]
    }
    response = requests.post(
        f'https://api.github.com/repos/{REPO}/issues',
        headers=headers,
        json=data
    )
    if response.status_code == 201:
        print(f'Issue criada: {title}')
    else:
        print(f'Erro ao criar issue: {title} - {response.status_code} - {response.text}') 