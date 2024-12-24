import asyncio
import time
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from threading import Thread
import shutil

from bs4 import BeautifulSoup


async def download_keys():
    # Specifica il nome del file HTML
    html_file = 'keySite.html'

    # Cartella contenente i file .iso
    iso_folder = "ISOs"
    # Cartella per le chiavi .dkey
    keys_folder = "keys"

    # Creazione delle cartelle se non esistono
    if not os.path.exists(iso_folder):
        os.makedirs(iso_folder)
        append_log(f"La cartella '{iso_folder}' è stata creata.")
    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder)
        append_log(f"La cartella '{keys_folder}' è stata creata, download delle chiavi...")

    if not os.path.exists(html_file):
        append_log(f"Errore: il file {html_file} non trovato.")
        time.sleep(3)
        for i in range(5, -1, -1):
            append_log(f"chiusura GUI tra: {i} secondo..." if i == 1 else f"chiusura GUI tra: {i} secondi...")
            time.sleep(1)
            if i == 1:
                break
        root.destroy()
        return

    # Leggi il contenuto del file HTML
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse del contenuto HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trova tutte le righe della tabella (tr)
    rows = soup.find_all('tr')

    # Crea la cartella 'keys' se non esiste
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Itera su ogni riga della tabella
    for row in rows:
        # Trova tutte le celle (td) nella riga
        cells = row.find_all('td')

        # Se ci sono almeno 6 celle (l'ultima dovrebbe essere la dkey)
        if len(cells) > 5:
            # Estrai il nome (prima cella) e la dkey (ultima cella)
            nome = cells[1].get_text(strip=True)
            dkey = cells[5].get_text(strip=True)

            # Rimuovi la parola ".iso" dalla dkey
            nome = nome.replace('.iso', '')

            # Crea un file .dkey nella cartella 'keys' con il nome della chiave
            filename = f'keys/{nome}.dkey'

            # Scrivi la dkey nel file
            with open(filename, 'w', encoding='utf-8') as key_file:
                key_file.write(dkey)
    append_log("Download delle chiavi completato.")

def set_inputs_state(state):
    """Abilita o disabilita gli input e i bottoni."""
    start_button.config(state=state)


def append_log(message):
    log_console.config(state=tk.NORMAL)
    log_console.insert(tk.END, message + "\n")
    log_console.see(tk.END)
    log_console.config(state=tk.DISABLED)


def show_log_console():
    log_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
    log_console.grid(row=4, column=0, columnspan=3, padx=10, pady=10)


def run_command_in_thread(command, iso_path, decrypted_filename):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            append_log(line.strip())
        for line in process.stderr:
            append_log(f"ERRORE: {line.strip()}")
        process.wait()
        if process.returncode == 0:
            append_log("Comando eseguito con successo!")
            decrypted_path = os.path.join(os.path.dirname(iso_path), decrypted_filename)

            # Verifica se il file decriptato esiste
            if os.path.exists(decrypted_path):
                append_log(f"File decriptato trovato in: {decrypted_path}")

                # Creazione della cartella Decrypted se non esiste
                decrypted_folder = os.path.join(os.path.dirname(iso_path), "Decrypted")
                if not os.path.exists(decrypted_folder):
                    os.makedirs(decrypted_folder)
                    append_log(f"La cartella 'Decrypted' è stata creata.")

                # Spostamento del file decriptato
                try:
                    shutil.move(str(decrypted_path), os.path.join(decrypted_folder, decrypted_filename))
                    append_log(f"File decriptato spostato in: {decrypted_folder}")
                except Exception as e:
                    append_log(f"Errore durante lo spostamento del file: {e}")
            else:
                append_log(f"Il file decriptato {decrypted_filename} non è stato trovato!")
        else:
            append_log(f"Il comando è terminato con codice di errore {process.returncode}")
    except Exception as e:
        append_log(f"Errore imprevisto: {e}")
    finally:
        set_inputs_state(tk.NORMAL)  # Riabilita gli input alla fine


def start_command():
    # Cartella contenente i file .iso
    iso_folder = "ISOs"
    # Cartella per le chiavi .dkey
    keys_folder = "keys"

    iso_files = [f for f in os.listdir(iso_folder) if f.endswith(".iso")]

    if not iso_files:
        messagebox.showerror("Errore", f"Nessun file .iso trovato nella cartella '{iso_folder}'!")
        return

    append_log(f"Trovati {len(iso_files)} file .iso nella cartella '{iso_folder}'.")

    # Per ogni file ISO, esegui il comando di decrittazione
    for iso_file in iso_files:
        iso_path = os.path.join(iso_folder, iso_file)
        # Rimuovi l'estensione .iso dal nome del file per trovare la chiave .dkey
        base_name = os.path.splitext(iso_file)[0]
        dkey_path = os.path.join(keys_folder, f"{base_name}.dkey")

        # Verifica se il file .dkey esiste
        if not os.path.exists(dkey_path):
            append_log(f"Chiave non trovata per {iso_file}, salto il file.")
            continue

        append_log(f"Trovata chiave per {iso_file}, eseguo il comando.")

        # Leggi il contenuto del file .dkey
        with open(dkey_path, "r") as dkey_file:
            dkey_content = dkey_file.read().strip()

        # Nuovo nome per il file decriptato (aggiungiamo _decrypted)
        decrypted_filename = f"{base_name}.iso_decrypted.iso"

        # Esegui il comando ps3dec con la chiave
        command = f"ps3dec -i \"{iso_path}\" -d \"{dkey_content}\" --skip"
        append_log(f"Esecuzione comando su: {iso_path}")
        set_inputs_state(tk.DISABLED)  # Disabilita gli input durante l'esecuzione del comando
        Thread(target=run_command_in_thread, args=(command, iso_path, decrypted_filename), daemon=True).start()

async def run_after_gui():
    await asyncio.sleep(0.1)
    await download_keys()

def start_asyncio_loop():
    asyncio.run(run_after_gui())

# Creazione della finestra principale
root = tk.Tk()
root.title("PS3 Decrypter GUI")
root.resizable(False, False)

# Creazione della console di log
log_label = tk.Label(root, text="Console log:")
log_console = tk.Text(root, height=15, width=80, state=tk.DISABLED, bg="black", fg="white")

# Log console visibile fin dall'inizio
show_log_console()

# Start button
start_button = tk.Button(root, text="Inizia", command=start_command, bg="green", fg="white")
start_button.grid(row=2, column=0, columnspan=3, pady=20)

thread = Thread(target=start_asyncio_loop, daemon=True)
thread.start()

root.mainloop()