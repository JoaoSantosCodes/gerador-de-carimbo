# Gerador de Carimbo

Bem-vindo à documentação oficial do projeto!

---

## Exemplo de uso rápido

```bash
# Atualize os dados
python scripts/atualiza_tudo.py

# Rode o app
streamlit run app.py
```

---

## Exemplo visual

![Print da interface do app](./print-interface.png)

*Para adicionar um print, salve uma imagem da tela principal do app como `print-interface.png` nesta pasta (`/docs`).*

*Exemplos visuais ajudam novos usuários a entender rapidamente o funcionamento do sistema.*

---

## Visão Geral

O Gerador de Carimbo é um sistema para unificação, consulta e geração de carimbos a partir de dados de lojas e inventário, com interface web, automação de pipeline e integração com banco de dados SQLite.

---

## Como Usar

1. **Atualize os arquivos Excel na pasta `Excel/`**
2. **Rode o pipeline de atualização:**
   ```bash
   python scripts/atualiza_tudo.py
   ```
3. **Inicie o app:**
   ```bash
   streamlit run app.py
   ```
4. **Consulte e exporte dados:**
   ```bash
   python scripts/consulta_e_exporta.py
   ```

---

## Scripts Utilitários

Veja a pasta `scripts/` para automações de backup, importação, consulta, criação de issues e mais.

---

## Contribuindo

Leia o arquivo [CONTRIBUTING.md](../CONTRIBUTING.md) para saber como colaborar.

---

## Dúvidas?
Abra uma issue no [GitHub](../issues)! 