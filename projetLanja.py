import customtkinter as ctk
from tkinter import messagebox, filedialog, Menu
import mysql.connector
from PIL import Image, ImageTk
import io

montre = ""


# Fonction pour se connecter à la base de données
def connexion_db():
    try:
        connex = mysql.connector.connect(
            host="localhost",
            user="lanja",
            password="fritekechup",
            database="bassl22_db"
        )
        return connex
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur lors de la tentative de connexion", f"Erreur: {err}")
        return None



# Login administrateur
def login():
    fenetreLogin = ctk.CTk()
    fenetreLogin.title("Acces a bassl22")
    fenetreLogin.geometry("300x250")

    def verification_login():
        if nomUtilisateur.get() == "lanja" and motDePasse.get() == "fritekechup":
            messagebox.showinfo("Login", "Login réussi!")
            fenetreLogin.destroy()
            menu_principal()
        else:
            messagebox.showerror("Login", "Nom d'utilisateur ou mot de passe incorrect")

    ctk.CTkLabel(fenetreLogin, text="Nom d'utilisateur").pack(pady=10)
    nomUtilisateur = ctk.CTkEntry(fenetreLogin)
    nomUtilisateur.pack(pady=10)

    ctk.CTkLabel(fenetreLogin, text="Mot de passe").pack(pady=10)
    motDePasse = ctk.CTkEntry(fenetreLogin, show="*")
    motDePasse.pack(pady=10)

    ctk.CTkButton(fenetreLogin, text="Login", command=verification_login, hover_color="darkred").pack(pady=20)

    fenetreLogin.mainloop()



# Interface Graphique principale
def menu_principal():
    global ecran
    ecran = ctk.CTk()
    ecran.geometry("800x600")
    ecran.title("BassL22 - Gestion des Employés")
    ecran.grid_rowconfigure(0, weight=1)
    ecran.grid_rowconfigure(2, weight=1)
    ecran.grid_columnconfigure(0, weight=1)
    ecran.grid_columnconfigure(2, weight=1)

    global frame
    frame = ctk.CTkFrame(master=ecran)

    menu = Menu(ecran)
    menuAction = Menu(menu, tearoff=0)
    menuAction.add_command(label="✙ Ajouter un employé", command=ajout_employe)
    menuAction.add_command(label="⛁ Liste des employés", command=afficher_employes_simple)
    menuAction.add_command(label="✎ Modifier un employé", command=interface_utile_modif)
    menuAction.add_command(label="✘ Exclure ou supprimer un employé", command=interface_utile_suppr)
    menuAction.add_command(label="☒ Liste des virés", command= liste_vires)
    menuAction.add_command(label="⚒ Départements", command=lister_departements)
    menu.add_cascade(label="Actions", menu=menuAction)

    menuOption = Menu(menu, tearoff=0)
    menuOption.add_command(label="☼ Changer le thème", command=changer_theme)
    menu.add_cascade(label="Option", menu=menuOption)

    menuApropos = Menu(menu, tearoff=0)
    menuApropos.add_command(label="? À propos de BassL22", command=a_propos)
    menu.add_cascade(label="A propos", menu=menuApropos)

    if montre == "departmt":
        lister_departements()

    ecran.config(menu=menu)
    ecran.mainloop()



# Menu départements
def lister_departements():
    reinitialiser_frame()
    frame.grid(row=1, column=1, padx=10, pady=10)

    rh = ctk.CTkButton(frame, command= lambda: afficher_employes_options('departement', 'RH'), text="Ressources humaines", font=("Verdana", 30), width=375, height=80, hover_color="orangered")
    rh.grid(row=0, column=0, padx=10, pady=10)
    marketing = ctk.CTkButton(frame, command= lambda: afficher_employes_options('departement', 'Marketing'), text="Marketing", font=("Verdana", 30), width=375, height=80, hover_color="darkred")
    marketing.grid(row=0, column=1, padx=10, pady=10)
    informatique = ctk.CTkButton(frame, command= lambda: afficher_employes_options('departement', 'Informatique'), text="Informatique", font=("Verdana", 30), width=375, height=80, hover_color="darkgreen")
    informatique.grid(row=1, column=0, padx=10, pady=10)
    sec = ctk.CTkButton(frame,command= lambda: afficher_employes_options('departement', 'Securité'), text="Sécurité", font=("Verdana", 30), width=375, height=80, hover_color="deepskyblue2")
    sec.grid(row=1, column=1, padx=10, pady=10)
    travaux = ctk.CTkButton(frame, command= lambda: afficher_employes_options('departement', 'Travaux'), text="Travaux", font=("Verdana", 30), width=375, height=80, hover_color="gold4")
    travaux.grid(row=2, column=0, padx=10, pady=10)
    autres = ctk.CTkButton(frame, command= lambda: afficher_employes_options('departement', 'Autre'), text="Autres", font=("Verdana", 30), width=375, height=80, hover_color="grey9")
    autres.grid(row=2, column=1, padx=10, pady=10)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)



# Ajout d'un employé
def ajout_employe():

    reinitialiser_frame()
    frame.pack(fill="both", expand="true")
    for i in range(4):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(6):
        frame.grid_columnconfigure(j, weight=1)

    def save_employe():
        nom = entry_nom.get()
        date_naissance = entry_date_naissance.get()
        adresse = entry_adresse.get()
        date_embauche = entry_date_embauche.get()
        departement = depart.get()

        photo = None
        if photo_path:
            with open(photo_path, 'rb') as file:
                photo = file.read()

        conn = connexion_db()
        if conn:
            curseur = conn.cursor()
            sql = "INSERT INTO employes (nom, date_naissance, adresse, date_embauche, departement, photo) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nom, date_naissance, adresse, date_embauche, departement, photo)
            try:
                curseur.execute(sql, val)
                conn.commit()
                messagebox.showinfo("Succès", "Employé ajouté avec succès!")
                afficher_employes_simple()
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur: {err}")
            finally:
                curseur.close()
                conn.close()

    def select_photo():
        nonlocal photo_path
        photo_path = filedialog.askopenfilename()
        if photo_path:
            img = Image.open(photo_path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            label_photo.configure(image=img, text="")
            bouton_photo.configure(text="Changer la photo")
            label_photo.image = img

    photo_path = None

    ctk.CTkLabel(frame, text="Nom").grid(row=0, column=0, padx=5, pady=5)
    entry_nom = ctk.CTkEntry(frame, width=200)
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Date de naissance\n(AAAA-MM-JJ)").grid(row=1, column=0, padx=5, pady=5)
    entry_date_naissance = ctk.CTkEntry(frame, width=100)
    entry_date_naissance.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Adresse").grid(row=2, column=0, padx=5, pady=5)
    entry_adresse = ctk.CTkEntry(frame, width=200)
    entry_adresse.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Date d'embauche\n(AAAA-MM-JJ)").grid(row=0, column=5, padx=5, pady=5)
    entry_date_embauche = ctk.CTkEntry(frame, width=100)
    entry_date_embauche.grid(row=0, column=6, padx=5, pady=5)

    depart = ctk.StringVar(value="RH")
    ctk.CTkLabel(frame, text="Département").grid(row=1, column=5, padx=5, pady=5)
    entry_departement = ctk.CTkOptionMenu(frame, variable=depart, values=["RH", "Marketing", "Informatique", "Securité", "Travaux", "Autre"], width=200, dropdown_fg_color="darkred", dropdown_hover_color="black", button_color="darkred", button_hover_color="black").grid(row=1, column=6, padx=5, pady=5)

    label_photo = ctk.CTkLabel(frame, font=("Verdana", 10), text="Pas de photo", fg_color="grey40", text_color="black", corner_radius=3, width=100, height=100)
    label_photo.grid(row=2, column=5, padx=5, pady=5)
    bouton_photo = ctk.CTkButton(frame, text="Choisir une photo", command=select_photo)
    bouton_photo.grid(row=2, column=6, padx=5, pady=5)

    ctk.CTkButton(frame, text="Ajouter", command=save_employe, fg_color="cyan4", hover_color="darkolivegreen").grid(row=3, column=3, padx=5, pady=5)



# Modification du theme
def changer_theme():
    reinitialiser_frame()
    frame.pack(fill="both", expand="true")
    def set_theme(theme):
        if theme == "Clair":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    ctk.CTkLabel(frame, text="Sélectionnez le thème").pack(pady=10)
    ctk.CTkButton(frame, text="Clair", fg_color="grey70", text_color="black", border_color="black", border_width=3, corner_radius=75, command=lambda: set_theme("Clair")).pack(pady=10)
    ctk.CTkButton(frame, text="Sombre", fg_color="grey10", text_color="white", border_color="grey45", border_width=3, corner_radius=75, command=lambda: set_theme("Sombre")).pack(pady=10)



# Interface ilaina @ modification
def interface_utile_modif():
    reinitialiser_frame()
    frame.pack(fill="both", expand="true")

    def centrer_widgets(*widgets):
        for widget in widgets:
            widget.pack(side="left", padx=10)

    frame_recherche = ctk.CTkFrame(frame)
    frame_recherche.pack(pady=20)

    def executer():
        exp_reg = barreRecherche.get()
        liste_pour_modifier(exp_reg)

    labelRecherche = ctk.CTkLabel(frame_recherche, text="Recherche")
    barreRecherche = ctk.CTkEntry(frame_recherche, width=300)
    boutonRecherche = ctk.CTkButton(frame_recherche, text="ok", width=10, command=executer)

    centrer_widgets(labelRecherche, barreRecherche, boutonRecherche)

    frame_boutons = ctk.CTkFrame(frame)
    frame_boutons.pack(expand = True)

    ctk.CTkButton(frame_boutons, text="Ressources Humaines", command=lambda : liste_modification("departement","RH"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Marketing", command=lambda : liste_modification("departement","Marketing"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Informatique", command=lambda : liste_modification("departement","Informatique"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Sécurité", command=lambda : liste_modification("departement","Securité"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Travaux", command=lambda : liste_modification("departement","Travaux"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Autres", command=lambda : liste_modification("departement","Autres"), width=375, height=50).pack(pady=10)



# Liste anle norecherchena ho modifiena
def liste_pour_modifier(exp):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    #Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i==0 or i==1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    rekety = """
    SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE LOWER(nom) LIKE %s;
    """
    curseur.execute(rekety, (f'%{exp.lower()}%',))
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        #Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw", width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70,70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0,)
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: modifier_profil(emp_id))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



# Liste anle norecherchena ho modifiena
def liste_pour_supprimer(exp):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    #Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i==0 or i==1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    rekety = """
    SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE LOWER(nom) LIKE %s;
    """
    curseur.execute(rekety, (f'%{exp.lower()}%',))
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        #Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw", width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70,70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0,)
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: supprimer_profil_rech(emp_id, exp))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



# Interface ilaina @ suppression
def interface_utile_suppr():
    reinitialiser_frame()
    frame.pack(fill="both", expand="true")

    def centrer_widgets(*widgets):
        for widget in widgets:
            widget.pack(side="left", padx=10)

    frame_recherche = ctk.CTkFrame(frame,)
    frame_recherche.pack(pady=20)

    def executer():
        exp_reg = barreRecherche.get()
        liste_pour_supprimer(exp_reg)

    labelRecherche = ctk.CTkLabel(frame_recherche, text="Recherche")
    barreRecherche = ctk.CTkEntry(frame_recherche, width=300)
    boutonRecherche = ctk.CTkButton(frame_recherche, text="ok", width=10, command=executer)

    centrer_widgets(labelRecherche, barreRecherche, boutonRecherche)

    frame_boutons = ctk.CTkFrame(frame)
    frame_boutons.pack(expand = True)

    ctk.CTkButton(frame_boutons, text="Ressources Humaines", command=lambda: liste_suppression("departement","RH"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Marketing", command=lambda: liste_suppression("departement","Marketing"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Informatique", command=lambda: liste_suppression("departement","Informatique"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Sécurité", command=lambda: liste_suppression("departement","Securité"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Travaux", command=lambda: liste_suppression("departement","Travaux"), width=375, height=50).pack(pady=10)
    ctk.CTkButton(frame_boutons, text="Autres", command=lambda: liste_suppression("departement","Autres"), width=375, height=50).pack(pady=10)



# Miafficher anle liste d'employes
def afficher_employes_simple():
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    #Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i==0 or i==1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    curseur.execute("SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE statut !='exclu' ORDER BY id DESC")
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        #Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0,y_position), window=emp_frame, anchor="nw", width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70,70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0,)
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: afficher_profil_simple(emp_id))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



# Miafficher anle profil avy ao amle liste d'employes mba ahamora2 anle retour
def afficher_profil_simple(id):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame_header = ctk.CTkFrame(frame)
    frame_header.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    bouton = ctk.CTkButton(frame_header, text="⇦", font=("Arial", 30), command=afficher_employes_simple)
    bouton.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    conn = connexion_db()
    curseur = conn.cursor()

    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()

    img_data = io.BytesIO(employe[6])
    img = Image.open(img_data)
    img.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(img)
    photo_label = ctk.CTkLabel(frame, image=photo)
    photo_label.image = photo
    photo_label.configure(text="", bg_color="yellow")
    photo_label.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    ctk.CTkLabel(frame, text=f"{employe[1]}", font=("Courier", 25)).place(x=450, y=130)
    ctk.CTkLabel(frame, text=f"Département: \t{employe[2]}", font=("Arial Black", 15)).place(x=450, y=350)
    ctk.CTkLabel(frame, text=f"Adresse: \t\t{employe[3]}", font=("Arial Black", 15)).place(x=450, y=380)
    ctk.CTkLabel(frame, text=f"Statut: \t\t{employe[4]}", font=("Arial Black", 15)).place(x=450, y=410)
    ctk.CTkLabel(frame, text=f"Date d'embauche: \t{employe[5]}", font=("Arial Black", 15)).place(x=450, y=440)



#Miafficher liste arakarkze ilaina
def afficher_employes_options(op1, op2):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    #Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i==0 or i==1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE ({op1}='{op2}' AND statut='actif') ORDER BY id DESC")
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        #Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw", width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70,70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0,)
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: afficher_profil(emp_id, op1, op2))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



#Miafficher anle voaroaka rehetra
def liste_vires():
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    #Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i==0 or i==1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE statut='exclu' ORDER BY id DESC")
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        #Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw", width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70,70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0,)
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y= 30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: afficher_profil_exclu(emp_id))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



#Miafficher anle liste ho supprimena a parir anle departement
def liste_suppression(op1, op2):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    # Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i == 0 or i == 1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    curseur.execute(
        f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE ({op1}='{op2}' AND statut='actif') ORDER BY id DESC")
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        # Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw",
                                                width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70, 70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0, )
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y=30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y=30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y=30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y=30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: supprimer_profil(emp_id, op1, op2))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



#Miafficher anle liste ho supprimena a partir anle departement
def liste_modification(op1, op2):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    conn = connexion_db()
    curseur = conn.cursor()

    # Mamboatra anle titre eny ambony
    frame_header = ctk.CTkFrame(frame)
    frame_header.pack(fill="x")
    labels = ["Photo", "Nom", "Département", "Adresse", "Statut", "Date d'embauche"]
    for i, text in enumerate(labels):
        if i == 0 or i == 1:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=30, pady=5, sticky="w")
            frame_header.columnconfigure(i, weight=1)
        else:
            label = ctk.CTkLabel(frame_header, text=text)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            frame_header.columnconfigure(i, weight=1)

    curseur.execute(
        f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE ({op1}='{op2}' AND statut='actif') ORDER BY id DESC")
    employes = curseur.fetchall()

    def populate_canvas(canvas):
        # Mamboatra frame tsirairay ho anle mpiasa
        y_position = 0
        emp_frames = []

        def miseajour_empframe(event):
            canvas_width = event.width
            for emp_frame in emp_frames:
                canvas.itemconfig(emp_frame, width=canvas_width)

        for emp in employes:
            emp_frame = ctk.CTkFrame(canvas, height=100)
            emp_frame.pack(fill="x", pady=10, padx=10)
            emp_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            emp_frame_id = canvas.create_window((0, y_position), window=emp_frame, anchor="nw",
                                                width=canvas.winfo_width())
            emp_frames.append(emp_frame_id)
            y_position += 100

            if emp[6]:
                img_data = io.BytesIO(emp[6])
                img = Image.open(img_data)
                img.thumbnail((70, 70))
                photo = ImageTk.PhotoImage(img)
                photo_label = ctk.CTkLabel(emp_frame, image=photo)
                photo_label.image = photo
                photo_label.configure(text="", width=0, )
                photo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            else:
                ctk.CTkLabel(emp_frame, text="Pas de photo").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            ctk.CTkLabel(emp_frame, text=emp[1]).place(x=150, y=30)
            ctk.CTkLabel(emp_frame, text=emp[2]).place(x=500, y=30)
            ctk.CTkLabel(emp_frame, text=emp[3]).place(x=650, y=30)
            ctk.CTkLabel(emp_frame, text=emp[4]).place(x=940, y=30)
            ctk.CTkLabel(emp_frame, text=emp[5]).grid(row=0, column=5, padx=80, pady=10, sticky="e")

            emp_frame.bind("<Button-1>", lambda e, emp_id=emp[0]: modifier_profil(emp_id))
            canvas.bind("<Configure>", miseajour_empframe)

    def on_canvas_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Mamboatra anle canvas misy anle frames sy ny barre de défilement
    canvas = ctk.CTkCanvas(frame, bg="grey36")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    populate_canvas(canvas)

    canvas.bind("<Configure>", lambda e: on_canvas_configure(canvas))



#Miafficher profil an'olona ahafahana migerer retour
def afficher_profil(id,op1,op2):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame_header = ctk.CTkFrame(frame)
    frame_header.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    bouton = ctk.CTkButton(frame_header, text="⇦", font=("Arial", 30), command=lambda :afficher_employes_options(op1,op2))
    bouton.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    conn = connexion_db()
    curseur = conn.cursor()

    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo, motif FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()


    img_data = io.BytesIO(employe[6])
    img = Image.open(img_data)
    img.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(img)
    photo_label = ctk.CTkLabel(frame, image=photo)
    photo_label.image = photo
    photo_label.configure(text="", bg_color="yellow")
    photo_label.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    ctk.CTkLabel(frame, text=f"{employe[1]}", font=("Courier", 25)).place(x=450, y=130)

    if employe[4] == "exclu":
        ctk.CTkLabel(frame, text="Motif de l'exclusion: \t", font=("Arial Black", 15)).place(x=450, y=200)
        labs = ctk.CTkLabel(frame, text=f"{employe[7]}", font=("Arial Black", 15), text_color="red", wraplength=320, width=320)
        labs.place(x=450, y=230)


    ctk.CTkLabel(frame, text=f"Département: \t{employe[2]}", font=("Arial Black", 15)).place(x=450, y=350)
    ctk.CTkLabel(frame, text=f"Adresse: \t\t{employe[3]}", font=("Arial Black", 15)).place(x=450, y=380)
    ctk.CTkLabel(frame, text=f"Statut: \t\t{employe[4]}", font=("Arial Black", 15)).place(x=450, y=410)
    ctk.CTkLabel(frame, text=f"Date d'embauche: \t{employe[5]}", font=("Arial Black", 15)).place(x=450, y=440)



#Miafficher profil an'olona voaroaka
def afficher_profil_exclu(id):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame_header = ctk.CTkFrame(frame)
    frame_header.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    bouton = ctk.CTkButton(frame_header, text="⇦", font=("Arial", 30), command=liste_vires)
    bouton.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    conn = connexion_db()
    curseur = conn.cursor()

    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo, motif FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()


    img_data = io.BytesIO(employe[6])
    img = Image.open(img_data)
    img.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(img)
    photo_label = ctk.CTkLabel(frame, image=photo)
    photo_label.image = photo
    photo_label.configure(text="", bg_color="yellow")
    photo_label.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    ctk.CTkLabel(frame, text=f"{employe[1]}", font=("Courier", 25)).place(x=450, y=130)

    if employe[4] == "exclu":
        ctk.CTkLabel(frame, text="Motif de l'exclusion: \t", font=("Arial Black", 15)).place(x=450, y=200)
        labs = ctk.CTkLabel(frame, text=f"{employe[7]}", font=("Arial Black", 15), text_color="red", wraplength=320, width=320)
        labs.place(x=450, y=230)


    ctk.CTkLabel(frame, text=f"Département: \t{employe[2]}", font=("Arial Black", 15)).place(x=450, y=350)
    ctk.CTkLabel(frame, text=f"Adresse: \t\t{employe[3]}", font=("Arial Black", 15)).place(x=450, y=380)
    ctk.CTkLabel(frame, text=f"Statut: \t\t{employe[4]}", font=("Arial Black", 15)).place(x=450, y=410)
    ctk.CTkLabel(frame, text=f"Date d'embauche: \t{employe[5]}", font=("Arial Black", 15)).place(x=450, y=440)



#Misupprimer profil a partir anle departement
def supprimer_profil(id,op1,op2):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame_header = ctk.CTkFrame(frame)
    frame_header.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    bouton = ctk.CTkButton(frame_header, text="⇦", font=("Arial", 30), command=lambda: liste_suppression(op1, op2))
    bouton.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    conn = connexion_db()
    curseur = conn.cursor()

    def supprimer(id_olona):
        motif = entry_motif.get("1.0", "end-1c")
        conn = connexion_db()
        if conn:
            curseur = conn.cursor()
            sql = f"UPDATE employes SET motif='{motif}', statut='exclu' WHERE id={id_olona}"
            try:
                curseur.execute(sql)
                conn.commit()
                messagebox.showinfo("Succès", "Employé renvoyé(e)!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur: {err}")
            finally:
                curseur.close()
                conn.close()
        afficher_employes_options("statut","exclu")



    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()

    img_data = io.BytesIO(employe[6])
    img = Image.open(img_data)
    img.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(img)
    photo_label = ctk.CTkLabel(frame, image=photo)
    photo_label.image = photo
    photo_label.configure(text="", bg_color="yellow")
    photo_label.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    ctk.CTkLabel(frame, text=f"{employe[1]}", font=("Courier", 25)).place(x=450, y=130)
    ctk.CTkLabel(frame, text="Motif du renvoi:", font=("Verdana", 8)).place(x=450, y=160)
    entry_motif = ctk.CTkTextbox(frame, width=310, height=150)
    entry_motif.place(x=450, y=190)
    ctk.CTkLabel(frame, text=f"Département: \t{employe[2]}", font=("Arial Black", 15)).place(x=450, y=350)
    ctk.CTkLabel(frame, text=f"Adresse: \t\t{employe[3]}", font=("Arial Black", 15)).place(x=450, y=380)
    ctk.CTkLabel(frame, text=f"Statut: \t\t{employe[4]}", font=("Arial Black", 15)).place(x=450, y=410)
    ctk.CTkLabel(frame, text=f"Date d'embauche: \t{employe[5]}", font=("Arial Black", 15)).place(x=450, y=440)
    ctk.CTkButton(frame, text="Supprimer", fg_color="darkred", command=lambda: supprimer(id)).place(x=450, y=490)



#Misupprimer profil a partir ana recherche
def supprimer_profil_rech(id, exp):
    reinitialiser_frame()
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame_header = ctk.CTkFrame(frame)
    frame_header.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
    bouton = ctk.CTkButton(frame_header, text="⇦", font=("Arial", 30), command=lambda: liste_pour_supprimer(exp))
    bouton.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    conn = connexion_db()
    curseur = conn.cursor()

    def supprimer(id_olona):
        motif = entry_motif.get("1.0", "end-1c")
        conn = connexion_db()
        if conn:
            curseur = conn.cursor()
            sql = f"UPDATE employes SET motif='{motif}', statut='exclu' WHERE id={id_olona}"
            try:
                curseur.execute(sql)
                conn.commit()
                messagebox.showinfo("Succès", "Employé renvoyé(e)!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur: {err}")
            finally:
                curseur.close()
                conn.close()
        afficher_employes_options("statut","exclu")



    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()

    img_data = io.BytesIO(employe[6])
    img = Image.open(img_data)
    img.thumbnail((400, 400))
    photo = ImageTk.PhotoImage(img)
    photo_label = ctk.CTkLabel(frame, image=photo)
    photo_label.image = photo
    photo_label.configure(text="", bg_color="yellow")
    photo_label.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    ctk.CTkLabel(frame, text=f"{employe[1]}", font=("Courier", 25)).place(x=450, y=130)
    ctk.CTkLabel(frame, text="Motif du renvoi:", font=("Verdana", 8)).place(x=450, y=160)
    entry_motif = ctk.CTkTextbox(frame, width=310, height=150)
    entry_motif.place(x=450, y=190)
    ctk.CTkLabel(frame, text=f"Département: \t{employe[2]}", font=("Arial Black", 15)).place(x=450, y=350)
    ctk.CTkLabel(frame, text=f"Adresse: \t\t{employe[3]}", font=("Arial Black", 15)).place(x=450, y=380)
    ctk.CTkLabel(frame, text=f"Statut: \t\t{employe[4]}", font=("Arial Black", 15)).place(x=450, y=410)
    ctk.CTkLabel(frame, text=f"Date d'embauche: \t{employe[5]}", font=("Arial Black", 15)).place(x=450, y=440)
    ctk.CTkButton(frame, text="Supprimer", fg_color="darkred", command=lambda: supprimer(id)).place(x=450, y=490)



#Mimodifier profil
def modifier_profil(id):
    reinitialiser_frame()
    frame.pack(fill="both", expand="true")
    for i in range(4):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(6):
        frame.grid_columnconfigure(j, weight=1)

    conn = connexion_db()
    curseur = conn.cursor()
    curseur.execute(f"SELECT id, nom, departement, adresse, statut, date_embauche, photo, date_naissance FROM employes WHERE id='{id}'")
    employe = curseur.fetchone()

    def modifier_employe(id):
        nom = entry_nom.get()
        date_naissance = entry_date_naissance.get()
        adresse = entry_adresse.get()
        date_embauche = entry_date_embauche.get()
        departement = depart.get()

        photo = None
        if photo_path:
            with open(photo_path, 'rb') as file:
                photo = file.read()
        else:
            photo = employe[6]

        conn = connexion_db()
        if conn:
            curseur = conn.cursor()
            sql = "UPDATE employes SET nom=%s, date_naissance=%s, adresse=%s, date_embauche=%s, departement=%s, photo=%s WHERE id=%s"
            values = (nom, date_naissance, adresse, date_embauche, departement, photo, id)
            try:
                curseur.execute(sql, values)
                conn.commit()
                messagebox.showinfo("Succès", "Employé modifié avec succès!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur: {err}")
            finally:
                curseur.close()
                conn.close()
        afficher_profil_simple(id)

    def select_photo():
        nonlocal photo_path
        photo_path = filedialog.askopenfilename()
        if photo_path:
            img = Image.open(photo_path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            label_photo.configure(image=img, text="")
            bouton_photo.configure(text="Changer la photo")
            label_photo.image = img


    photo_path = None

    ctk.CTkLabel(frame, text="Nom").grid(row=0, column=0, padx=5, pady=5)
    entry_nom = ctk.CTkEntry(frame, width=200)
    entry_nom.insert(0, employe[1])
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Date de naissance\n(AAAA-MM-JJ)").grid(row=1, column=0, padx=5, pady=5)
    entry_date_naissance = ctk.CTkEntry(frame, width=100)
    entry_date_naissance.insert(0, employe[7])
    entry_date_naissance.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Adresse").grid(row=2, column=0, padx=5, pady=5)
    entry_adresse = ctk.CTkEntry(frame, width=200)
    entry_adresse.insert(0, employe[3])
    entry_adresse.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Date d'embauche\n(AAAA-MM-JJ)").grid(row=0, column=5, padx=5, pady=5)
    entry_date_embauche = ctk.CTkEntry(frame, width=100)
    entry_date_embauche.insert(0, employe[5])
    entry_date_embauche.grid(row=0, column=6, padx=5, pady=5)

    depart = ctk.StringVar(value=employe[2])
    ctk.CTkLabel(frame, text="Département").grid(row=1, column=5, padx=5, pady=5)
    entry_departement = ctk.CTkOptionMenu(frame, variable=depart,
                                          values=["RH", "Marketing", "Informatique", "Securité", "Travaux", "Autre"],
                                          width=200, dropdown_fg_color="darkred", dropdown_hover_color="black",
                                          button_color="darkred", button_hover_color="black").grid(row=1, column=6,
                                                                                                   padx=5, pady=5)

    img_data_x = io.BytesIO(employe[6])
    img_x = Image.open(img_data_x)
    img_x.thumbnail((100, 100))
    photo_pers = ImageTk.PhotoImage(img_x)
    label_photo = ctk.CTkLabel(frame, font=("Verdana", 10), text="", image=photo_pers, fg_color="grey40", text_color="black",
                               corner_radius=3, width=100, height=100)
    label_photo.grid(row=2, column=5, padx=5, pady=5)
    bouton_photo = ctk.CTkButton(frame, text="Choisir une photo", command=select_photo)
    bouton_photo.grid(row=2, column=6, padx=5, pady=5)

    ctk.CTkButton(frame, text="Modifier", command= lambda: modifier_employe(id), fg_color="cyan4", hover_color="darkolivegreen").grid(
        row=3, column=3, padx=5, pady=5)



# Reinitialisation frame
def reinitialiser_frame():
    for widget in frame.winfo_children():
        widget.destroy()



# Fenetre a propos de bassl22
def a_propos():
    reinitialiser_frame()
    frame.pack(fill="both", expand="true")
    ctk.CTkLabel(frame, text="Ce logiciel \"bassl22\" a été conçu par Lanja Fitahina RAHERISON à titre de projet python du 2ème année d'étude en Génie Logiciel.\n Copyright LanjaFii2024").pack(pady=10)
    imgLanja_chemin = "/home/lanja/PycharmProjects/LogicielDeGestion/lanjafii.jpg"
    image_lanja = Image.open(imgLanja_chemin)
    image_lanja.thumbnail((300,300))
    img_lanja = ImageTk.PhotoImage(image_lanja)
    ctk.CTkLabel(master=frame, image=img_lanja, text="").pack()
    ctk.CTkLabel(frame,text="Remerciements: \n Jesosy Kristy \n Mr Andrianaivo Herifidy \n st-BASS-22 (mon ordi) \n\n\n\n\n Credits by LanjaFii \n\n☏: +261389195456\n✉: base3fita@gmail.com\n\nCopyright LanjaFii2024").pack()



# Configuration initiale
if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # Utilise le thème système par défaut
    ctk.set_default_color_theme("blue")  # Thème de couleur par défaut
    montre = "departmt"
    if connexion_db():
        #menu_principal()
        login()


