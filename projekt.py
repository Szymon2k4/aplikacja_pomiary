import customtkinter as ctk
from pomiar import Pomiar
import ctypes
import uuid
from datetime import date
from itertools import count

from data_manage import data_man, remove_data_using_id, save_file, load_measuremenst, is_file_name_exist

# ogólne ustawienia aplikacji
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


# klasa do obsługi GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Pomiary Elektryczne')
        self.iconbitmap('lightning.ico')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ikona.ikona")
        self.geometry('600x400')
        self.parameters() 
        self.save_window()
        
    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())  
        

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
                      slant="roman"
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

        self.save_name_variable = ctk.StringVar()
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

        



        

        
    # przejsie z okna zaposu do okna glownego
    def run_app(self):
        self.save_tab.destroy()
        self.geometry('1200x600')
        try:
            self.title(f'Pomiary elektryczne:  {str(self.save_name_variable.get()).upper()}')
        except AttributeError:
            self.title(f'Pomiary elektryczne:  {str(self.save_name_variable).upper()}')
        self.main_window()
    
    #obsluga okna zapisu
    def save_window(self):
        # funkcje do obsługi buttonow w save_window
        def dodaj():
            name = str(self.save_name_variable.get())
            dat = date.today()
            print(is_file_name_exist('nazwy_pomiary.csv', name))

            if data_man('nazwy_pomiary.csv', ['Nazwa', 'data'], [name, dat]) == True:
                pass

        def wczytaj():
            self.save_tab.load_frame.button[x:=to_load.pop()].cget("text")
            self.run_app()

        def handle_options(i):
                self.save_tab.button2.configure(state = 'normal')
                self.save_tab.load_frame.button[i].configure(fg_color = '#5bc0eb')
                for k in range(len(meas)):
                    if k != i:
                        self.save_tab.load_frame.button[k].configure(fg_color = 'white')

                if not to_load:
                    to_load.append(i)
                else:
                    to_load[0] = i

                self.save_name_variable = meas[i]
        #####

        to_load = list()

        self.save_tab = ctk.CTkFrame(self,
                                     width = 550,
                                     height = 350)
        self.save_tab.grid(row=0, column=0, padx=25, pady=25, sticky="n")
        self.save_tab.grid_propagate(False)

        self.save_tab.label1 = ctk.CTkLabel(self.save_tab,
                                            text='Nazwa pomiarów:',
                                            text_color='white',
                                            font=('Helvetica', 16)                              
                                                  ) 
        self.save_tab.label1.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.save_tab.entry1 = ctk.CTkEntry(self.save_tab, 
                                                  placeholder_text="text",
                                                  width=200, 
                                                  textvariable=self.save_name_variable 
                                                                                 
                                                  ) 
        self.save_tab.entry1.grid(row=1, column=0, padx=10, pady=0, sticky="n")

        self.save_tab.label1 = ctk.CTkLabel(self.save_tab,
                                            text='notatka:',
                                            text_color='white',
                                                                         
                                                  ) 
        self.save_tab.label1.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        self.save_tab.entry2 = ctk.CTkTextbox(self.save_tab,    
                                                  width=200,
                                                  height=150,
                                                  wrap = 'word',
                                                                       
                                                  ) 
        self.save_tab.entry2.grid(row=3, column=0, padx=10, pady=0, sticky="n")
        self.save_tab.grid_rowconfigure(3, weight = 3)

        self.save_tab.button1 = ctk.CTkButton(self.save_tab, text="dodaj", command=dodaj)
        self.save_tab.button1.grid(row=4, column=0, padx=10, pady=15, sticky = 'sw')

        self.save_tab.button2 = ctk.CTkButton(self.save_tab, 
                                              text="wczytaj", 
                                              command=wczytaj,
                                              state='disabled')
        self.save_tab.button2.grid(row=4, column=1, padx=30, pady=15, sticky = 'sw')

        self.save_tab.load_frame = ctk.CTkScrollableFrame(self.save_tab,
                                                          fg_color='white',
                                                          width = 250,
                                                          height = 150,
                                                          label_text='Pomiary'
                                                          )
        self.save_tab.load_frame.grid(row = 0, column = 1, pady = 10, padx = 30, rowspan = 4)
        #load_measuremenst()
        meas = ['pierszy', 'drugi', 'trzeci']
        self.save_tab.load_frame.button = list(range(len(meas)))

        for i, mea in enumerate(meas):
            self.save_tab.load_frame.button[i]= ctk.CTkButton(self.save_tab.load_frame,
                                                                text=mea,
                                                                text_color='black',
                                                                fg_color='white',
                                                                anchor = 'w',
                                                                width = 230,
                                                                corner_radius=10,
                                                                hover_color='#a0d8f1',
                                                                command = lambda i = i: handle_options(i))
            self.save_tab.load_frame.button[i].grid(row = i, column = 0, padx = 5, pady = 0, sticky = 'ew')
            
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
        # zmienne globalne okna tab1_window
        gen = count(0, 3)            
        delete_buttons_dict = dict()
        labels = dict()
        for i in range(9):
            labels[i] = dict()



        # funnkcje do obslugi buttonow w tab1_window 
        # funkcja do obslugi klawiszy, klikniecie enter
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
            nazwa = self.tab1.frame1.circuit_name.cget("text")
            typ_bez = self.tab1.frame1.fuse_type_ABCD.get()
            typ_bez_liczba = self.tab1.frame1.fuse_type_nr.get()
            ipz_zmierzone = self.tab1.frame1.entry_measured_ipz.get()
            ipz_zmierzone = ipz_zmierzone.replace(',', '.')
            pomiar = Pomiar(nazwa, typ_bez, typ_bez_liczba, ipz_zmierzone)
            
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

        #funkcja przycisk usun
        def remove_all():
            #funkcja wykorzystana w remove_all
            def remove_all2():
                self.tab1.buttons_frame.remove_all.configure(state = 'disabled')
                ar = 0
                removing_id = list()
                while True:
                    try:
                        for i in range(8):
                            labels[i][ar].destroy()
                        delete_buttons_dict[ar].destroy()
                        removing_id.append(labels[8][ar])
                        ar +=3
                    except KeyError:
                        break
                
                self.tab1.check_window.destroy()
                remove_data_using_id(removing_id)
                #####
            try:
                self.tab1.check_window.destroy()
            except AttributeError:
                pass

            self.tab1.check_window = ctk.CTkToplevel(self.tab1) 
            self.tab1.check_window.geometry("350x150")  
            self.tab1.check_window.title("Usuwanie pomiarów")  
            # Unosi okno nad inne
            self.tab1.check_window.lift()  
            self.tab1.check_window.grab_set()

            for i in range(2):  
                self.tab1.check_window.grid_columnconfigure(i, weight=1)
                self.tab1.check_window.grid_rowconfigure(i, weight=1)
            # Etykieta w nowym oknie
            self.tab1.check_window.label = ctk.CTkLabel(self.tab1.check_window, text=f'Kliknij OK aby potwierdzić usunięcie wszystkich pomiarów')
            self.tab1.check_window.label.grid(row = 0, column = 0, padx=0, pady=10, sticky = 'n', columnspan = 2)
            
            # Przycisk zamykający okno
            self.tab1.check_window.ok_button = ctk.CTkButton(self.tab1.check_window, text="OK", command=remove_all2)
            self.tab1.check_window.ok_button.grid(row = 1, column = 0, padx=20, pady=0, sticky = 'w' )

            self.tab1.check_window.nok_button = ctk.CTkButton(self.tab1.check_window, text="Anuluj", command=self.tab1.check_window.destroy)
            self.tab1.check_window.nok_button.grid(row = 1, column = 1, padx=20, pady=0, sticky = 'e' )

            

            

        

        def export_excel():
            raise NotImplementedError

 
        
        
        
        # rama3 - dodawanie kolejnych pomiarów
        def add_measurement():
            actual_row = next(gen) # row kolejnego pomiaru

            self.tab1.buttons_frame.remove_all.configure(state = 'normal')
            self.tab1.buttons_frame.export_excel.configure(state = 'normal')
            def handle_delete_row(ar):
                def delete_row():
                    for i in range(8):
                        labels[i][ar].destroy()
                    delete_buttons_dict[ar].destroy()
                    self.tab1.check_window.destroy()

                    rmv_id = labels[8][ar]
                    remove_data_using_id(rmv_id)
                    ####
                try:
                    self.tab1.check_window.destroy()
                except AttributeError:
                    pass

                self.tab1.check_window = ctk.CTkToplevel(self.tab1)  
                self.tab1.check_window.geometry("350x150") 
                self.tab1.check_window.title("Usuwanie pomiaru") 
                # Unosi okno nad inne
                self.tab1.check_window.lift()  
                self.tab1.check_window.grab_set() 

                for i in range(2):  
                    self.tab1.check_window.grid_columnconfigure(i, weight=1)
                    self.tab1.check_window.grid_rowconfigure(i, weight=1)
                # Etykieta w nowym oknie
                pom = labels[0][ar].cget("text")
                self.tab1.check_window.label = ctk.CTkLabel(self.tab1.check_window, text=f'Kliknij OK aby potwierdzić usunięcie pomiaru "{pom}"')
                self.tab1.check_window.label.grid(row = 0, column = 0, padx=0, pady=10, sticky = 'n', columnspan = 2)
                
                # Przycisk zamykający okno
                self.tab1.check_window.ok_button = ctk.CTkButton(self.tab1.check_window, text="OK", command=delete_row)
                self.tab1.check_window.ok_button.grid(row = 1, column = 0, padx=20, pady=0, sticky = 'w' )

                self.tab1.check_window.nok_button = ctk.CTkButton(self.tab1.check_window, text="Anuluj", command=self.tab1.check_window.destroy)
                self.tab1.check_window.nok_button.grid(row = 1, column = 1, padx=20, pady=0, sticky = 'e' )
            
                
            #slownik do przechowywania kolejnych danych
            self.tab1.framescrol.label = dict()
            for i in range(8):
                self.tab1.framescrol.label[i] = dict()
            #nazwa
            self.tab1.framescrol.label[0][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                            text=self.tab1.frame1.entry_circuit_name.get()
                                            + " ",
                                            font = self.font_arial16,
                                            text_color="#1f538d")
            self.tab1.framescrol.label[0][actual_row].grid(row=actual_row, column=0, padx=10, pady=5, sticky="w", columnspan = 6)
            
            #typ bezpiecznika
            self.tab1.framescrol.label[1][actual_row]= ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame1.fuse_type_ABCD.get() 
                                                    + self.tab1.frame1.fuse_type_nr.get(),
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label[1][actual_row].grid(row=actual_row+1, column = 0, padx=10, pady=0, sticky="w")
            
            #ipz obliczone
            self.tab1.framescrol.label[2][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.ipz_security_value_result.cget("text"))
                                                    +"\u03A9",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label[2][actual_row].grid(row=actual_row+1, column = 1, padx=10, pady=0, sticky="w")

            #prad zw. zab.
            self.tab1.framescrol.label[3][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.short_circuit_current_protection_result.cget("text"))
                                                    +"A",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label[3][actual_row].grid(row=actual_row+1, column = 2, padx=10, pady=0, sticky="w")

            #obliczone IPZ
            self.tab1.framescrol.label[4][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame1.entry_measured_ipz.get()
                                                    +"\u03A9",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label[4][actual_row].grid(row=actual_row+1, column = 3, padx=10, pady=0, sticky="w")

            #obliczony prad zw. zab.
            self.tab1.framescrol.label[5][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=str(self.tab1.frame2.calculated_short_circuit_current_result.cget("text"))
                                                    + "A",
                                                    font = self.font_arial15,
                                                    text_color='black')
            self.tab1.framescrol.label[5][actual_row].grid(row=actual_row+1, column = 4, padx=10, pady=0, sticky="w")

            #ocena
            self.tab1.framescrol.label[6][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text=self.tab1.frame2.grade_result.cget("text"), 
                                                    font = self.font_arial15,
                                                    text_color="#008B00" if self.tab1.frame2.grade_result.cget("text") == "TAK" else "#8B0000")   
            self.tab1.framescrol.label[6][actual_row].grid(row=actual_row+1, column = 5, padx=10, pady=0, sticky="w")
            
            #przycisk usun
            self.tab1.framescrol.delete_button = ctk.CTkButton(self.tab1.framescrol, 
                                                    text="usuń",
                                                    width = 55,
                                                    height = 35,
                                                    command = lambda actual_row = actual_row: handle_delete_row(actual_row),
                                                    state = 'disabled') 
            self.tab1.framescrol.delete_button.grid(row=actual_row+1, column = 6, padx=10, pady=0, sticky="w")
            
            #linia poiedzy koljenymi pomiarami
            self.tab1.framescrol.label[7][actual_row] = ctk.CTkLabel(self.tab1.framescrol, 
                                                    text="-"*200,
                                                    text_color='black')
            self.tab1.framescrol.label[7][actual_row].grid(row=actual_row+2, column=0, padx=0, pady=0, sticky="n", columnspan=7)

            # zapisywanie danych do slownikow
            for i in range(8):
                labels[i][actual_row] = self.tab1.framescrol.label[i][actual_row]
            delete_buttons_dict[actual_row] = self.tab1.framescrol.delete_button

            labels[8][actual_row] = self.generate_unique_id()
           
            
            # przesuwanie strony w dół
            self.tab1.framescrol.update_idletasks()
            self.tab1.framescrol._parent_canvas.yview_moveto(1.0)
            self.tab1.frame2.add_measurement_button.configure(state='disabled')

            # przekazywnie dodadanych danych do plikow
            data_table = [labels[i][actual_row].cget("text") for i in range(7)]
            data_table.append(labels[8][actual_row])
            data_table.append(date.today())
            data_table.append('nd') #not deleted
            file_name = 'pomiary/name.csv'
            headlines = ['nazwa', 'typ_bez', 'ipz_zab', 'prad_zw_zab', 'ipz_obl', 'obl_pr_zwarc', 'ocena', 'id', 'datetime.date(yyyy, mm, dd)', 'deleted']
            data_man(file_name, headlines, data_table)



            self.tab1.framescrol.delete_button.configure(state = 'normal')
        ##################

        ## IMPLEMENTACJA RAMY PIERWSZEJ
        # Rama pierwsza - w nią należy wpisać dane do obliczeń
        self.tab1.frame1 = ctk.CTkFrame(self.tab1,
                                        width=400,
                                        height=200,
                                        fg_color="white",
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
                                             text_color='black'
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
                                        fg_color="white")
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
                                                        font = self.font_arial15,
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
        print_format = 23
        self.tab1.framescrol = ctk.CTkScrollableFrame(self.tab1, 
                                        width=670, 
                                        height=320,
                                        label_font = self.font_arial12,
                                        fg_color="white",
                                        scrollbar_button_color="black")
                                        # label_text="Zab.".ljust(print_format)+
                                        # "IPZ zab.".ljust(print_format)+ 
                                        # "P. zw. zab.".ljust(print_format)+
                                        # "IPZ zm.".ljust(print_format)+
                                        # "P. zw. obl.".ljust(print_format)+
                                        # "Ocena".ljust(print_format)+ 
                                        # "Usuń",
                                        # label_anchor="w",)
        
        self.tab1.framescrol.grid(row=0, column=1, padx=0, pady=40, sticky = "n", rowspan=2)

        for i in range(7):  
            self.tab1.framescrol.grid_columnconfigure(i, weight=1)
        

        # tytuly ramy 3
        self.tab1.header_frame = ctk.CTkFrame(self.tab1, 
                                              width=693,
                                              height=30,
                                              fg_color = "#2B2B2B")

        self.tab1.header_frame.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = 'n')
        self.tab1.header_frame.grid_propagate(False)

        for i in range(7):  
            self.tab1.header_frame.grid_columnconfigure(i, weight=1)

        self.tab1.header_frame.label1 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = 'Typ zab.',
                                                     text_color="white",
                                                     )
        self.tab1.header_frame.label1.grid(row = 0, column = 0, padx = 10, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label2 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = ' IPZ zab.',
                                                     text_color="white")
        
        self.tab1.header_frame.label2.grid(row = 0, column = 1, padx = 5, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label3 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = ' Prąd zw.',
                                                     text_color="white")
        
        self.tab1.header_frame.label3.grid(row = 0, column = 2, padx = 15, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label4 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = ' IPZ zm.',
                                                     text_color="white")
        
        self.tab1.header_frame.label4.grid(row = 0, column = 3, padx = 10, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label5 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = 'Prąd zw. obl.',
                                                     text_color="white")
        
        self.tab1.header_frame.label5.grid(row = 0, column = 4, padx = 0, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label6 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = 'Ocena',
                                                     text_color="white")
        
        self.tab1.header_frame.label6.grid(row = 0, column = 5, padx = 0, pady = 0, sticky = 'w', columnspan = 2)

        self.tab1.header_frame.label6 = ctk.CTkLabel(self.tab1.header_frame,
                                                     text = 'Usuń',
                                                     text_color="#2B2B2B")
        
        self.tab1.header_frame.label6.grid(row = 0, column = 6, padx = 17, pady = 0, sticky = 'w', columnspan = 1)

        
        

        
        # okno do przyciskow
        self.tab1.buttons_frame = ctk.CTkFrame(self.tab1, 
                                            width=693,
                                            height=40,
                                            fg_color = "white")

        self.tab1.buttons_frame.grid(row = 1, column = 1, padx = 0, pady = 20, sticky = 'ws')
        self.tab1.buttons_frame.grid_propagate(False)
        
        for i in range(2):  
            self.tab1.buttons_frame.grid_columnconfigure(i, weight=1)


        self.tab1.buttons_frame.remove_all = ctk.CTkButton(self.tab1.buttons_frame,
                                                            text = 'Usuń wszystko',
                                                            width = 140,
                                                            height = 28,
                                                            command = remove_all,
                                                            state = 'disabled')
        self.tab1.buttons_frame.remove_all.grid(row = 0, column = 0, padx = 0, pady = 5, sticky = 'n')  
            

        self.tab1.buttons_frame.export_excel = ctk.CTkButton(self.tab1.buttons_frame,
                                                            text='Eksportuj',
                                                            width = 140,
                                                            height = 28,
                                                            command = export_excel,
                                                            state = 'disabled')
        self.tab1.buttons_frame.export_excel.grid(row = 0, column = 1,padx = 0, pady = 5, sticky = 'n')
        
    













