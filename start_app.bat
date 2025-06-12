@echo off
echo Iniciando o aplicativo...
REM Instala as dependências do projeto
pip install -r requirements.txt
REM Inicia o app Streamlit
python -m streamlit run app.py
pause 