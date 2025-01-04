import customtkinter as ctk
from pomiar import Pomiar

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Pomiary Elektryczne')
        self.geometry('1200x600')
        self.parameters() 
        self.main_window()


    # paramtery
    def parameters(self):
        
        #fonts
        self.font_arial18 = ctk.CTkFont(family="Arial", 
                      size=18,
                      weight="bold", 
                      slant="roman", 
                      ) 
        
        self.font_arial15 = ctk.CTkFont(family="Arial", 
                      size=15, 
                      slant="roman", 
                      )
        self.font_arial16 = ctk.CTkFont(family="Arial",
                        size=16,
                        slant="italic",
                        weight="bold",
                        )
        
        self.font_arial12 = ctk.CTkFont(family="Arial", 
                      size=12, 
                      slant="roman", 
                      )
        
        def limit_text_25_name(*args):
            current_text = self.entry_name_variable.get()
            
            if len(current_text) > 25:  
                self.entry_name_variable.set(current_text[:25])  
        
        self.entry_name_variable = ctk.StringVar()
        self.entry_name_variable.trace_add("write", limit_text_25_name)  


        def limit_text_2_fuse(*args):
            current_text = self.entry_fuse_variable.get()
            if len(current_text) > 2:  
                self.entry_fuse_variable.set(current_text[:2]) 
            try:
                int(current_text[-1])
            except ValueError:
                self.entry_fuse_variable.set(current_text[:-1])
            except IndexError:
                pass

             
        
        self.entry_fuse_variable = ctk.StringVar()
        self.entry_fuse_variable.trace_add("write", limit_text_2_fuse)

        
        def limit_text_4_ipz(*args):
            current_text = self.entry_ipz_variable.get()

            if len(current_text) > 4:  
                self.entry_ipz_variable.set(current_text[:4])  
        
            try:
                s = ['.', ',']
                if current_text[-1] in s and not (s[0] in current_text[:-1] or s[1] in current_text[:-1]):
                    pass
                else:
                    int(current_text[-1])
            except ValueError:
                self.entry_ipz_variable.set(current_text[:-1])
            except IndexError:
                pass

        
        self.entry_ipz_variable = ctk.StringVar()
        self.entry_ipz_variable.trace_add("write", limit_text_4_ipz)
        
        

    # obsluga glownego okna
    def main_window(self):
        self.main_tab = ctk.CTkTabview(self,
                                   width=1150,
                                   height=500,
                                   anchor = 'w')
        self.main_tab.grid(row=0, column=0, padx=25, pady=20, sticky="ew", columnspan=3)

        # przyciski ogólne
        self.button1 = ctk.CTkButton(self, text="myn")
        self.button1.grid(row=1, column=0, padx=0, pady=5)

        self.button2 = ctk.CTkButton(self, text="my button")
        self.button2.grid(row=1, column=1, padx=0, pady=5)

        self.button3 = ctk.CTkButton(self, text="my button3")
        self.button3.grid(row=1, column=2, padx=0, pady=5)

        # zakładki
        self.tab1 = self.main_tab.add("Obwód jednofazowy",)
        self.tab2 = self.main_tab.add("Obwód jednofazowy2")
        self.tab3 = self.main_tab.add("Obwód trzyfazowy")

        self.tabnames = ["Obwód jednofazowy", "Obwód jednofazowy2", "Obwód trzyfazowy"]

        # wywołanie funkcji do obsługi zakładek
        
        self.tab1_window()
    

    # obsluga pierwszej zakladki
    def tab1_window(self):    
        # funkcja do obslugi klawiszy
        def kliknij_klaiwsz(event):
            if self.main_tab.get() == self.tabnames[0]:
                if self.tab1.frame1.calculate_button.cget("state") == "normal":
                    calculate()
                elif self.tab1.frame2.add_measurement_button.cget("state") == "normal":
                    add_measurement()
                else:
                    pass
                
        self.bind("<Return>", kliknij_klaiwsz)

        #funkcje do obslugi okna
        def calculate():
            # sprawdzenie czy wszystkie pola są wypełnione
            if self.tab1.frame1.entry_circuit_name.get() == "" or \
            self.tab1.frame1.fuse_type_ABCD.get() == "" or \
            self.tab1.frame1.fuse_type_nr.get() == "" or \
            self.tab1.frame1.entry_measured_ipz.get() == "":
                return  # brak danych
            
            # wykonanie obliczeń(pomiaru)
            pomiar = Pomiar(self.tab1.frame1.circuit_name.cget("text"),
                            self.tab1.frame1.fuse_type_ABCD.get(),
                            self.tab1.frame1.fuse_type_nr.get(),
                            self.tab1.frame1.entry_measured_ipz.get())
            
            # zebranie danych z obliczeń
            self.tab1.frame2.ipz_security_value_result.configure(text=round(pomiar.ipz_zabezpieczenia(), 2))
            self.tab1.frame2.short_circuit_current_protection_result.configure(text=round(pomiar.prad_zwarciowy_zabezpieczenia()))
            self.tab1.frame2.calculated_short_circuit_current_result.configure(text=round(pomiar.obliczony_prad_zwarciowy()))
            self.tab1.frame2.grade_result.configure(text=pomiar.ocena())

            # zablokowanie przycisku oblicz i pól do wykonywania kolejnego pomiaru
            self.tab1.frame1.entry_circuit_name.configure(state='disabled')
            self.tab1.frame1.fuse_type_ABCD.configure(state='disabled')
            self.tab1.frame1.fuse_type_nr.configure(state='disabled')
            self.tab1.frame1.entry_measured_ipz.configure(state='disabled')
            self.tab1.frame1.calculate_button.configure(state='disabled')

            # odblokowanie przycisku dodaj pomiar
            self.tab1.frame2.add_measurement_button.configure(state='normal')

        def new_measurement():
            # odblokowanie pól do wprowadzania danych 
            self.tab1.frame1.entry_circuit_name.configure(state='normal')
            self.tab1.frame1.fuse_type_ABCD.configure(state='normal')
            self.tab1.frame1.fuse_type_nr.configure(state='normal')
            self.tab1.frame1.entry_measured_ipz.configure(state='normal')
            self.tab1.frame1.calculate_button.configure(state='normal')

            # zablokowanie przycisku dodaj pomiar
            self.tab1.frame2.add_measurement_button.configure(state='disabled')


            # wyczyszczenie pól
            self.tab1.frame1.entry_circuit_name.delete(0, 'end')
            self.tab1.frame1.fuse_type_ABCD.set('')
            self.tab1.frame1.fuse_type_nr.delete(0, 'end')
            self.tab1.frame1.entry_measured_ipz.delete(0, 'end')

            # wyczyszczenie wyników
            self.tab1.frame2.ipz_security_value_result.configure(text="")
            self.tab1.frame2.short_circuit_current_protection_result.configure(text="")
            self.tab1.frame2.calculated_short_circuit_current_result.configure(text="")
            self.tab1.frame2.grade_result.configure(text="")
            
            

        # generator liczb parzystych(kolejne wiersze w których będą wyświetlane pomiary)
        def number_generator():
            for i in range(0, 1000, 2):
                yield i
        gen = number_generator()

        def add_measurement():
            actual_row = next(gen)
            self.tab1.framescrol.label1 = ctk.CTkLabel(self.tab1.framescrol, 
                                            text=self.tab1.frame1.entry_circuit_name.get()
                                            + " ",
                                            font = self.font_arial16,
                                            text_color="#1f538d")
            self.tab1.framescrol.label1.grid(row=actual_row, column=0, padx=10, pady=5, sticky="w", columnspan=7)

            self.tab1.framescrol.label2 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame1.fuse_type_ABCD.get() 
                                                    + self.tab1.frame1.fuse_type_nr.get(),
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label2.grid(row=actual_row+1, column=0, padx=10, pady=0, sticky="w")

            self.tab1.framescrol.label3 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.ipz_security_value_result.cget("text"))
                                                    +"\u03A9",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label3.grid(row=actual_row+1, column=0, padx=80, pady=0, sticky="w", columnspan=2)

            self.tab1.framescrol.label4 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.short_circuit_current_protection_result.cget("text"))
                                                    +"A",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label4.grid(row=actual_row+1, column=0, padx=190, pady=0, sticky="w", columnspan=3)

            self.tab1.framescrol.label5 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame1.entry_measured_ipz.get()
                                                    +"\u03A9",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label5.grid(row=actual_row+1, column=0, padx=300, pady=0, sticky="w", columnspan=4)

            self.tab1.framescrol.label6 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.calculated_short_circuit_current_result.cget("text"))
                                                    + "A",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label6.grid(row=actual_row+1, column=0, padx=410, pady=0, sticky="w", columnspan=5)

            self.tab1.framescrol.label7 = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame2.grade_result.cget("text"), 
                                                    font = self.font_arial15,
                                                    text_color="#008B00" if self.tab1.frame2.grade_result.cget("text") == "TAK" else "#8B0000")   
            self.tab1.framescrol.label7.grid(row=actual_row+1, column=0, padx=520, pady=0, sticky="w", columnspan = 6)

            
            
            self.tab1.frame2.add_measurement_button.configure(state='disabled')

        
        
        # Rama pierwsza - w nią należy wpisać dane do obliczeń
        self.tab1.frame1 = ctk.CTkFrame(self.tab1,
                                        width=400,
                                        height=200,
                                        fg_color="silver",
                                        )
        self.tab1.frame1.grid(row=0, column=0, padx=10, pady=0, sticky="n")
        self.tab1.frame1.grid_propagate(False)

        # napis PARAMETRY
        self.tab1.frame1.inscription_parametry = ctk.CTkLabel(self.tab1.frame1, 
                                   text="PARAMETRY", 
                                   font = self.font_arial18,
                                   text_color='black')
        self.tab1.frame1.inscription_parametry.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        # nazwa obwodu
        self.tab1.frame1.circuit_name = ctk.CTkLabel(self.tab1.frame1,
                                             text = "Nazwa:",
                                             font=self.font_arial15,
                                             text_color='black',
                                             )
        self.tab1.frame1.circuit_name.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.tab1.frame1.entry_circuit_name = ctk.CTkEntry(self.tab1.frame1, 
                                                  placeholder_text="",
                                                  width=200,
                                                  textvariable=self.entry_name_variable,
                                                  ) 
        self.tab1.frame1.entry_circuit_name.grid(row=1, column=1, padx=0, pady=5, sticky="w", columnspan=2)

        # typ bezpiecznika
        self.tab1.frame1.fuse_type = ctk.CTkLabel(self.tab1.frame1, 
                                               text="Typ bezpiecznika:", 
                                               font = self.font_arial15,
                                               text_color='black'
                                               )
        self.tab1.frame1.fuse_type.grid(row=2, column=0, padx=20, pady=0, sticky="w")

        self.tab1.frame1.fuse_type_ABCD = ctk.CTkOptionMenu(self.tab1.frame1, 
                                                       values = ["A", "B", "C", "D"],
                                                       width = 90,
                                                       )
        self.tab1.frame1.fuse_type_ABCD.set("")
        self.tab1.frame1.fuse_type_ABCD.grid(row=2, column=1, padx=0, pady=0, sticky="w")

        self.tab1.frame1.fuse_type_nr = ctk.CTkEntry(self.tab1.frame1, 
                                              placeholder_text="",
                                              width=100,
                                              textvariable=self.entry_fuse_variable,
                                              )
        self.tab1.frame1.fuse_type_nr.grid(row=2, column=1, padx=100, pady=0, sticky="w", columnspan=2)

        # IPZ zmierzone
        self.tab1.frame1.measured_ipz = ctk.CTkLabel(self.tab1.frame1,
                                               text = "IPZ zmierzone[\u03A9]:",
                                               font=self.font_arial15,
                                               text_color='black',
                    )
        self.tab1.frame1.measured_ipz.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.tab1.frame1.entry_measured_ipz = ctk.CTkEntry(self.tab1.frame1, 
                                               placeholder_text="",
                                               width=200,
                                               textvariable=self.entry_ipz_variable,
                                               )
        self.tab1.frame1.entry_measured_ipz.grid(row=3, column=1, padx=0, pady=10, sticky="w")

        # przycisk oblicz
        self.tab1.frame1.calculate_button = ctk.CTkButton(self.tab1.frame1, 
                                               text="Oblicz",
                                               command=calculate, 
                                               )
        print(self.tab1.frame1.entry_circuit_name.get())

        self.tab1.frame1.calculate_button.grid(row=4, column=0, padx=15, pady=10, sticky="w")

        # przycisk nowy pomiar
        self.tab1.frame1.new_measurement_button = ctk.CTkButton(self.tab1.frame1, 
                                               text="Nowy pomiar",
                                               command=new_measurement,
                                               )
        self.tab1.frame1.new_measurement_button.grid(row=4, column=1, padx=0, pady=10, sticky="w")


        #Rama druga - w niej wyświetlają się wyniki obliczeń
        self.tab1.frame2 = ctk.CTkFrame(self.tab1,
                                        width=400,
                                        height=200,
                                        fg_color="silver")
        self.tab1.frame2.grid(row=1, column=0, padx=10, pady=20, sticky="n")
        self.tab1.frame2.grid_propagate(False)

        # napis WYNIK
        self.tab1.frame2.inscription_wynik = ctk.CTkLabel(self.tab1.frame2, 
                                   text="WYNIK", 
                                   font = self.font_arial18,
                                   text_color='black')
        self.tab1.frame2.inscription_wynik.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        # IPZ zabezpieczenia
        self.tab1.frame2.ipz_security_value = ctk.CTkLabel(self.tab1.frame2, 
                                               text="IPZ zabezpieczenia[\u03A9]:", 
                                               font = self.font_arial15,
                                               text_color='black'
                                               )
        self.tab1.frame2.ipz_security_value.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        self.tab1.frame2.ipz_security_value_result = ctk.CTkLabel(self.tab1.frame2,
                                                        text = "",
                                                        font=self.font_arial15,
                                                        text_color='black',
                                                        )
        self.tab1.frame2.ipz_security_value_result.grid(row=1, column=1, padx=20, pady=0, sticky="w")

        # Prąd zwarciowy zabezpieczenia
        self.tab1.frame2.short_circuit_current_protection = ctk.CTkLabel(self.tab1.frame2, 
                                               text="Prąd zwarciowy zabezpieczenia[A]:", 
                                               font = self.font_arial15,
                                               text_color='black'
                                               )
        self.tab1.frame2.short_circuit_current_protection.grid(row=2, column=0, padx=20, pady=0, sticky="w")

        self.tab1.frame2.short_circuit_current_protection_result = ctk.CTkLabel(self.tab1.frame2,
                                                        text = "",
                                                        font=self.font_arial15,
                                                        text_color='black',
                                                        )
        self.tab1.frame2.short_circuit_current_protection_result.grid(row=2, column=1, padx=20, pady=0, sticky="w")

        # Obliczony prąd zwarciowy
        self.tab1.frame2.calculated_short_circuit_current = ctk.CTkLabel(self.tab1.frame2, 
                                               text="Obliczony prąd zwarciowy[A]:", 
                                               font = self.font_arial15,
                                               text_color='black'
                                               )
        self.tab1.frame2.calculated_short_circuit_current.grid(row=3, column=0, padx=20, pady=0, sticky="w")

        self.tab1.frame2.calculated_short_circuit_current_result = ctk.CTkLabel(self.tab1.frame2,
                                                        text = "",
                                                        font=self.font_arial15,
                                                        text_color='black',
                                                        )
        self.tab1.frame2.calculated_short_circuit_current_result.grid(row=3, column=1, padx=20, pady=0, sticky="w")

        # Ocena
        self.tab1.frame2.grade = ctk.CTkLabel(self.tab1.frame2, 
                                               text="Ocena:", 
                                               font = self.font_arial15,
                                               text_color='black'
                                               )
        self.tab1.frame2.grade.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.tab1.frame2.grade_result = ctk.CTkLabel(self.tab1.frame2,
                                                        text = "",
                                                        font=self.font_arial15,
                                                        text_color='black',
                                                        )
        self.tab1.frame2.grade_result.grid(row=4, column=1, padx=20, pady=0, sticky="w")

        # przycisk dodaj pomiar
        self.tab1.frame2.add_measurement_button = ctk.CTkButton(self.tab1.frame2, 
                                               text="Dodaj pomiar",
                                               command=add_measurement,
                                               state='disabled',
                                               )
        self.tab1.frame2.add_measurement_button.grid(row=5, column=0, padx=15, pady=10, sticky="w")

        # Rama trzecia - w niej wyświetlają się pomiary
        self.tab1.framescrol = ctk.CTkScrollableFrame(self.tab1, 
                                        width=670, 
                                        height=356,
                                        label_font = self.font_arial12,
                                        fg_color="silver",
                                        scrollbar_button_color="black",
                                        label_text="Zab.".ljust(15)+
                                        "IPZ zab.[\u03A9]".ljust(25)+ 
                                        "P. zw. zab.[A]".ljust(25)+
                                        "IPZ zm.[\u03A9]".ljust(25)+
                                        "P. zw. obl.[A]".ljust(25)+
                                        "Ocena".ljust(15)+ 
                                        "Usuń",
                                        label_anchor="w",)
        
        self.tab1.framescrol.grid(row=0, column=1, padx=0, pady=0, sticky = "n", rowspan=2)

app = App()
app.mainloop()

