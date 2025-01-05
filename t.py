import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("300x400")
        self.title("Auto-scroll Frame")

        # Tworzymy scrollowalną ramkę
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=250, height=300)
        self.scrollable_frame.pack(pady=20, padx=20)

        # Przycisk do dodawania nowych elementów
        self.add_button = ctk.CTkButton(self, text="Dodaj element", command=self.add_item)
        self.add_button.pack(pady=10)

        # Licznik elementów
        self.item_count = 0

    def add_item(self):
        # Dodajemy nowy element do scrollowalnej ramki
        self.item_count += 1
        label = ctk.CTkLabel(self.scrollable_frame, text=f"Element {self.item_count}")
        label.pack(pady=5)

        # Automatyczne przewijanie na dół
        self.scrollable_frame.update_idletasks()
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)
       

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = App()
    app.mainloop()
