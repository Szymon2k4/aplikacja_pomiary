import customtkinter as ctk

def wybrano_wartosc(choice):
    print("Wybrano:", choice)

root = ctk.CTk()
root.geometry("300x200")

# Tworzymy ramkę (CTkFrame)
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Etykieta w ramce
label = ctk.CTkLabel(frame, text="Wybierz opcję:")
label.pack(pady=5)

# Lista rozwijana w ramce
combo = ctk.CTkComboBox(frame, values=["Opcja 1", "Opcja 2", "Opcja 3"], command=wybrano_wartosc)
combo.pack(pady=5)

root.mainloop()
