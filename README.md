# 🐍 Snake CV — Curriculum Vitae Interattivo

Un curriculum vitae presentato come **gioco Snake**. Mangia i cibi per scoprire le informazioni del candidato: istruzione, esperienze, competenze e soft skill. Ogni elemento del CV è un "cibo" da raccogliere nel gioco.

---

## ✨ Funzionalità

- 🎮 **Gioco Snake completo** con punteggi, record e livelli di velocità regolabili
- 📄 **CV integrato** — ogni elemento raccoglibile rivela una sezione del curriculum
- 📊 **Pannello competenze** con barre di avanzamento animate (Python, React/JS, Java, SQL, Docker, KNX/IoT)
- 🗂️ **Registro info** — tutte le sezioni raccolte vengono visualizzate in tempo reale
- 📱 **Responsive e mobile-friendly** con D-pad touch per smartphone
- 🕹️ **Controlli multipli**: frecce direzionali, WASD, swipe touch
- 💾 **Salvataggio progressi** tramite localStorage (campagna continua anche dopo game over)
- 🎯 **Schermata di vittoria** con riepilogo completo del CV alla fine della partita

---

## 🗂️ Struttura del progetto

```
int_cv/
├── app.py                  # Server Flask (entry point)
├── requirements.txt        # Dipendenze Python
├── templates/
│   └── index.html          # Pagina principale (HTML + CSS)
└── static/
    └── js/
        ├── cv-data.js      # Contenuto del CV (da personalizzare)
        ├── game.js         # Logica del gioco Snake
        ├── renderer.js     # Rendering del canvas
        ├── controls.js     # Gestione input (tastiera + touch)
        ├── ui-manager.js   # Aggiornamento interfaccia
        ├── storage.js      # Persistenza localStorage
        └── main.js         # Bootstrap dell'applicazione
```

---

## 🚀 Avvio rapido

### 1. Clona il repository

```bash
git clone https://github.com/gformy/int_cv.git
cd int_cv
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

> **Nota:** richiede Python 3.8+. È consigliato usare un ambiente virtuale:
> ```bash
> python -m venv .venv && source .venv/bin/activate  # Linux/Mac
> python -m venv .venv && .venv\Scripts\activate     # Windows
> pip install -r requirements.txt
> ```

### 3. Avvia il server

```bash
python app.py
```

Apri il browser su **http://localhost:5000**

---

## 📱 Accesso da mobile (stessa rete WiFi)

Avvia il server normalmente e poi trova il tuo IP locale:

```bash
# Mac / Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

Poi apri **http://\<tuo-ip\>:5000** sul tuo smartphone. Apparirà automaticamente il D-pad touch.

---

## ⚙️ Configurazione

### Cambiare porta

```bash
PORT=8080 python app.py
```

---

## 🎮 Come si gioca

| Azione | Tastiera | Mobile |
|--------|----------|--------|
| Su | `↑` / `W` | Swipe ↑ o D-pad |
| Giù | `↓` / `S` | Swipe ↓ o D-pad |
| Sinistra | `←` / `A` | Swipe ← o D-pad |
| Destra | `→` / `D` | Swipe → o D-pad |

- **Mangia i cibi colorati** per guadagnare punti e scoprire le sezioni del CV
- Ogni colore corrisponde a una categoria:
  - 🟡 **Giallo** — Istruzione
  - 🟠 **Arancione** — Tirocinio
  - 🟢 **Verde acqua / Turchese** (`#4ecdc4`) — Volontariato
  - 🟣 **Viola** (`#a855f7`) — Esperienza da Sviluppatore
  - 🔴 **Rosa/Rosso** (`#f43f5e`) — Esperienza ASL Roma 2
  - 🔵 **Ciano** (`#06b6d4`) — Soft Skills & Extra
- **Game Over?** Puoi continuare la campagna: i progressi sono salvati
- **Velocità** regolabile con lo slider (solo desktop)

---

## 🛠️ Tecnologie utilizzate

| Layer | Tecnologia |
|-------|-----------|
| Backend | Python 3 + Flask |
| Frontend | HTML5 Canvas, CSS3, Vanilla JS |
| Font | Google Fonts (Orbitron, Share Tech Mono) |
| Deploy | Gunicorn (incluso in `requirements.txt`) |
| Storage | Browser localStorage |

---

## ✏️ Personalizzare il CV

Modifica il file **`static/js/cv-data.js`** per inserire i tuoi dati.  
Ogni voce ha questa struttura:

```js
{
  cat: '🎓',                      // emoji categoria
  cat_name: 'Istruzione',         // nome categoria
  title: 'Laurea in Informatica', // titolo breve
  text: 'Descrizione dettagliata...', // testo visualizzato
  color: '#ffd700',               // colore del "cibo" nel gioco
  glow: 'rgba(255,215,0,0.6)'     // effetto glow del cibo
}
```

Le barre competenze nel pannello laterale si animano automaticamente in base alle categorie degli elementi raccolti, secondo la mappa `SKILL_MAP` in fondo allo stesso file.

---

## 🚢 Deploy in produzione

Il progetto include **Gunicorn** per il deploy su server Linux/cloud:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:SnakeCvApp(AppConfig()).app"
```

---

## 📄 Licenza

Progetto open source — libero di essere forked e adattato al proprio curriculum.
