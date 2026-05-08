import customtkinter
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from PIL import Image, ImageTk
import webbrowser
import json


@dataclass
class Lego:
    tipologia: str
    nome: str
    eta: int
    anno: int
    id: str
    numero_pezzi: int
    prezzo: float
    link: str
    immagine: str
    
class App:
    
    #Creazione win iniziale
    def __init__(self):
        self.finestra = None                    #|
        self.agg_set = None                     #|
        self.set_lego = []                      #|
        self.percorso = None                    #|  
        self.percorso_immagine = None           #|  Varibaili globali
        self.salva_immagini = []                #|
        self.controllo_senza_salvare = False    #|
        self.indice= None                       #|

        
        self.win = ctk.CTk()
        self.win.geometry("1080x720")
        self.win.title("Gestore set LEGO")
        self.win.resizable(True, True)
        self.win.minsize(1080, 720)

        crea_btn = ctk.CTkButton(self.win, text="Crea nuovo gestore", width=400, height=100 , font=ctk.CTkFont(size=40, weight="bold"), cursor="hand2", corner_radius=32, command= lambda: self.crea(0))
        crea_btn.place(relx=0.5, rely=0.4, anchor="center")

        apri_btn=ctk.CTkButton(self.win, text="Apri set già esistenti", width=400, height=100, font=ctk.CTkFont(size=40, weight="bold"), cursor="hand2", corner_radius=32, command=lambda: self.crea(1))
        apri_btn.place(relx=0.5, rely=0.6, anchor="center")  
        
    #Funzione apertura file esistente
    def file_esistente(self):
        self.percorso=filedialog.askopenfilename(defaultextension=".json", title="Scegli salvataggio da caricare", filetypes=[("File JSON", ".json")])
        if self.percorso:
            with open(self.percorso, "r") as file:
                lista = json.load(file)
                
            self.set_lego = [] 
            
            for caricare in lista:
                set_caricato = Lego(
                    tipologia =caricare["tipologia"],
                    nome =caricare["nome"],
                    eta = caricare["eta"],
                    anno =caricare["anno"],
                    id =caricare["id"],
                    numero_pezzi= caricare["numero_pezzi"],
                    prezzo = caricare["prezzo"],
                    link =caricare["link"],
                    immagine = caricare["immagine"]
                )
                self.set_lego.append(set_caricato)
                
            
            messagebox.showinfo("Perfetto!", "File caricato con successo!")
        else:            
            messagebox.showwarning("Attenzione!", "Qualcosa è andato storto! Apertura gestore vuoto")
        
    #Creazione finestra       
    def crea(self, esiste):
        self.set_lego=[]
        if esiste == 1:
            self.file_esistente()
            
        if self.finestra is None or not self.finestra.winfo_exists(): 
            self.finestra = customtkinter.CTkToplevel(self.win)  
            self.finestra.geometry("1600x820")
            self.finestra.minsize = (1600, 820)
            self.finestra.title("Gestore")
            self.finestra.lift()       
            self.finestra.protocol("WM_DELETE_WINDOW", lambda: self.chiudi(self.finestra))  #se viene premuta la x si esegue la funzione chiudi        
            self.win.withdraw()
            #viene nascosta la win iniziale
            info_btn = ctk.CTkButton(self.finestra, text="Informazioni", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12)
            info_btn.grid(row = 0, column = 0, padx=30, pady =15)
            
            nset_btn = ctk.CTkButton(self.finestra, text="Crea nuovo set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command = self.aggiungi)
            nset_btn.grid(row = 0, column = 1, padx=15, pady =15)     
            
            save_btn = ctk.CTkButton(self.finestra, text="Salva", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command=lambda: self.salva(0))
            save_btn.grid(row = 0, column = 2, padx=30, pady =15)
            
            snome_btn = ctk.CTkButton(self.finestra, text="Salva con nome", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command=lambda: self.salva(1))
            snome_btn.grid(row = 0, column = 3, padx=30, pady =15)
            
            container = ctk.CTkFrame(self.finestra, width=150, height=30, bg_color="transparent", fg_color="transparent")
            container.grid(row = 0, column = 4, padx=30, pady =15)
            
            reset = ctk.CTkButton(container, width=30, height=30, text="X", fg_color="red", font=ctk.CTkFont(size=21), hover_color="#800000", command= self.aggiorna_tabella)
            reset.pack(side="left", padx=5)
            
            self.ent_ricerca = ctk.CTkEntry(container, width=200, height=30, font=ctk.CTkFont(size=14, weight="bold"), placeholder_text="Cerca un set...", corner_radius=16)
            self.ent_ricerca.pack(side="left", padx=5)
            
            cerca = ctk.CTkButton(container, text="Cerca",  width=100, height=30, font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command= self.cerca)
            cerca.pack(side="right", padx=5)         
            
            #Tabella
            self.tabella = ttk.Treeview(self.finestra)
            self.tabella["columns"] = ("Tipologia", "Nome", "Età", "Anno", "ID", "Numero pezzi", "Prezzo", "Link")
            self.tabella.column("#0", width=80, anchor="center")
            self.tabella.heading("#0", text="img")
             
            self.tabella.bind("<Button-1>", self.apri_link)      
            self.tabella.bind("<Double-1>", self.modifica)
            self.tabella.bind("<Button-3>", self.elimina)
            
            for colonna in self.tabella["columns"]:
                self.tabella.column(colonna, anchor="center", minwidth=120)            
                self.tabella.heading(colonna, text=colonna)

            self.tabella.grid(row=1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
            
            #stile per tabella strano        
            self.finestra.grid_rowconfigure(1, weight=1)
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="#F8F9FA", foreground="#222222", fieldbackground="#F8F9FA", rowheight=105, font=("Segoe UI", 11))
            style.configure("Treeview.Heading", background="#FFD500", foreground="#222222", font=("Segoe UI", 11, "bold"), relief="flat")      
            style.map("Treeview", background=[("selected", "#4A90E2")], foreground=[("selected", "white")])
            style.map("Treeview.Heading", background=[("active", "#FFC300")])
            for i in range(5):
                self.finestra.grid_columnconfigure(i, weight=1) 
                          
            self.aggiorna_tabella()
    
    #chiusura finestre
    def chiudi(self, finestra_da_chiudere):
        if self.controllo_senza_salvare==True and finestra_da_chiudere== self.finestra:
            self.sicuro()
        if finestra_da_chiudere is not None and finestra_da_chiudere.winfo_exists():
            finestra_da_chiudere.destroy() 
            if finestra_da_chiudere == self.finestra:       
                self.win.deiconify()
            else:
                pass    
    
    #Finestra aggiunta set lego
    def aggiungi(self):        
                    
        if self.agg_set is None or not self.agg_set.winfo_exists():
            self.agg_set = customtkinter.CTkToplevel(self.finestra)
            self.agg_set.geometry("1080x720")
            self.agg_set.minsize = (1080, 720)
            self.agg_set.title("Nuovo set")               
            self.agg_set.grab_set()     
            self.agg_set.protocol("WM_DELETE_WINDOW", lambda: self.chiudi(self.agg_set))


            l1 = ctk.CTkLabel(self.agg_set, text="Tipologia del set lego:" )
            l1.grid(row=0, column=0, padx=30, pady=20)
            self.ent1 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent1.grid(row=0, column=1, padx=30, pady=20)
            
            l2 = ctk.CTkLabel(self.agg_set, text="Nome set lego:" )
            l2.grid(row=1, column=0, padx=30, pady=20)
            self.ent2 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent2.grid(row=1, column=1, padx=30, pady=20)
            
            l3 = ctk.CTkLabel(self.agg_set, text="Età necessaria:" )
            l3.grid(row=2, column=0, padx=30, pady=20)
            self.ent3 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent3.grid(row=2, column=1, padx=30, pady=20)
            
            l4 = ctk.CTkLabel(self.agg_set, text="Anno di uscita:" )
            l4.grid(row=3, column=0, padx=30, pady=20)
            self.ent4 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent4.grid(row=3, column=1, padx=30, pady=20)
            
            l5 = ctk.CTkLabel(self.agg_set, text="Id lego:" )
            l5.grid(row=4, column=0, padx=30, pady=20)
            self.ent5 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent5.grid(row=4, column=1, padx=30, pady=20)
            
            limg = ctk.CTkLabel(self.agg_set, text="Inserisci l'immagine del set:")
            limg.grid(row=4, column=2, padx=30, pady=20)
            btnimg = ctk.CTkButton(self.agg_set, text="Scegli immagine", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command= self.immagine)
            btnimg.grid(row=5, column=2)
            
            self.foto = ctk.CTkLabel(self.agg_set, width=150, height=150, text="")
            self.foto.grid(row=4 , column=3)
            
            l6 = ctk.CTkLabel(self.agg_set, text="Numero pezzi:" )
            l6.grid(row=5, column=0, padx=30, pady=20)
            self.ent6 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent6.grid(row=5, column=1, padx=30, pady=20)
            
            l7 = ctk.CTkLabel(self.agg_set, text="Prezzo(euro):" )
            l7.grid(row=6, column=0, padx=30, pady=20)
            self.ent7 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent7.grid(row=6, column=1, padx=30, pady=20)
            
            l8 = ctk.CTkLabel(self.agg_set, text="Link al sito ufficiale:" )
            l8.grid(row=7, column=0, padx=30, pady=20)
            self.ent8 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent8.grid(row=7, column=1, padx=30, pady=20)
            
            self.aggiunta = ctk.CTkButton(self.agg_set, text="Aggiungi il set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command= lambda: self.aggiungere(0))        
            self.aggiunta.grid(row=8, column=0, padx=30, pady=20)
    
    #Aggiunta set lego            
    def aggiungere(self, x):
        if not (self.ent1.get() and self.ent2.get() and self.ent3.get() and self.ent4.get() and self.ent5.get() and self.ent6.get() and self.ent7.get() and self.ent8.get()):
            messagebox.showwarning("attenzione!", "Devi compilare tutti i campi!")
        elif not self.foto.cget("image"):
            messagebox.showwarning("attenzione!", "Foto mancante, inseriscine una!")
            
        else:
            try:
                eta = int(self.ent3.get())
                anno = int(self.ent4.get())
                numero_pezzi = int(self.ent6.get())
                prezzo = float(self.ent7.get().replace(",", "."))

            except ValueError:
                messagebox.showwarning("attenzione!", "Anno, numero, pezzi e prezzo devono essere numeri!")
            else:
                nuovo_set = Lego(
                    tipologia= self.ent1.get(),
                    nome=self.ent2.get(),
                    eta=eta,
                    anno=anno,
                    id=self.ent5.get(),
                    numero_pezzi=numero_pezzi,
                    prezzo=prezzo,
                    link=self.ent8.get(),
                    immagine=self.percorso_immagine
                )
                if x == 0:
                    self.set_lego.append(nuovo_set)                    
                else:
                    self.set_lego[self.indice] = nuovo_set
                    
                self.aggiorna_tabella()
                self.chiudi(self.agg_set)
               
        self.controllo_senza_salvare = True            
    
    #Salvataggio set LEGO            
    def salva(self,x):
        if not self.set_lego:
            messagebox.showwarning("Attenzione!", "Lista vuota!")
            return
        else:
            if self.percorso==None or x == 1:
                self.percorso = filedialog.asksaveasfilename(defaultextension=".json", title="Scegli dove salvare i set lego", filetypes=[("File JSON", ".json")])

            if self.percorso:
                lista = []

                for set in self.set_lego:
                    diz = {
                        "tipologia": set.tipologia,
                        "nome": set.nome,
                        "eta": set.eta,
                        "anno": set.anno,
                        "id": set.id,
                        "numero_pezzi": set.numero_pezzi,
                        "prezzo": set.prezzo,
                        "link": set.link,
                        "immagine": set.immagine
                    }
                    lista.append(diz)

                with open(self.percorso, "w") as file:
                    json.dump(lista, file, indent=4)
        self.controllo_senza_salvare = False
    
    #Se non hai salvato il lavoro  
    def sicuro(self):
        risposta = messagebox.askyesno("Cosa vuoi fare?", "Non hai salvato il lavoro, vuoi salvarlo adesso?")
        if risposta:
            self.salva(0)
        else:
            pass
    
    #Aggiornamento tabella   
    def carica_tabella(self, info, indice_reale):     
        img_tk = None

        if info.immagine:                  
            img_pil = Image.open(info.immagine).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img_pil)
            self.salva_immagini.append(img_tk)                #metto l'immagine in una lista perchè se no non viene mostrata nella tabella                    
                    
        self.tabella.insert("", "end", iid=str(indice_reale), image=img_tk, values=(
            info.tipologia, info.nome, info.eta, info.anno,
            info.id, info.numero_pezzi, str(info.prezzo) + " €", info.link
        ))
        
    def aggiorna_tabella(self):
        self.tabella.delete(*self.tabella.get_children())                  #cancella ogni riga della tabella ttk
        self.salva_immagini = []
        
        for indice, dati in enumerate(self.set_lego):                     #enumerate serve a trovare indice del set
            
            self.carica_tabella(dati, indice)
        
    #Ricerca set        
    def cerca(self):
        self.tabella.delete(*self.tabella.get_children())                  
        self.salva_immagini = []
        
        ricerca=self.ent_ricerca.get().lower()
        if self.ent_ricerca.get()=="":
            self.aggiorna_tabella()
            return
            
        for indice, dati in enumerate(self.set_lego):
            if ricerca in str(dati.tipologia).lower() or ricerca in str(dati.nome).lower() or ricerca in str(dati.anno).lower() or ricerca in str(dati.eta).lower() or ricerca in str(dati.id).lower() or ricerca in str(dati.prezzo).lower() or ricerca in str(dati.numero_pezzi).lower():
                self.carica_tabella(dati, indice)
                    
            #commento di Vergani: se gotti avesse usato una lista (che sarebe molto comoda in python) per i dati del singolo set lego, questa sintassi più pulita e concisa sarebbe stata possibile:
            #for i in dati:
                #if (ricerca in i.lower()):
                    #self.carica_tabella(dati)
                    #return      
    
    #Caricamento immagine
    def aggiunta_immagine(self, percorso):
        if percorso:
            img = ctk.CTkImage(light_image=Image.open(percorso), size=(150, 150))
            self.salva_immagini.append(img)
            self.foto.configure(image=img)
        
                
    def immagine(self):
        self.percorso_immagine = filedialog.askopenfilename(defaultextension=".png", title="Scegli un'immagine", filetypes=[("File immagine", "*.png *.jpg *.jpeg")])       
        self.aggiunta_immagine(self.percorso_immagine)
    
    #apertura link
    def apri_link(self, event):
        riga = self.tabella.identify_row(event.y)
        colonna = self.tabella.identify_column(event.x)
        cella = self.tabella.identify_region(event.x, event.y)
        
        if cella == "cell" and colonna == "#8": 
            if riga:
                valori = self.tabella.item(riga, 'values')
                url = valori[7]
                if url:
                    webbrowser.open_new_tab(url)      
    
    #modifica set                
    def modifica(self, event):
        riga = self.tabella.identify_row(event.y)
        
       
        if riga and riga != "":                               #controllo che non vengano cliccati i titoli
            self.indice = int(riga)
            self.percorso_immagine = self.set_lego[self.indice].immagine
            
            self.aggiungi()
            self.aggiunta.configure(text = "Modifica set", command= lambda: self.aggiungere(1))
            self.agg_set.title("Modifica set")    
            
            self.aggiunta_immagine(self.set_lego[self.indice].immagine)      # perchè se modifico un secondo set senza cambiare immagine prende quelle vecchia

            valori = self.tabella.item(riga, 'values')                   
            self.ent1.insert(0,valori[0])
            self.ent2.insert(0,valori[1])
            self.ent3.insert(0,valori[2])
            self.ent4.insert(0,valori[3])
            self.ent5.insert(0,valori[4])
            self.ent6.insert(0,valori[5])
            self.ent7.insert(0,valori[6].replace("€", ""))
            self.ent8.insert(0,valori[7])

    #Elimina set lego
    def elimina(self, event):
        riga = self.tabella.identify_row(event.y)
        
        if riga and riga != "":
            self.indice = int(riga)
            domanda=messagebox.askyesno("Richiesta eliminazione", "Sei sicuro di eliminare il set? verrà perso per sempre") 
            if domanda:            
                self.set_lego.pop(self.indice)      
                self.aggiorna_tabella()
                self.controllo_senza_salvare = True
            else:
                pass    

        
app = App()
app.win.mainloop()