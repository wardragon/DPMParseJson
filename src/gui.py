import PySimpleGUI as sg
import datetime
import threading
import time

# Simulazione della funzione splitJson
def splitJson():
    sg.popup("splitJson eseguita!")

# Funzione per aggiornare l'orologio in tempo reale
def update_time(window):
    while True:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Formato orologio
        window['-TIME-'].update(current_time)
        time.sleep(1)

# Funzione principale per lanciare l'interfaccia GUI
def launchGui():
    # Layout dell'interfaccia
    layout = [
        [
            sg.Column([
                [sg.Text('', size=(8, 1), font=('Helvetica', 48), justification='center', key='-TIME-')],
            ]),
            sg.Column([
                [sg.Button('Genera', key='-GENERA-', size=(10, 2), font=('Helvetica', 14))],
                [sg.Button('Esci', key='-ESCI-', size=(10, 2), font=('Helvetica', 14))]
            ])
        ]
    ]

    # Creazione della finestra
    window = sg.Window('DPM JSON Generator', layout, finalize=True)

    # Thread per l'aggiornamento dell'orologio
    threading.Thread(target=update_time, args=(window,), daemon=True).start()

    # Ciclo dell'evento
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-ESCI-':
            break
        elif event == '-GENERA-':
            splitJson()

    # Chiudi la finestra
    window.close()

