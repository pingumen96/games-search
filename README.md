# Games Database - Interfaccia Interattiva con AI

Un'applicazione Python interattiva per cercare giochi utilizzando l'API RAWG, con funzionalità avanzate di filtraggio, ordinamento, esportazione multi-formato e **recensioni AI generate da OpenAI**.

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

### 4. **🤖 Recensioni AI (NOVITÀ!)**
- **Recensioni automatiche** generate da OpenAI GPT-3.5
- **Voti da 1 a 10** per ogni gioco
- **Analisi contestuale** basata su genere, piattaforme e data di rilascio
- **Feature opzionale** - attivabile durante la ricerca
- Richiede API key OpenAI (configurabile in `.env`)

### 5. **Ordinamento Flessibile**
- **Data di rilascio**: cronologico
- **Titolo A-Z**: alfabetico crescente
- **Titolo Z-A**: alfabetico decrescente
- **Piattaforma**: per nome piattaforma
- **Nessun ordinamento**: ordine originale API

### 6. **Esportazione Multi-Formato** 🆕
- **CSV**: formato standard per fogli di calcolo
- **Markdown**: tabelle formattate per documenti
- **XLSX**: file Excel nativi con formattazione automatica
- **XML**: struttura gerarchica con metadati
- **Include recensioni AI** se generate
- Nome file personalizzabile
- Encoding UTF-8 per caratteri speciali
- Path assoluto mostrato dopo l'esportazione

## 📦 Installazione

### Prerequisiti
- Python 3.7 o superiore
- Connessione internet (per API RAWG)

### Dipendenze
```bash
pip install requests tabulate questionary python-dotenv openpyxl openai
```

### Configurazione API Keys

1. **Copia il file di esempio:**
```bash
cp .env.example .env
```

2. **Configura le API Keys nel file `.env`:**
```env
# RAWG API Key (Obbligatoria)
RAWG_API_KEY=your_rawg_api_key_here

# OpenAI API Key (Opzionale - per recensioni AI)
OPENAI_API_KEY=your_openai_api_key_here
```

#### Come ottenere le API Keys:

**RAWG API Key (Gratuita - Obbligatoria):**
1. Registrati su [https://rawg.io/apidocs](https://rawg.io/apidocs)
2. Ottieni la tua API key gratuita
3. Inseriscila nel file `.env`

**OpenAI API Key (A pagamento - Opzionale):**
1. Vai su [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crea un account e genera una API key
3. Inseriscila nel file `.env`
4. **Nota**: Le recensioni AI comportano un costo per token utilizzato
```

## 🎮 Utilizzo

### Avvio
```bash
python main.py
```

### Menu Principale
1. **🔍 Cerca giochi per data** - Nuova ricerca
2. **📊 Mostra ultimi risultati** - Visualizza l'ultima ricerca
3. **📁 Esporta ultimi risultati** - Salva in vari formati
4. **❌ Esci** - Chiude l'applicazione

### Flusso Ricerca
1. **Anno**: inserisci anno (1970-2025) o premi Invio per anno corrente
2. **Mese**: inserisci mese (1-12) o premi Invio per mese corrente
3. **Piattaforme**: scegli modalità filtro
4. **🤖 Recensioni AI**: scegli se generare recensioni automatiche (opzionale)
5. **Ordinamento**: seleziona criterio di ordinamento
6. **Esportazione**: salvataggio in formato preferito (CSV/Markdown/XLSX/XML)

## 📋 Formato Dati

### Campi Visualizzati
- **Titolo**: Nome del gioco
- **Piattaforme**: Lista delle piattaforme supportate
- **Data Rilascio**: Data di pubblicazione (YYYY-MM-DD)
- **Generi**: Categorie del gioco
- **🤖 Recensione AI**: Mini-recensione generata da OpenAI (opzionale)
- **🤖 Voto AI**: Valutazione da 1 a 10 (opzionale)

### Esempio Output (con AI)
```
┌─────────────────────┬──────────────────┬─────────────┬──────────────┬──────────────────────────┬─────────┐
│ Titolo              │ Piattaforme      │ Data Rilascio│ Generi       │ Recensione AI            │ Voto AI │
├─────────────────────┼──────────────────┼─────────────┼──────────────┼──────────────────────────┼─────────┤
│ Super Mario Bros    │ NES, Switch      │ 1985-09-13  │ Platform     │ Un capolavoro senza tem..│ 9/10    │
│ The Legend of Zelda │ NES, Game Boy    │ 1986-02-21  │ Action, Adv  │ L'inizio di una saga l...│ 8/10    │
└─────────────────────┴──────────────────┴─────────────┴──────────────┴──────────────────────────┴─────────┘
```

### Esempio Recensione AI Completa
```
Titolo: Super Mario Bros
Recensione AI: "Un capolavoro del platform che ha rivoluzionato l'industria videoludica.
Gameplay intuitivo, level design perfetto e colonna sonora indimenticabile rendono
questo titolo un'esperienza senza tempo che continua a divertire dopo decenni."
Voto AI: 9/10
```

## ⚡ Performance e Costi

### Recensioni AI
- **Tempo**: ~2-3 secondi per recensione
- **Costo**: ~$0.001-0.002 per recensione (dipende dalla lunghezza)
- **Modello**: GPT-3.5-turbo (veloce ed economico)
- **Limite**: Raccomandato max 50 giochi per sessione

### Consigli per l'Uso
- Usa le recensioni AI per ricerche mirate (pochi giochi di qualità)
- Per ricerche ampie, evita le recensioni AI per contenere i costi
- Le recensioni sono generate in italiano e contestualizzate

## 🆕 Novità della Versione

### v2.0 - AI Integration
- ✅ Recensioni AI con OpenAI GPT-3.5
- ✅ Voti automatici da 1 a 10
- ✅ Esportazione multi-formato (CSV, MD, XLSX, XML)
- ✅ Supporto recensioni AI in tutti i formati di export
- ✅ Configurazione flessibile tramite file .env
- ✅ Gestione errori migliorata per API esterne
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
