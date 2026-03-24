# int_cv
an interactive curriculum with python

```bash
# 1. Installa le dipendenze (solo Flask)
pip install -r requirements.txt
 
# 2. Avvia il server
python app.py
```
 
Apri il browser su **http://localhost:5000**
 
## Accesso da mobile (stessa rete WiFi)
 
```bash
# Trova il tuo IP locale su Mac/Linux:
ifconfig | grep "inet " | grep -v 127.0.0.1
 
# Su Windows:
ipconfig
```


## Cambiare porta
 
```bash
PORT=8080 python app.py
```