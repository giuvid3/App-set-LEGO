import customtkinter
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from PIL import Image, ImageTk
import json


@dataclass

class lego:
    tipologia: str
    nome: str
    eta: int
    anno: int
    id: str
    numero_pezzi: int
    prezzo: float
    link: str
    immagine: str
    

#funzioni:
    
def chiudi(finestra_da_chiudere):
    if finestra_da_chiudere is not None and finestra_da_chiudere.winfo_exists():
        finestra_da_chiudere.destroy() 
        if finestra_da_chiudere == finestra:       
            win.deiconify()
        else:
            pass



    

#finestre secondarie:
 
finestra = None
agg_set = None 
set_lego = [] 
percorso = None
percorso_immagine = None
referenze_immagini = []
    
def crea(esiste):
    if esiste == 1:
        global percorso
        global set_lego
        global percorso_immagine
        percorso=filedialog.askopenfilename()
        if percorso:
            with open(percorso, "r") as file:
                lista = json.load(file)
                
            set_lego = [] 
              
            for caricare in lista:
                set_caricato = lego(
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
                set_lego.append(set_caricato)
            
            messagebox.showinfo("Perfetto!", "File caricato con successo!")
        else:            
            messagebox.showwarning("Attenzione!", "Qualcosa è andato storto! Apertura gestore vuoto")
            set_lego = []
                    
        
    global finestra    
    if finestra is None or not finestra.winfo_exists():                  #se la finestra esiste o è stata chiusa 
               
        #funzioni finestra:        
        def aggiungi():
            global agg_set
            
            if agg_set is None or not agg_set.winfo_exists():
                agg_set = customtkinter.CTkToplevel(finestra)
                agg_set.geometry("1080x720")
                agg_set.minsize = (1080, 720)
                agg_set.title("Nuovo set")               
                agg_set.grab_set()     
                agg_set.protocol("WM_DELETE_WINDOW", lambda: chiudi(agg_set))   #se premo la x viene eseguito chiudi    
                
                
                
                def immagine():
                    global percorso_immagine
                    percorso_immagine = None
                    percorso_immagine = filedialog.askopenfilename()
                    
                    
                
                
                
                
                
                #inserimento dati
                l1 = ctk.CTkLabel(agg_set, text="Tipologia del set lego:" )
                l1.grid(row=0, column=0, padx=30, pady=20)
                ent1 = ctk.CTkEntry(agg_set, width=300)
                ent1.grid(row=0, column=1, padx=30, pady=20)
                
                l2 = ctk.CTkLabel(agg_set, text="Nome set lego:" )
                l2.grid(row=1, column=0, padx=30, pady=20)
                ent2 = ctk.CTkEntry(agg_set, width=300)
                ent2.grid(row=1, column=1, padx=30, pady=20)
                
                l3 = ctk.CTkLabel(agg_set, text="Età necessaria:" )
                l3.grid(row=2, column=0, padx=30, pady=20)
                ent3 = ctk.CTkEntry(agg_set, width=300)
                ent3.grid(row=2, column=1, padx=30, pady=20)
                
                l4 = ctk.CTkLabel(agg_set, text="Anno di uscita:" )
                l4.grid(row=3, column=0, padx=30, pady=20)
                ent4 = ctk.CTkEntry(agg_set, width=300)
                ent4.grid(row=3, column=1, padx=30, pady=20)
                
                l5 = ctk.CTkLabel(agg_set, text="Id lego:" )
                l5.grid(row=4, column=0, padx=30, pady=20)
                ent5 = ctk.CTkEntry(agg_set, width=300)
                ent5.grid(row=4, column=1, padx=30, pady=20)
                
                limg = ctk.CTkLabel(agg_set, text="Inserisci l'immagine del set:")
                limg.grid(row=4, column=2, padx=30, pady=20)
                btnimg = ctk.CTkButton(agg_set, text="Scegli immagine", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command=immagine)
                btnimg.grid(row=4, column=3, pady=20)
                
                l6 = ctk.CTkLabel(agg_set, text="Numero pezzi:" )
                l6.grid(row=5, column=0, padx=30, pady=20)
                ent6 = ctk.CTkEntry(agg_set, width=300)
                ent6.grid(row=5, column=1, padx=30, pady=20)
                
                l7 = ctk.CTkLabel(agg_set, text="Prezzo(euro):" )
                l7.grid(row=6, column=0, padx=30, pady=20)
                ent7 = ctk.CTkEntry(agg_set, width=300)
                ent7.grid(row=6, column=1, padx=30, pady=20)
                
                l8 = ctk.CTkLabel(agg_set, text="Link al sito ufficiale:" )
                l8.grid(row=7, column=0, padx=30, pady=20)
                ent8 = ctk.CTkEntry(agg_set, width=300)
                ent8.grid(row=7, column=1, padx=30, pady=20)
                
                
                def aggiungere():
                    global percorso_immagine
                    if not (ent1.get() and ent2.get() and ent3.get() and ent4.get() and ent5.get() and ent6.get() and ent7.get() and ent8.get()):
                        messagebox.showwarning("attenzione!", "Devi compilare tutti i campi!")
                    else:

                        try:
                            eta = int(ent3.get())
                            anno = int(ent4.get())
                            numero_pezzi = int(ent6.get())
                            prezzo = float(ent7.get().replace(",", "."))

                        except ValueError:
                            messagebox.showwarning("attenzione!", "Anno, numero pezzi e prezzo devono essere numeri!")
                        else:

                            nuovo_set = lego(
                                tipologia=ent1.get(),
                                nome=ent2.get(),
                                eta=eta,
                                anno=anno,
                                id=ent5.get(),
                                numero_pezzi=numero_pezzi,
                                prezzo=prezzo,
                                link=ent8.get(),
                                immagine=percorso_immagine
                            )

                            set_lego.append(nuovo_set)
                            chiudi(agg_set)
                            aggiorna_tabella()  
                        
                aggiunta = ctk.CTkButton(agg_set, text="Aggiungi il set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command= aggiungere)        
                aggiunta.grid(row=8, column=0, padx=30, pady=20)        
        
        
                        
        def salva(x):
            global percorso
            if not set_lego:
                messagebox.showwarning("Attenzione!", "Lista vuota!")
                return
            else:
                if percorso==None or x == 1:
                    percorso = filedialog.asksaveasfilename(defaultextension=".json", title="scegli dove salvare i set lego", filetypes=[("File JSON", ".json")])

                if percorso:
                    lista = []

                    for set in set_lego:
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

                    with open(percorso, "w") as file:
                        json.dump(lista, file, indent=4)     
                    
         
        #oggetti in finestra:
        
        finestra = customtkinter.CTkToplevel(win)  
        finestra.geometry("1600x900")
        finestra.minsize = (1600, 900)
        finestra.title("Gestore")
        finestra.lift()       
        finestra.protocol("WM_DELETE_WINDOW", lambda: chiudi(finestra))  #se viene premuta la x si esegue la funzione chiudi        
        win.withdraw()                                                   #viene nascosta la win iniziale
        
        
        nset_btn = ctk.CTkButton(finestra, text="Crea nuovo set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command = aggiungi)
        nset_btn.grid(row = 0, column = 0, padx=15, pady =15)
        
        mod_btn = ctk.CTkButton(finestra, text="Modifica un set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12)
        mod_btn.grid(row = 0, column = 1, padx=30, pady =15)
        
        del_btn = ctk.CTkButton(finestra, text="Elimina un set", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12)
        del_btn.grid(row = 0, column = 2, padx=30, pady =15)
        
        save_btn = ctk.CTkButton(finestra, text="Salva", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command=lambda: salva(0))
        save_btn.grid(row = 0, column = 3, padx=30, pady =15)
        
        snome_btn = ctk.CTkButton(finestra, text="Salva con nome", width=150, height=30 , font=ctk.CTkFont(size=20, weight="bold"), cursor="hand2", corner_radius=12, command=lambda: salva(1))
        snome_btn.grid(row = 0, column = 4, padx=30, pady =15)
        
        
        
        tabella = ttk.Treeview(finestra)

        tabella["columns"] = ("Tipologia", "Nome", "Età", "Anno", "ID", "Numero pezzi", "Prezzo", "Link")

        tabella.column("#0", width=80, anchor="center")
        tabella.heading("#0", text="img")       

        for colonna in tabella["columns"]:
            tabella.column(colonna, anchor="center", width=120)            
            tabella.heading(colonna, text=colonna)

        tabella.grid(row=1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
        
        #stile per tabella strano        
        finestra.grid_rowconfigure(1, weight=1)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#F8F9FA", foreground="#222222", fieldbackground="#F8F9FA", rowheight=105, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#FFD500", foreground="#222222", font=("Segoe UI", 11, "bold"), relief="flat")      
        style.map("Treeview", background=[("selected", "#4A90E2")], foreground=[("selected", "white")])
        style.map("Treeview.Heading", background=[("active", "#FFC300")])
        for i in range(5):
            finestra.grid_columnconfigure(i, weight=1)
        
           
        
        def aggiorna_tabella():
            global referenze_immagini
            tabella.delete(*tabella.get_children())
            referenze_immagini.clear()
            for dati in set_lego:
                img_tk = ""                   
                img_pil = Image.open(dati.immagine).resize((100, 100))
                img_tk = ImageTk.PhotoImage(img_pil)
                referenze_immagini.append(img_tk)                         #metto l'immagine in una lista perchè se no non viene mostrata nella tabella                    
                        
                tabella.insert("", "end", image=img_tk, values=(
                    dati.tipologia, dati.nome, dati.eta, dati.anno,
                    dati.id, dati.numero_pezzi, dati.prezzo, dati.link
                ))
            
        aggiorna_tabella()      


#finestra win principale: 

win = ctk.CTk()
win.geometry("1080x720")
win.title("Gestore set LEGO")
win.resizable(True, True)
win.minsize(1080, 720)


crea_btn = ctk.CTkButton(win, text="Crea nuovo gestore", width=400, height=100 , font=ctk.CTkFont(size=40, weight="bold"), cursor="hand2", corner_radius=32, command= lambda: crea(0))
crea_btn.place(relx=0.5, rely=0.4, anchor="center")

apri_btn=ctk.CTkButton(win, text="Apri set già esistenti", width=400, height=100, font=ctk.CTkFont(size=40, weight="bold"), cursor="hand2", corner_radius=32, command=lambda: crea(1))
apri_btn.place(relx=0.5, rely=0.6, anchor="center")


win.mainloop()

































