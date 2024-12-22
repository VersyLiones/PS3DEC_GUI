
# PS3 Decrypter GUI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Un'applicazione GUI per decrittare i file `.iso` della PS3 utilizzando le chiavi `.dkey`. Questa applicazione automatizza il processo di decrittazione e gestisce i file `.iso` e `.dkey` in modo organizzato.

---

## Requisiti

- Python 3.8 o superiore
- Moduli richiesti (installabili con `pip install -r requirements.txt`):
  - `bs4`
  - `tkinter` (integrato con Python standard)
  - `shutil` (integrato con Python standard)

---

## Passaggi per l'installazione

1. **Clona il repository o scarica i file:**

   ```bash
   git clone https://github.com/tuo-utente/ps3-decrypter-gui.git
   cd ps3-decrypter-gui
   ```

2. **Installa i moduli richiesti:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepara i file necessari:**

   - Posiziona i file `.iso` nella cartella `ISOs`.
   - Posiziona un file HTML contenente le chiavi nella directory principale e rinominalo `keySite.html`.

4. **Esegui l'applicazione:**

   ```bash
   python main.py
   ```

---

## Utilizzo

1. **Scaricare le chiavi:**  
   Durante l'avvio, l'applicazione leggerà il file `keySite.html` e creerà i file `.dkey` nella cartella `keys`.

2. **Decrittazione automatica:**  
   - Tutti i file `.iso` nella cartella `ISOs` verranno elaborati.  
   - Se una chiave `.dkey` corrispondente è disponibile nella cartella `keys`, il file `.iso` sarà decriptato.

3. **Gestione automatica dei file:**  
   - I file `.iso` decriptati (ad esempio, `game.iso_decrypted.iso`) saranno spostati nella sottocartella `ISOs/Decrypted`.

---

## Funzionalità

- **Download automatico delle chiavi:**  
  Le chiavi sono generate leggendo il file HTML e salvate come file `.dkey`.
- **Decrittazione batch:**  
  Elaborazione automatica di tutti i file `.iso` disponibili.
- **Gestione file:**  
  I file decriptati sono spostati in una cartella dedicata.

---

## Licenza

Questo progetto è rilasciato sotto la licenza MIT. Consulta il file [LICENSE](LICENSE) per maggiori informazioni.

---

## Contatti

- **Autore:** [Il tuo nome o username GitHub](https://github.com/tuo-utente)
- **Email:** tuoemail@example.com
