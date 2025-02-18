import customtkinter as ctk
import uuid  # Generowanie unikalnych ID

# Tworzymy główne okno
root = ctk.CTk()
root.geometry("300x200")

# Słownik przechowujący {unikalne_id: przycisk}
buttons = {}

# Funkcja obsługująca kliknięcie przycisku
def button_clicked(button_id):
    print(f"Kliknięto przycisk o ID: {button_id}")  # Wyświetlenie ID w konsoli

# Tworzenie 3 przycisków
for i in range(3):
    button_id = str(uuid.uuid4())  # Generowanie unikalnego ID
    btn = ctk.CTkButton(root, text=f"Przycisk {i+1}", command=lambda id=button_id: button_clicked(id))
    btn.pack(pady=5)
    buttons[button_id] = btn  # Dodanie do słownika

root.mainloop()
