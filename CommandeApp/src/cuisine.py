from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
import xlsxwriter


window=Tk()
window.title("Cuisine")
window.config(background="white")
style=Style()
style.configure("Custom.TButton",bg="white",font="Raleway 12 underline",padding=[5,5,5,5])
style.configure("Label",background="white",font="Raleway 12")
style.configure("Custom.TLabel",background="white",font="Raleway 20")



def refresh_page():
    for child in window.winfo_children():
        child.destroy() 
    
#Ajoute un produit dans la table "Produit"
def ajout_produit(code,nom,unite):
    refresh_page()
    affiche_form_produit(window)
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    if(nom=="" or unite==""):
        Label(window,text="Veuillez rentrer tous les champs",style="Label").grid(row="4",column="1",pady=7,padx=3)
    else:
        nouveau_produit=(code,nom,unite,0)
        cursor.execute("INSERT INTO Produit VALUES(?,?,?,?)",nouveau_produit)
        connection.commit()
        Label(window,text="Le produit a bien été enregisté",style="Label").grid(row="4",column="1",pady=7,padx=3)
    connection.close()
    
    
    
    
#Affiche le formulaire pour ajouté les produits
def affiche_form_produit(window):
    refresh_page()  
    CodeProduit=IntVar()
    NomProduit=StringVar()
    Unite=StringVar()
    Label(window,style="Custom.TLabel",text="Ajout produit:").grid(row="0",column="0")
    label_code_produit=Label(window,text="Code:",style="Label")
    label_libelle=Label(window,text="Nom:",style="Label")
    label_unite=Label(window,text="Unité de mesure:",style="Label")
    
    champ_code_produit=Entry(window,textvariable=CodeProduit)
    champ_libelle=Entry(window,textvariable=NomProduit)
    champ_unite=Entry(window,textvariable=Unite)
    label_code_produit.grid(row="1",column="0",pady=3)
    champ_code_produit.grid(row="1",column="1",pady=3)
    label_libelle.grid(row="2",column="0",pady=3)
    champ_libelle.grid(row="2",column="1",pady=3)
    label_unite.grid(row="3",column="0",pady=3)
    champ_unite.grid(row="3",column="1",pady=3)
    Button(window,text="Ajouter le produit",style="Custom.TButton",command=lambda:ajout_produit(CodeProduit.get(),NomProduit.get(),Unite.get())).grid(row="4",column="0",pady=7)
    Button(window,text="Faire une nouvelle commande",style="Custom.TButton",command=lambda:affiche_form_commande(window)).grid(row="5",column="0")
    Button(window,text="Voir les produits",style="Custom.TButton",command=lambda:voir_produit(window)).grid(row="0",column="2")
    
    
    
    
    
    
    
def affiche_conversion_fichier(window):
    refresh_page()
    affiche_form_commande(window)
    nomFichier=StringVar()
    Label(window,text="Entrer le nom du fichier",style="Label").grid(row="8",column="0",pady=5,padx=3)
    Entry(window,textvariable=nomFichier).grid(row="8",column="1",pady=5,padx=3)
    Button(window,text="Créer le fichier de commande",style="Custom.TButton",command=lambda:creation_fichier(nomFichier.get(),window)).grid(row="8",column="3",pady=5,padx=10)
    
    
    
    
#Affiche le formulaire pour faire des commandes  
def affiche_form_commande(window):
    refresh_page()
    CodeProduit=IntVar()
    Quantite=IntVar()
    Label(window,text="Ajout commande:",style="Custom.TLabel").grid(row="0",column="0")
    label_code_produit=Label(window,text="Code:",style="Label")
    label_quantite=Label(window,text="Quantité:",style="Label")
    champ_code_produit=Entry(window,textvariable=CodeProduit)
    champ_quantite=Entry(window,textvariable=Quantite)
    label_code_produit.grid(row="1",column="0",pady=3)
    champ_code_produit.grid(row="1",column="1",pady=3)
    label_quantite.grid(row="2",column="0",pady=3)
    champ_quantite.grid(row="2",column="1",pady=3)
    Button(window,text="Modifier la commande",style="Custom.TButton",command=lambda:ajout_commande(CodeProduit.get(),Quantite.get())).grid(row="4",column="0",pady=7)
    Button(window,text="Ajouter un nouveau produit",style="Custom.TButton",command=lambda:affiche_form_produit(window)).grid(row="5",column="0")
    Button(window,text="Terminer la commande",style="Custom.TButton",command=lambda:affiche_conversion_fichier(window)).grid(row="7",column="0",pady=5)
    Button(window,text="Voir les commandes",style="Custom.TButton",command=lambda:voir_commande(window)).grid(row="0",column="3")
    
    
    
    
#Fonction qui ajoute une nouvelle commande dans la table "Commande"   
def ajout_commande(code,quantite):
    refresh_page()
    affiche_form_commande(window)
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    if(str(quantite)==""):
        Label(window,text="Veuillez rentrer tous les champs",style="Label").grid(row="4",column="1",pady=10,padx=10)
    else:
        update=(quantite,code)
        cursor.execute("UPDATE Produit SET Quantité=? WHERE CodeProduit=?",update)
        connection.commit()
        Label(window,text="La commande a bien été enregisté",style="Label").grid(row="4",column="1",pady=10,padx=10)
    connection.close()
    
    
    
    
    
    
#Ajoute les produits dans un tableur avec leur poids dans un tableur
def creation_fichier(nomFichier,window):
    
    fileName="./"+nomFichier+".xlsx"
    workbook= xlsxwriter.Workbook(nomFichier+".xlsx")
    worksheet = workbook.add_worksheet("sheet1")
    worksheet.write(0,0,"Code Produit")
    worksheet.write(0,1,"Libellé")
    worksheet.write(0,2,"Quantité")
    worksheet.write(0,3,"Unité")

    
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    cursor.execute("SELECT CodeProduit,Libellé,Quantité,Unité FROM Produit")
    commandes=cursor.fetchall()
    i=1
    for commande in commandes:
        
        worksheet.write(i,0,commande[0])
        worksheet.write(i,1,commande[1])
        worksheet.write(i,2,commande[2])
        worksheet.write(i,3,commande[3])
        i+=1
    workbook.close()
    Label(window,text="Le fichier a bien été créé",style="Label").grid(row="9",column="1",pady=3)
    cursor.execute("SELECT CodeProduit FROM Produit")
    for produit in cursor.fetchall():
        reset=(0,produit[0])
        cursor.execute("UPDATE Produit SET Quantité=? WHERE CodeProduit=?",reset)
        connection.commit()

    connection.close()
    
    
    
    
    
#Affiche la liste des produits    
def voir_produit(window):
    refresh_page()
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    create_table(connection, cursor)
    cursor.execute("SELECT CodeProduit,Libellé,Unité FROM Produit")
    Button(window,text="Ajout d'un produit ?",style="Custom.TButton",command=lambda:affiche_form_produit(window)).grid(row="0",column="0")
    Button(window,text="Ajout d'une commande ?",style="Custom.TButton",command=lambda:affiche_form_commande(window)).grid(row="1",column="0")
    Label(window,text="Liste des produits:",style="Custom.TLabel").grid(row="2",column="0")
    i=3
    game_scroll = Scrollbar(window,orient='vertical')
    my_game = Treeview(window,yscrollcommand=game_scroll.set)
    game_scroll.grid(column=1, row=3, sticky=(N, S))

    my_game.grid(row=3,pady=25)
    game_scroll.config(command=my_game.yview)

    #define our column
        
    my_game['columns'] = ('CodeProduit', 'Libellé', 'Unité')

    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("CodeProduit",anchor=CENTER, width=500)
    my_game.column("Libellé",anchor=CENTER, width=500)
    my_game.column("Unité",anchor=CENTER,width=500)
    #Create Headings 
    my_game.heading("CodeProduit",text="CodeProduit",anchor=CENTER)
    my_game.heading("Libellé",text="Libellé",anchor=CENTER)
    my_game.heading("Unité",text="Unité",anchor=CENTER)
    i=0
    for produit in cursor.fetchall():
        my_game.insert(parent='',index='end',iid=i,text='',
        values=(produit[0],produit[1],produit[2]))
        i+=1
    my_game.grid(row=3,column=0)
    
       
        
        
        
#Affiche la liste des commandes        
def voir_commande(window):
    refresh_page()
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    create_table(connection, cursor)
    cursor.execute("SELECT CodeProduit,Libellé,Quantité,Unité FROM Produit")
    Button(window,text="Ajout d'un produit ?",style="Custom.TButton",command=lambda:affiche_form_produit(window)).grid(row="0",column="0")
    Button(window,text="Ajout d'une commande ?",style="Custom.TButton",command=lambda:affiche_form_commande(window)).grid(row="1",column="0")
    Label(window,text="Liste des produits:",style="Custom.TLabel").grid(row="2",column="0")
    i=3
    game_scroll = Scrollbar(window,orient='vertical')
    my_game = Treeview(window,yscrollcommand=game_scroll.set)
    game_scroll.grid(column=1, row=3, sticky=(N, S))

    my_game.grid(row=3,pady=25)
    game_scroll.config(command=my_game.yview)

    #define our column
        
    my_game['columns'] = ('CodeProduit', 'Libellé','Quantité' ,'Unité')

    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("CodeProduit",anchor=CENTER, width=400)
    my_game.column("Libellé",anchor=CENTER, width=400)
    my_game.column("Quantité",anchor=CENTER, width=400)
    my_game.column("Unité",anchor=CENTER,width=400)
    #Create Headings 
    my_game.heading("CodeProduit",text="CodeProduit",anchor=CENTER)
    my_game.heading("Libellé",text="Libellé",anchor=CENTER)
    my_game.heading("Quantité",text="Quantité",anchor=CENTER)
    my_game.heading("Unité",text="Unité",anchor=CENTER)
    i=0
    for produit in cursor.fetchall():
        my_game.insert(parent='',index='end',iid=i,text='',
        values=(produit[0],produit[1],produit[2],produit[3]))
        i+=1
    my_game.grid(row=3,column=0)
def create_table_init():
    connection = connect("data.db")
    with connection:
        cursor = connection.cursor()
    sql='CREATE TABLE IF NOT EXISTS "Produit" ("CodeProduit" INTEGER NOT NULL,"Libellé"	TEXT NOT NULL,"Unité" TEXT NOT NULL,"Quantité"	INTEGER,PRIMARY KEY("CodeProduit"))'
    cursor.execute(sql)
    connection.commit()
    
def create_table(connection,cursor):
    sql='CREATE TABLE IF NOT EXISTS "Produit" ("CodeProduit" INTEGER NOT NULL,"Libellé"	TEXT NOT NULL,"Unité" TEXT NOT NULL,"Quantité"	INTEGER,PRIMARY KEY("CodeProduit"))'
    cursor.execute(sql)
    connection.commit()
    
affiche_form_produit(window)
create_table_init()
window.mainloop()