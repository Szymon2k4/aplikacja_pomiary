import customtkinter as ctk

# Tworzenie głównego okna
root = ctk.CTk()
root.geometry("500x400")

# Ramka jako nagłówek
header_frame = ctk.CTkFrame(root)
header_frame.pack(fill="x", padx=20, pady=(20, 0))  # Na szerokość okna

# Podział nagłówka na 3 kolumny
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

# Dodanie etykiet do kolumn
ctk.CTkLabel(header_frame, text="Kolumna 1", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
ctk.CTkLabel(header_frame, text="Kolumna 2", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)
ctk.CTkLabel(header_frame, text="Kolumna 3", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, pady=5)

# Tworzenie przewijanej ramki
scrollable_frame = ctk.CTkScrollableFrame(root)
scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Podział przewijanej ramki na kolumny
scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)
scrollable_frame.grid_columnconfigure(2, weight=1)

# Dodanie przykładowych danych do kolumn
for i in range(10):
    ctk.CTkLabel(scrollable_frame, text=f"Dane {i+1}A").grid(row=i, column=0, padx=10, pady=5)
    ctk.CTkLabel(scrollable_frame, text=f"Dane {i+1}B").grid(row=i, column=1, padx=10, pady=5)
    ctk.CTkLabel(scrollable_frame, text=f"Dane {i+1}C").grid(row=i, column=2, padx=10, pady=5)

root.mainloop()
