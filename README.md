# Games Database - Interfaccia Interattiva

Un'applicazione Python interattiva per cercare giochi utilizzando l'API RAWG, con funzionalità avanzate di filtraggio, ordinamento ed esportazione multi-formato.

## 🚀 Funzionalità

### 1. **Interfaccia Testuale Interattiva**
- Menu principale elegante con navigazione tramite frecce
- Input guidato con validazione
- Feedback visivo con emoji e messaggi colorati

### 2. **Ricerca Dinamica per Data**
- Selezione interattiva di anno e mese
- Valori predefiniti per data corrente
- Validazione automatica degli input
- Range supportato: 1970 - anno corrente

### 3. **Filtro Avanzato per Piattaforme**
- **Nessun filtro**: mostra tutti i giochi
- **Lista predefinita**: selezione multipla da piattaforme comuni
  - PC, PlayStation, Xbox, Nintendo Switch
  - iOS, Android, NES, SNES, Game Boy
  - Arcade, Atari, Sega Genesis
- **Input manuale**: inserimento libero di piattaforme personalizzate

### 4. **Ordinamento Flessibile**
- **Data di rilascio**: cronologico
- **Titolo A-Z**: alfabetico crescente
- **Titolo Z-A**: alfabetico decrescente
- **Piattaforma**: per nome piattaforma
- **Nessun ordinamento**: ordine originale API

### 5. **Esportazione Multi-Formato** 🆕
- **CSV**: formato standard per fogli di calcolo
- **Markdown**: tabelle formattate per documenti
- **XLSX**: file Excel nativi con formattazione automatica
- **XML**: struttura gerarchica con metadati
- Nome file personalizzabile
- Encoding UTF-8 per caratteri speciali
- Path assoluto mostrato dopo l'esportazione

## 📦 Installazione

### Prerequisiti
- Python 3.7 o superiore
- Connessione internet (per API RAWG)

### Dipendenze
```bash
pip install requests tabulate questionary python-dotenv openpyxl
```
```

## 🎮 Utilizzo

### Avvio
```bash
python main.py
```

### Menu Principale
1. **🔍 Cerca giochi per data** - Nuova ricerca
2. **📊 Mostra ultimi risultati** - Visualizza l'ultima ricerca
3. **📁 Esporta ultimi risultati in CSV** - Salva su file
4. **❌ Esci** - Chiude l'applicazione

### Flusso Ricerca
1. **Anno**: inserisci anno (1970-2025) o premi Invio per anno corrente
2. **Mese**: inserisci mese (1-12) o premi Invio per mese corrente
3. **Piattaforme**: scegli modalità filtro
4. **Ordinamento**: seleziona criterio di ordinamento
5. **Esportazione**: opzionale salvataggio CSV

## 📋 Formato Dati

### Campi Visualizzati
- **Titolo**: Nome del gioco
- **Piattaforme**: Lista delle piattaforme supportate
- **Data Rilascio**: Data di pubblicazione (YYYY-MM-DD)
- **Generi**: Categorie del gioco

### Esempio Output
```
┌─────────────────────┬──────────────────────┬──────────────┬─────────────────────┐
│ Titolo              │ Piattaforme          │ Data Rilascio│ Generi              │
├─────────────────────┼──────────────────────┼──────────────┼─────────────────────┤
│ Super Mario Bros.   │ NES, Nintendo Switch │ 1985-09-13   │ Platformer, Action  │
│ The Legend of Zelda │ NES, Game Boy        │ 1986-02-21   │ Action, Adventure   │
└─────────────────────┴──────────────────────┴──────────────┴─────────────────────┘
```

## 🔧 Configurazione

### API Key
Il programma usa una chiave API RAWG predefinita. Per utilizzare la tua chiave personale:

1. Registrati su [RAWG.io](https://rawg.io/apidocs)
2. Ottieni la tua API key
3. Modifica la variabile `api_key` in `main.py`

### Personalizzazioni
- **Piattaforme comuni**: modifica la lista `common_platforms` nella classe `GamesDB`
- **Dimensione pagina API**: cambia `page_size=100` nell'URL API
- **Range anni**: modifica il controllo di validazione in `get_year_input()`

## 🐛 Risoluzione Problemi

### Errori Comuni
- **ModuleNotFoundError**: Installa le dipendenze con `pip install -r requirements.txt`
- **API Error**: Verifica la connessione internet e la validità della chiave API
- **Nessun risultato**: Prova con date diverse o rimuovi i filtri piattaforma

### Limitazioni
- Massimo 100 giochi per ricerca (limitazione API)
- Date supportate dalla base dati RAWG
- Alcune piattaforme potrebbero non essere presenti nei dati storici

## 📄 File Generati

### CSV Export
- **Nome predefinito**: `games_results.csv`
- **Colonne**: Title, Platforms, Release Date, Genres
- **Encoding**: UTF-8
- **Separatore**: virgola

## 🤝 Contributi

Funzionalità implementate:
- ✅ Interfaccia interattiva con questionary
- ✅ Input dinamico anno/mese con validazione
- ✅ Filtro piattaforme (lista + manuale)
- ✅ Ordinamento multiplo
- ✅ Esportazione CSV

Per miglioramenti futuri:
- Paginazione risultati
- Cache risultati
- Filtri aggiuntivi (genere, rating)
- Export formati multipli (JSON, Excel)

## 📞 Supporto

Per problemi o suggerimenti, aprire una issue nel repository del progetto.

---
*Powered by RAWG API - The largest video game database*
