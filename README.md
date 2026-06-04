# 🧱 Gestore Set LEGO

<p align="center">
  Applicazione desktop sviluppata in Python per la gestione completa di una collezione di set LEGO.
</p>

<p align="center">
  <strong>Creazione • Modifica • Ricerca • Salvataggio • Catalogazione</strong>
</p>

---

## 📖 Panoramica

**Gestore Set LEGO** è un software desktop progettato per consentire la gestione di una collezione personale di set LEGO attraverso un'interfaccia grafica semplice da utilizzare.

L'applicazione permette di inserire e consultare tutte le informazioni principali di ciascun set, incluse immagini, dati tecnici e collegamenti al sito ufficiale LEGO.

Tutti i dati vengono memorizzati in formato JSON per una gestione più facile.

---

## ✨ Funzionalità Principali

### 🧩 Gestione dei Set

* Creazione di nuovi set LEGO
* Modifica dei set esistenti
* Eliminazione dei set registrati
* Visualizzazione in tabella interattiva

### 🖼️ Gestione delle Immagini

* Associazione di un'immagine ad ogni set
* Anteprima durante l'inserimento e la modifica
* Visualizzazione delle miniature nella tabella principale

### 🔍 Ricerca Rapida

Ricerca tramite:

* Nome del set
* Tipologia
* ID LEGO
* Anno di uscita
* Età consigliata
* Numero di pezzi
* Prezzo

### 💾 Salvataggio dei Dati

* Salvataggio in formato JSON
* Salvataggio con nome personalizzato
* Apertura di collezioni esistenti
* Gestione delle modifiche non salvate

### 🌐 Collegamenti Web

* Apertura diretta del sito ufficiale LEGO
* Controllo preliminare della validità degli URL

### ✅ Validazione dei Dati

Il software verifica automaticamente:

* Compilazione di tutti i campi obbligatori
* Presenza dell'immagine associata
* Unicità dell'ID LEGO
* Correttezza dei dati numerici
* Assenza di valori negativi
* Integrità dei file caricati

---

## 🖥️ Interfaccia Grafica

L'applicazione è composta da diverse finestre dedicate alle principali operazioni.

### 🚀 Schermata Iniziale

Consente di:

* Creare una nuova collezione
* Aprire una collezione esistente

### 📋 Finestra Principale

Include:

* Visualizzazione della collezione
* Barra di ricerca
* Creazione di nuovi set
* Salvataggio dei dati
* Accesso alla documentazione interna

### ✏️ Inserimento e Modifica

Permette la gestione completa delle informazioni relative a ciascun set LEGO:

* Dati identificativi
* Immagine del set
* Prezzo
* Link ufficiale

### ℹ️ Sezione Informazioni

Contiene:

* Descrizione dell'applicazione
* Elenco delle funzionalità disponibili
* Guida rapida all'utilizzo
* Informazioni sull'autore

---

## ⌨️ Comandi Rapidi

| Operazione                  | Azione                      |
| --------------------------- | --------------------------- |
| Modifica di un set          | Doppio clic sulla riga      |
| Eliminazione di un set      | Clic destro sulla riga      |
| Apertura del link ufficiale | Clic sulla colonna Link     |
| Salvataggio dati            | Pulsante **Salva**          |
| Nuovo salvataggio           | Pulsante **Salva con nome** |
| Ricerca set                 | Barra di ricerca            |

---

## 📂 Formato di Salvataggio

I dati vengono memorizzati in formato JSON.

Esempio:

```json id="s1"
[
    {
        "tipologia": "Technic",
        "nome": "Bugatti Chiron",
        "eta": 16,
        "anno": 2018,
        "id": "42083",
        "numero_pezzi": 3599,
        "prezzo": 449.99,
        "link": "https://www.lego.com",
        "immagine": "C:/immagini/bugatti.jpg"
    }
]
```

---

## 🛠️ Tecnologie Utilizzate

### Linguaggio

* Python 3

### Librerie

* CustomTkinter
* Tkinter
* Pillow (PIL)
* Dataclasses
* JSON
* Webbrowser

---

## 📦 Installazione

### Requisiti

* Python 3.10 o superiore
* Sistema operativo compatibile con Python

### Download

Scaricare tutti i file dell'applicazione e conservarli nella stessa cartella.

Per il corretto funzionamento dell'interfaccia grafica devono essere presenti anche:

```text id="s2"
icona.ico
sfondo.png
```

### Installazione delle Dipendenze

```bash id="s3"
pip install customtkinter pillow
```

### Avvio del Programma

```bash id="s4"
python main.py
```

In alternativa è possibile eseguire direttamente il file `main.py` tramite doppio clic.

---

## 👨‍💻 Autore

**Davide Gotti**

Progetto sviluppato a scopo didattico e personale per la gestione di collezioni LEGO tramite interfaccia grafica desktop.

---

## 📄 Licenza

Copyright © 2026 Davide Gotti.

Tutti i diritti riservati.

Il software è stato realizzato per finalità didattiche e formative. Eventuali modifiche, distribuzioni o riutilizzi del codice sorgente devono essere autorizzati dall'autore.
