import PySimpleGUI as sg
import datetime
import threading
import time
import configparser
import io
import sys
from splitJson import *  # Importa tutto il contenuto dal modulo splitJson
from pathlib import Path

# Funzione per ottenere la data corrente
def current_date_str():
    return datetime.datetime.now().strftime('%Y%m%d')

# Funzione per leggere il file di configurazione
def load_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    if not config.has_section('Settings'):
        config.add_section('Settings')
    return config

# Funzione per scrivere il file di configurazione
def save_config(values, filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    if not config.has_section('Settings'):
        config.add_section('Settings')
    for key, value in values.items():
        config.set('Settings', key.lower(), str(value))
    with open(filename, 'w') as configfile:
        config.write(configfile)

# Funzione per aggiornare l'orologio in tempo reale
def update_time(window):
    while True:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        window['-TIME-'].update(current_time)
        time.sleep(1)

# Funzione per eseguire splitJson e visualizzare l'output in tempo reale
def run_splitjson_and_show_output(input_file, url, sun, output_file_nouni, output_file_uni, json_file_out):
    # Layout della finestra di output
    output_layout = [
        [sg.Multiline(size=(80, 20), key='-OUTPUT-', font=('Courier New', 10), autoscroll=True, disabled=True)],
        [sg.Button('Chiudi', key='-CLOSE-', size=(10, 1), font=('Helvetica', 12), pad=((450, 0), (10, 10)))]
    ]
    output_window = sg.Window('Output SplitJson', output_layout, modal=True, finalize=True)

    # Cattura l'output di console
    buffer = io.StringIO()
    sys.stdout = buffer  # Reindirizza stdout al buffer

    # Avvia splitJson in un thread separato
    def run_splitJson():
        try:
            splitJson(input_file, url, sun, output_file_nouni, output_file_uni, json_file_out)
        finally:
            sys.stdout = sys.__stdout__  # Ripristina stdout

    thread = threading.Thread(target=run_splitJson, daemon=True)
    thread.start()

    # Aggiorna la finestra con l'output di console in tempo reale
    while thread.is_alive() or buffer.tell() > 0:
        output_text = buffer.getvalue()  # Ottiene il contenuto attuale del buffer
        output_window['-OUTPUT-'].update(output_text)
        event, _ = output_window.read(timeout=100)
        if event == '-CLOSE-':
            break

    output_window.close()
    thread.join()  # Assicurati che il thread finisca
    sys.stdout = sys.__stdout__  # Ripristina stdout

# Funzione principale per lanciare l'interfaccia GUI
def launchGui():
    # Carica le impostazioni dal file config.ini
    config = load_config()
    path=Path.home() / "Documents"
    # Definizione dei valori di default delle variabili e dei tooltip
    variables_info = {
        "input_file": ("", "Percorso del file di input."),
        "output_file_nouni": (path / f"nouniroma1-{current_date_str()}.xlsx", "Nome del file di output senza univocità."),
        "output_file_uni": (path / f"uniroma1-{current_date_str()}.xlsx", "Nome del file di output con univocità."),
        "json_file_out": (path / f"data-to-import-{current_date_str()}.json", "Nome del file JSON di output."),
        "url": ("https://services.uniroma1.it/api/1.0/people-ict-view", "URL per recuperare i dati."),
        "sun": (True, "Attiva/disattiva l'opzione Sun.")
    }

    # Imposta i valori caricati dal file di configurazione o usa quelli di default
    initial_values = {}
    for var_name, (default_value, _) in variables_info.items():
        if config.has_option('Settings', var_name):
            initial_values[var_name] = config.get('Settings', var_name)
            if var_name == 'sun':
                initial_values[var_name] = config.getboolean('Settings', var_name)
        else:
            initial_values[var_name] = default_value

    # Layout dell'interfaccia
    layout = [
        [
            sg.Column([
                [sg.Text('', size=(8, 1), font=('Helvetica', 48), justification='center', key='-TIME-')],
                *[
                    [sg.Text(var_name, size=(15, 1)), 
                     sg.Input(default_text=initial_values[var_name], tooltip=variables_info[var_name][1], key=f'-{var_name.upper()}-', size=(60, 1), enable_events=True)]
                    for var_name in variables_info
                ],
                [sg.Button('Salva', key='-SALVA-', visible=False, size=(10, 1), font=('Helvetica', 14))]
            ]),
            sg.Column([
                [sg.Button('Genera', key='-GENERA-', size=(10, 2), font=('Helvetica', 14))],
                [sg.Button('Esci', key='-ESCI-', size=(10, 2), font=('Helvetica', 14))]
            ])
        ]
    ]

    # Creazione della finestra
    window = sg.Window('Interfaccia SplitJson con Orologio e Variabili', layout, finalize=True)

    # Thread per l'aggiornamento dell'orologio
    threading.Thread(target=update_time, args=(window,), daemon=True).start()

    # Ciclo dell'evento
    modified = False  # Flag per tracciare modifiche
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-ESCI-':
            break
        elif event == '-GENERA-':
            # Recupera i valori dai campi di input
            input_file = values['-INPUT_FILE-']
            output_file_nouni = values['-OUTPUT_FILE_NOUNI-']
            output_file_uni = values['-OUTPUT_FILE_UNI-']
            json_file_out = values['-JSON_FILE_OUT-']
            url = values['-URL-']
            sun = values['-SUN-'] in ('True', 'true', '1', True)

            # Esegui splitJson e mostra l'output in una finestra separata
            run_splitjson_and_show_output(input_file, url, sun, output_file_nouni, output_file_uni, json_file_out)

        # Mostra il pulsante "Salva" se una variabile è stata modificata
        if event.startswith('-') and event.endswith('-'):
            modified = True
            window['-SALVA-'].update(visible=True)

        # Salva i valori nel file config.ini quando si clicca "Salva"
        if event == '-SALVA-' and modified:
            try:
                config_values = {k[1:-1].lower(): v for k, v in values.items() if k.startswith('-') and k.endswith('-')}
                save_config(config_values)
                sg.popup("Configurazione salvata con successo!", title="Esito del Salvataggio", button_type=sg.POPUP_BUTTONS_OK)
                window['-SALVA-'].update(visible=False)
                modified = False
            except Exception as e:
                sg.popup_error(f"Errore nel salvataggio della configurazione: {e}")

    window.close()
