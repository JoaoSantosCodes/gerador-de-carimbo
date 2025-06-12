# Gerador de Carimbo — Documentação do Projeto

## Visão Geral

O Gerador de Carimbo é um sistema que:
- Unifica dados de duas planilhas (Relação de Lojas e Inventário) em uma base única.
- Permite buscar e gerar carimbos personalizados para cada loja/VD.
- Registra cada solicitação em um banco de dados para auditoria e relatórios.
- Possui interface web (Streamlit) para uso e consulta.

---

## Estrutura de Pastas e Arquivos

```
/
├── app.py                # Aplicativo principal (Streamlit)
├── db.py                 # Módulo de banco de dados SQLite
├── start_app.bat         # Script para rodar o app
├── requirements.txt      # Dependências do projeto
├── carimbos.db           # Banco de dados SQLite (gerado automaticamente)
├── CSV/
│   ├── Relação-de-Lojas.csv      # Planilha de lojas (origem)
│   ├── Inventário.csv            # Planilha de inventário (origem)
│   ├── BaseUnificada.csv         # Planilha unificada (gerada)
│   └── unificar_planilhas.py     # Script de unificação
├── img/
│   └── Modelo Carimbo.jpg        # Imagem de referência
├── Excel/
│   ├── Inventário_05.2025.xlsx   # Originais em Excel
│   └── Relação de Lojas Old.xlsx
```

---

## Fluxo de Funcionamento

1. **Unificação das Planilhas**
   - Execute `python CSV/unificar_planilhas.py` para gerar `BaseUnificada.csv`.
   - O script faz o de/para entre PEOP (lojas) e People (inventário), buscando o número em qualquer parte do campo.
   - Se houver campo "Novo", ele é priorizado.

2. **Uso do App**
   - Rode o app com `streamlit run app.py` (ou use o `start_app.bat`).
   - Digite o código do VD/loja para buscar registros.
   - Selecione o registro desejado e visualize o carimbo.
   - Clique em "Enviar por e-mail" para registrar a solicitação no banco (envio real pode ser implementado depois).

3. **Relatórios**
   - Acesse a página "Relatórios" no menu lateral.
   - Filtre por data, VD ou operadora.
   - Exporte os registros para CSV.

---

## Banco de Dados

- O banco `carimbos.db` é criado automaticamente.
- Cada solicitação de carimbo é registrada com data/hora, dados do carimbo, e-mail de destino e status de envio.

---

## Pontos de Atenção

- Sempre gere a `BaseUnificada.csv` após atualizar as planilhas de origem.
- O app só busca dados na planilha unificada.
- Se um registro não tiver dados suficientes, o carimbo não será gerado.
- O envio de e-mail está como "simulado", mas pode ser implementado facilmente.

---

## Melhorias Futuras

- Implementar envio real de e-mail.
- Adicionar autenticação de usuário.
- Permitir upload de novas planilhas via interface.
- Gerar carimbo em PDF.
- Mais filtros e gráficos nos relatórios.

## Teste de Atualização
- Teste de commit realizado em 2024 