@echo off
cd /d %~dp0
python consolidar.py
python -m streamlit run portal.py
pause