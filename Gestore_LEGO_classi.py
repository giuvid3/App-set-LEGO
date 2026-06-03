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
        self.info = None                        #|
        self.set_lego = []                      #|
        self.percorso = None                    #|  
        self.percorso_immagine = None           #|  Varibaili generali
        self.salva_immagini = []                #|
        self.controllo_senza_salvare = False    #|
        self.indice= None                       #|

        
        
        
        self.win = ctk.CTk()
        self.win.geometry("1080x720")
        self.win.title("Gestore set LEGO")
        self.win.resizable(False, False)
        self.win.minsize(1080, 720)
        self.win.iconbitmap("icona.ico")
        img_sfondo = ctk.CTkImage(light_image=Image.open("sfondo.png"), dark_image=Image.open("sfondo.png"), size=(1080, 720))
    
        self.label_sfondo = ctk.CTkLabel(self.win, image=img_sfondo, text="")
        self.label_sfondo.place(x=0, y=0, relwidth=1, relheight=1)
        
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
                

            if not isinstance(lista, list):
                messagebox.showerror("Errore", "Formato file non valido, apertura gestore vuoto")
                return

            if len(lista) == 0:
                messagebox.showwarning("Attenzione", "Il file è vuoto")
                return
            self.set_lego = []
            
            for caricare in lista:
                try:
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
                except KeyError:           #se manca un campo
                    messagebox.showerror("Errore", "Formato file non valido, apertura gestore vuoto")
                    return
                    
            
            messagebox.showinfo("Perfetto!", "File caricato con successo!")
        
    #Creazione finestra       
    def crea(self, esiste):
        if esiste == 0:
            self.set_lego = []
        if esiste == 1:
            self.file_esistente()
            
        if self.finestra is None or not self.finestra.winfo_exists(): 
            self.finestra = customtkinter.CTkToplevel(self.win)  
            self.finestra.geometry("1600x820")
            self.finestra.minsize(1600, 820)
            self.finestra.title("Gestore")
            self.finestra.lift()
            self.finestra.protocol("WM_DELETE_WINDOW", lambda: self.chiudi(self.finestra))  #se viene premuta la x si esegue la funzione chiudi        
            self.win.withdraw()         #viene nascosta la win iniziale
            
            info_btn = ctk.CTkButton(self.finestra, text="Informazioni", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command= self.informazioni)
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
            self.tabella["columns"] = ("Indice", "Tipologia", "Nome", "Età", "Anno", "ID", "Numero pezzi", "Prezzo", "Link")
            self.tabella.column("#0", width=80, anchor="center")
            self.tabella.heading("#0", text="img")
            self.tabella.column("Indice", width=50, anchor="center")
            self.tabella.heading("Indice", text="Indice")
             
            self.tabella.bind("<Button-1>", self.apri_link)      
            self.tabella.bind("<Double-1>", self.modifica)
            self.tabella.bind("<Button-3>", self.elimina)
            
            for colonna in self.tabella["columns"][1:]:
                self.tabella.column(colonna, anchor="center", width=120)            
                self.tabella.heading(colonna, text=colonna)
                
            scrollbar = ctk.CTkScrollbar(self.finestra, orientation="vertical", command=self.tabella.yview)
            self.tabella.configure(yscrollcommand=scrollbar.set)

            scrollbar.grid(row=1, column=5, sticky="ns")
            self.tabella.grid(row=1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
            
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
    
    #Chiusura finestre
    def chiudi(self, finestra_da_chiudere):
        if self.controllo_senza_salvare==True and finestra_da_chiudere== self.finestra:
            if not self.sicuro():
                return

        if finestra_da_chiudere is not None and finestra_da_chiudere.winfo_exists():
            finestra_da_chiudere.destroy() 
            if finestra_da_chiudere == self.finestra:       
                self.win.deiconify()            #La finestra viene ripristinata
            else:
                pass    
    
    #Finestra aggiunta set lego
    def aggiungi(self):        
                    
        if self.agg_set is None or not self.agg_set.winfo_exists():
            self.agg_set = customtkinter.CTkToplevel(self.finestra)
            self.agg_set.geometry("950x720")
            self.agg_set.minsize(950, 720)
            self.agg_set.resizable(False, False)
            self.agg_set.title("Nuovo set")
            self.agg_set.grab_set()
            self.agg_set.protocol("WM_DELETE_WINDOW", lambda: self.chiudi(self.agg_set))

            titolo = ctk.CTkLabel(self.agg_set, text="➕ Aggiungi un nuovo Set LEGO", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3C64BB")
            titolo.grid(row=0, column=0, columnspan=3, pady=(20, 30))

            frame_img = ctk.CTkFrame(self.agg_set, width=300, corner_radius=15)                 #frame immagine che occupa 9 righe
            frame_img.grid(row=1, column=2, rowspan=8, padx=(40, 30), pady=20, sticky="nsew")         
            frame_img.grid_columnconfigure(0, weight=1)
            frame_img.grid_rowconfigure(0, weight=1)    #le righe si adattano per rendere centrato il contenuto
            frame_img.grid_rowconfigure(1, weight=0)
            frame_img.grid_rowconfigure(2, weight=0)
            frame_img.grid_rowconfigure(3, weight=1)
            
            limg = ctk.CTkLabel(frame_img, text="Immagine del set", font=ctk.CTkFont(size=22, weight="bold"))
            limg.grid(row=0, column=0, padx=20, pady=(20, 10))

            btnimg = ctk.CTkButton(frame_img, text="Scegli immagine", width=180, height=35, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=12, command=self.immagine)
            btnimg.grid(row=3, column=0, padx=20, pady=(10, 20))

            self.foto = ctk.CTkLabel(frame_img, text="", width=220, height=220)
            self.foto.grid(row=2, column=0, padx=20, pady=20)

            l1 = ctk.CTkLabel(self.agg_set, text="Tipologia del set lego:", font=ctk.CTkFont(size=14, weight="bold"))
            l1.grid(row=1, column=0, padx=30, pady=20)
            self.ent1 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent1.grid(row=1, column=1, padx=30, pady=20)

            l2 = ctk.CTkLabel(self.agg_set, text="Nome set lego:", font=ctk.CTkFont(size=14, weight="bold"))
            l2.grid(row=2, column=0, padx=30, pady=20)
            self.ent2 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent2.grid(row=2, column=1, padx=30, pady=20)

            l3 = ctk.CTkLabel(self.agg_set, text="Età necessaria:", font=ctk.CTkFont(size=14, weight="bold"))
            l3.grid(row=3, column=0, padx=30, pady=20)
            self.ent3 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent3.grid(row=3, column=1, padx=30, pady=20)

            l4 = ctk.CTkLabel(self.agg_set, text="Anno di uscita:", font=ctk.CTkFont(size=14, weight="bold"))
            l4.grid(row=4, column=0, padx=30, pady=20)
            self.ent4 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent4.grid(row=4, column=1, padx=30, pady=20)

            l5 = ctk.CTkLabel(self.agg_set, text="Id lego:", font=ctk.CTkFont(size=14, weight="bold"))
            l5.grid(row=5, column=0, padx=30, pady=20)
            self.ent5 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent5.grid(row=5, column=1, padx=30, pady=20)

            l6 = ctk.CTkLabel(self.agg_set, text="Numero pezzi:", font=ctk.CTkFont(size=14, weight="bold"))
            l6.grid(row=6, column=0, padx=30, pady=20)
            self.ent6 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent6.grid(row=6, column=1, padx=30, pady=20)

            l7 = ctk.CTkLabel(self.agg_set, text="Prezzo(euro):", font=ctk.CTkFont(size=14, weight="bold"))
            l7.grid(row=7, column=0, padx=30, pady=20)
            self.ent7 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent7.grid(row=7, column=1, padx=30, pady=20)

            l8 = ctk.CTkLabel(self.agg_set, text="Link al sito ufficiale:", font=ctk.CTkFont(size=14, weight="bold"))
            l8.grid(row=8, column=0, padx=30, pady=20)
            self.ent8 = ctk.CTkEntry(self.agg_set, width=300)
            self.ent8.grid(row=8, column=1, padx=30, pady=20)

            self.aggiunta = ctk.CTkButton(self.agg_set, text="💾 Aggiungi il Set", width=150, height=30, font=ctk.CTkFont(size=18, weight="bold"), cursor="hand2", corner_radius=12, fg_color="#2E8B57", hover_color="#246B45",command=lambda: self.aggiungere(0))
            self.aggiunta.grid(row=9, column=1, pady=20)
    
    #Aggiunta set lego            
    def aggiungere(self, x):
        if not (self.ent1.get() and self.ent2.get() and self.ent3.get() and self.ent4.get() and self.ent5.get() and self.ent6.get() and self.ent7.get() and self.ent8.get()):
            messagebox.showwarning("attenzione!", "Devi compilare tutti i campi!")
        elif not self.foto.cget("image"):
            messagebox.showwarning("attenzione!", "Foto mancante, inseriscine una!")
         
        else:
            for i in self.set_lego:
                    if i.id == self.ent5.get() and x ==0 :
                        messagebox.showwarning("Attenzione!", "Id set lego già esistente! Inseriscine un'altro")
                        return
            try:
                eta = int(self.ent3.get())
                anno = int(self.ent4.get())
                numero_pezzi = int(self.ent6.get())
                prezzo = float(self.ent7.get().replace(",", "."))
                
                if (eta < 0 or anno < 0 or numero_pezzi < 0 or prezzo < 0):
                    messagebox.showwarning("attenzione!", "Controlla che i valori di età, anno, numero pezzi e prezzo siano positivi!") 
                    return
                
                
            except ValueError:
                messagebox.showwarning("attenzione!", "Anno, numero, pezzi e prezzo devono essere numeri!")
                return
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
            messagebox.showwarning("Attenzione!", "Nessun set LEGO inserito!")
            return
        else:
            if self.percorso==None or x == 1:
                self.percorso = filedialog.asksaveasfilename(defaultextension=".json", title="Scegli dove salvare i set lego", filetypes=[("File JSON", ".json")])
            if not self.percorso:    #se viene chiusa la scheda il percorso non c'è ed esce dalla funzione
                return
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

            if self.controllo_senza_salvare:
                return False

        return True
    
    #Aggiornamento tabella   
    def carica_tabella(self, info, indice_reale):     
        img_tk = None

        if info.immagine:                  
            try:
                img_pil = Image.open(info.immagine).resize((100, 100))
                img_tk = ImageTk.PhotoImage(img_pil)
                self.salva_immagini.append(img_tk)             #metto l'immagine in una lista perchè se no non viene mostrata nella tabella  
            except:
                img_tk =None
                                              
                    
        self.tabella.insert("", "end", iid=str(indice_reale), image=img_tk, values=(
            indice_reale + 1, info.tipologia, info.nome, info.eta, info.anno,
            info.id, info.numero_pezzi, str(info.prezzo) + " €", info.link
        ))
        
    def aggiorna_tabella(self):
        self.salva_immagini = []
        self.tabella.delete(*self.tabella.get_children())                  #cancella ogni riga della tabella ttk
        
        
        for indice, dati in enumerate(self.set_lego):                     #enumerate serve a restituire indice e dato del set nello stesso momento
            
            self.carica_tabella(dati, indice)
        
    #Ricerca set        
    def cerca(self):
        self.tabella.delete(*self.tabella.get_children())                  
        self.salva_immagini = []
        
        ricerca=self.ent_ricerca.get().strip().lower()
        if ricerca == "":
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
            img = ctk.CTkImage(light_image=Image.open(percorso), size=(220, 220))
            self.salva_immagini.append(img)
            self.foto.configure(image=img)
      
    #Aggiunta immagine              
    def immagine(self):
        self.percorso_immagine = filedialog.askopenfilename(defaultextension=".png", title="Scegli un'immagine", filetypes=[("File immagine", "*.png *.jpg *.jpeg")])       
        self.aggiunta_immagine(self.percorso_immagine)
    
    #Apertura link
    def apri_link(self, event):
        riga = self.tabella.identify_row(event.y)
        colonna = self.tabella.identify_column(event.x)
        cella = self.tabella.identify_region(event.x, event.y)
        
        if cella == "cell" and colonna == "#9": 
            if riga:
                valori = self.tabella.item(riga, 'values')
                url = valori[8]
                if url.startswith("http://") or url.startswith("https://"):
                    webbrowser.open_new_tab(url)      
                else:
                    messagebox.showwarning("Attenzione!", "Link non valido")
    
    #Modifica set                
    def modifica(self, event):
        riga = self.tabella.identify_row(event.y)
        
       
        if riga and riga != "":                               #controllo che non vengano cliccati i titoli
            self.indice = int(riga)
            self.percorso_immagine = self.set_lego[self.indice].immagine
            
            if self.agg_set is None or not self.agg_set.winfo_exists():
                self.aggiungi()
                
            self.aggiunta.configure(text = "Modifica set", command= lambda: self.aggiungere(1))
            self.agg_set.title("Modifica set")    
            
            self.aggiunta_immagine(self.set_lego[self.indice].immagine)      # perchè se modifico un secondo set senza cambiare immagine prende quelle vecchia

            valori = self.tabella.item(riga, 'values')
            for e in [self.ent1, self.ent2, self.ent3, self.ent4, self.ent5, self.ent6, self.ent7, self.ent8]:    #Pulizia entry precedenti
                e.delete(0, "end")
                               
            self.ent1.insert(0,valori[1])
            self.ent2.insert(0,valori[2])
            self.ent3.insert(0,valori[3])
            self.ent4.insert(0,valori[4])
            self.ent5.insert(0,valori[5])
            self.ent6.insert(0,valori[6])
            self.ent7.insert(0,valori[7].replace("€", ""))
            self.ent8.insert(0,valori[8])
        
        self.controllo_senza_salvare = True
    
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
    
    #Informazione sul programma
    def informazioni(self):
        if self.info is None or not self.info.winfo_exists():
            self.info = customtkinter.CTkToplevel(self.finestra)
            self.info.geometry("1080x720")
            self.info.minsize(1080, 900)
            self.info.config(background="white")
            self.info.title("Informazioni sul programma")               
            self.info.grab_set()
            self.info.protocol("WM_DELETE_WINDOW", lambda: self.chiudi(self.info))
            
            self.frame = ctk.CTkScrollableFrame(self.info, fg_color="white")
            self.frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
            
            self.info.grid_rowconfigure(0, weight=1)
            self.info.grid_columnconfigure(0, weight=1)
            
            titolo = ctk.CTkLabel(self.frame, text="GESTORE SET LEGO", font=ctk.CTkFont(size=30, weight="bold"))
            titolo.pack(pady=(10, 25))
            
            testo = """
                Autore
                ------------------------
                Applicazione sviluppata da Davide Gotti.

                Scopo dell'applicazione
                ------------------------
                Questo programma permette di creare e gestire una collezione di set LEGO.
                È possibile aggiungere, modificare, eliminare, cercare e salvare i set
                all'interno di file JSON.

                Funzionalità principali
                ------------------------
                • Creazione di nuovi set LEGO
                • Modifica dei set esistenti
                • Eliminazione dei set
                • Ricerca rapida nella tabella
                • Salvataggio e caricamento dei dati
                • Gestione immagini dei set
                • Apertura del link ufficiale direttamente dal programma

                Comandi rapidi
                ------------------------
                • Doppio click su una riga:
                Modifica il set selezionato.

                • Click destro su una riga:
                Elimina il set selezionato.

                • Click sul link:
                Apre il sito ufficiale del set nel browser.

                • Pulsante "Salva":
                Salva il file corrente.

                • Pulsante "Salva con nome":
                Salva il progetto in un nuovo file JSON.

                • Barra di ricerca:
                Permette di trovare rapidamente un set tramite:
                nome, tipologia, anno, ID, prezzo o numero pezzi.

                Formato dei dati
                ------------------------
                I set vengono salvati in formato JSON per garantire:
                • semplicità
                • leggibilità
                • compatibilità
                • facilità di modifica

                Copyright
                ------------------------
                © 2026 Davide Gotti
                Tutti i diritti riservati.

                Questo software è stato realizzato a scopo didattico e personale.
                        """
                        
                        
            lbtesto = ctk.CTkLabel(self.frame, text=testo, justify="left", anchor="w", font=ctk.CTkFont(size=16))
            lbtesto.pack(fill="both", expand=True, padx=20, pady=10)
          
            
app = App()
app.win.mainloop()
