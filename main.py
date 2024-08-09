import tkinter as tk
from tkinter import messagebox
import re
import random
from datetime import datetime
from testscript import sayhello

# Initialer Wert für den BatchCounter
batch_counter = 1


# Funktion zum Setzen des Fokus auf das nächste Widget
def focus_next_widget(event):
    # Die Methode 'focus_set()' wird auf das nächste Widget angewendet
    next_widget = event.widget.tk_focusNext()
    next_widget.focus_set()

    # Wenn das nächste Widget der Button ist, dann wird der Button direkt geklickt
    if next_widget == label_config:
        button_generate.invoke()

    return "break"  # Verhindert das Standardverhalten der Eingabetaste


# Funktion zum Generieren eines Zufallswerts im Format X_e_Y
def generate_custom_random_value():
    first_char = random.randint(0, 9)  # Zufallszahl von 0 bis 9
    last_char = random.randint(0, 9)  # Zufallszahl von 0 bis 9
    return f"{first_char}e{last_char}"


# Funktion zum Formatieren der BatchNumber, BatchCounter und MaterialNumber entsprechend der Länge
def format_length(value, length, pad_char='0'):
    return value.rjust(length, pad_char)[:length]


# Funktion zum Generieren der aktuellen Zeit im Format yyMMdd
def get_current_timestamp():
    now = datetime.now()
    return now.strftime("%d%m%y")


# Funktion zum Generieren der Serialnummer
def generate_serial_number():
    global batch_counter
    try:
        # Benutzereingaben holen
        batch_number = entry_batch_number.get()
        material_number = entry_material_number.get()
        batch_number_length = 10  # Standardwert, falls nicht angegeben
        batch_counter_length = 7  # Standardwert, falls nicht angegeben

        # Länge von BatchNumber und BatchCounter extrahieren
        batch_number_match = re.search(r'\{BatchNumber:PadLeft:(\d+):0\}', entry_order.get())
        if batch_number_match:
            batch_number_length = int(batch_number_match.group(1))

        batch_counter_match = re.search(r'\{BatchCounter:PadLeft:(\d+):0\}', entry_order.get())
        if batch_counter_match:
            batch_counter_length = int(batch_counter_match.group(1))

        # MaterialNumber einfach nur erkennen und formatieren, ohne eine Gruppe zu verwenden
        material_number_match = re.search(r'\{MaterialNumber:NoFormat:0:0\}', entry_order.get())
        if material_number_match:
            formatted_material_number = material_number  # MaterialNumber so wie sie ist übernehmen
        else:
            formatted_material_number = ''  # Wenn kein Platzhalter gefunden wird, leer setzen

        # BatchNumber formatieren
        formatted_batch_number = format_length(batch_number, batch_number_length)

        # BatchCounter formatieren
        formatted_batch_counter = format_length(f"{batch_counter}", batch_counter_length)

        # Reihenfolge der Komponenten festlegen
        order = entry_order.get()

        # FixedText automatisch extrahieren und ersetzen
        def replace_fixed_text(match):
            return match.group(1) or ''

        # InsertValue automatisch generieren und ersetzen
        def replace_insert_value(match):
            return generate_custom_random_value()

        # TimeStamp automatisch generieren und ersetzen
        def replace_timestamp(match):
            return get_current_timestamp()

        # Platzhalter in der Serialnummer ersetzen
        serial_number = re.sub(r'\{FixedText:(.*?)\}', replace_fixed_text, order)
        serial_number = re.sub(r'\{InsertValue:NoFormat:0\}', replace_insert_value, serial_number)
        serial_number = re.sub(r'\{TimeStamp:TimeFormat:yyMMdd\}', replace_timestamp, serial_number)
        serial_number = re.sub(r'\{BatchNumber:PadLeft:\d+:0\}', formatted_batch_number, serial_number)
        serial_number = re.sub(r'\{BatchCounter:PadLeft:\d+:0\}', formatted_batch_counter, serial_number)
        serial_number = re.sub(r'\{MaterialNumber:NoFormat:0:0\}', formatted_material_number, serial_number)

        # Eingetragene Konfiguration anzeigen
        # label_config.config(text="{FixedText:|}{BatchNumber:PadLeft:10:0}{BatchCounter:PadLeft:7:0}{InsertValue:NoFormat:0}{BatchNumber:PadLeft:10:0}{MaterialNumber:NoFormat:0:0}{TimeStamp:TimeFormat:yyMMdd}")

        # Serialnummer in das Label einfügen
        label_serial_number.config(text=serial_number)

        # BatchCounter erhöhen
        batch_counter += 1
    except ValueError:
        messagebox.showerror("Eingabefehler", "Bitte geben Sie gültige Zahlen ein!")

print("hi")


def print_hi_two_times():
    print("hi")
    print("hi")

print_hi_two_times()
sayhello()

# print("hi")
 # print("hi")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Pattern Creator")

# Fenstergröße und Hintergrundfarbe anpassen
root.geometry("1500x400")
root.configure(bg="#f0f0f0")

# Icon setzen (passen Sie den Dateinamen und Pfad an)
try:
    icon_image = tk.PhotoImage(file='Witzenmann_Icon.png')  # Oder 'icon.ico' für Windows
    root.iconphoto(False, icon_image)
except tk.TclError:
    print("Icon-Datei nicht gefunden.")

# Frames erstellen, um Widgets dynamisch anzupassen
frame_top = tk.Frame(root, bg="#e0e0e0")
frame_top.pack(fill="x", padx=20, pady=10)
frame_top.grid_rowconfigure(0, weight=1)
frame_top.grid_columnconfigure(1, weight=1)

frame_middle = tk.Frame(root, bg="#e0e0e0")
frame_middle.pack(fill="x", padx=20, pady=10)
frame_middle.grid_rowconfigure(0, weight=1)
frame_middle.grid_columnconfigure(1, weight=1)

frame_bottom = tk.Frame(root, bg="#e0e0e0")
frame_bottom.pack(fill="both", expand=True, padx=20, pady=10)
frame_bottom.grid_rowconfigure(1, weight=1)
frame_bottom.grid_columnconfigure(0, weight=1)

# Verhindern, dass die Frames automatisch die Größe der enthaltenen Widgets übernehmen
# frame_top.pack_propagate(False)
# frame_middle.pack_propagate(False)
# frame_bottom.pack_propagate(False)

# Styling für Labels und Textboxen
label_font = ("Segoe UI", 14)
button_font = ("Segoe UI", 14, "bold")
entry_font = ("Segoe UI", 12)

# Labels und Eingabefelder
label_batch_number = tk.Label(frame_top, text="Batch:", font=label_font, bg="#f0f0f0", width="7")
label_batch_number.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_batch_number = tk.Entry(frame_top, font=entry_font, width=30)
entry_batch_number.grid(row=0, column=1, padx=5, pady=5, sticky="we")

label_material_number = tk.Label(frame_top, text="Material:", font=label_font, bg="#f0f0f0", width="7")
label_material_number.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_material_number = tk.Entry(frame_top, font=entry_font, width=30)
entry_material_number.grid(row=1, column=1, padx=5, pady=5, sticky="we")

label_order = tk.Label(frame_middle, text="Konfig:", font=label_font, bg="#f0f0f0", width="7")
label_order.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_order = tk.Entry(frame_middle, font=entry_font, width=186)
entry_order.grid(row=0, column=1, padx=5, pady=5, sticky="we")

# Button zum Generieren der Serialnummer
button_generate = tk.Button(frame_bottom, text="Serialnummer generieren", font=button_font,
                            command=generate_serial_number, bg="#4CAF50", fg="white")
button_generate.grid(row=0, columnspan=2, padx=5, pady=10)

# Label zur Anzeige der eingetragenen Konfiguration
label_config = tk.Entry(frame_middle, justify="center", font=("Helvetica", 12, "italic"), bg="#f0f0f0",
                        readonlybackground="#f0f0f0", borderwidth=0)
label_config.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Beispieltext einfügen
label_config.insert(0,
                    "{FixedText:|}{BatchNumber:PadLeft:10:0}{BatchCounter:PadLeft:7:0}{InsertValue:NoFormat:0}{BatchNumber:PadLeft:10:0}{MaterialNumber:NoFormat:0:0}{TimeStamp:TimeFormat:yyMMdd}")
label_config.config(state="readonly")

# Label zur Anzeige der generierten Serialnummer
label_serial_number = tk.Label(frame_bottom, text="", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
label_serial_number.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

# Fenstergröße anpassen und Frames dynamisch skalieren
root.update_idletasks()

# Binden der Eingabetaste (Enter) an die Textboxen
entry_batch_number.bind("<Return>", focus_next_widget)
entry_material_number.bind("<Return>", focus_next_widget)
entry_order.bind("<Return>", focus_next_widget)
# label_config.bind("<Return>", focus_next_widget)
button_generate.bind("<Return>", focus_next_widget)

# Hauptfenster starten
root.mainloop()
