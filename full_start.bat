@ECHO OFF
python static/PY/chewer.py
python app.py
start chrome http://127.0.0.1:5000/ 
PAUSE