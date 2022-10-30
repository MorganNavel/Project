import sqlite3
from tkinter import *
from tkinter.ttk import *
from random import *




def create_table():
    db_path="base.db"
    connection_cursor=connection_data_base(db_path)
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    cursor.execute('CREATE TABLE IF NOT EXISTS "Translation" ("Korean" TEXT NOT NULL,"English" TEXT NOT NULL,"ID" INTEGER,PRIMARY KEY("ID"))')
    connection.commit()
    connection.close()
    
def connection_data_base(db_path):
    connection=sqlite3.connect(db_path)
    with connection:
        cursor=connection.cursor()
    return [connection,cursor]


def send_error_too_much_field_fill():
    show_translation_form(window)
    Label(window,text="You have to write in only one field",style="Label").grid(row=4,column=1)
    
def translation_english_to_korean(english):
    connection_cursor=connection_data_base("base.db")
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    show_translation_form(window)
    word=(english,)
    cursor.execute("SELECT  Korean FROM Translation WHERE English = ?",word)
    result+="Korean: "+cursor.fetchone()[0]
    Label(window,text=result,style="Label").grid(padx=5,row=5,column=1)
    connection.close()
    
    
def translation_korean_to_english(korean):
    connection_cursor=connection_data_base("base.db")
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    show_translation_form(window)
    word=(korean,)
    cursor.execute("SELECT  English FROM Translation WHERE Korean = ?",word) 
    result="English: "+cursor.fetchone()[0]+"\n"
    Label(window,text=result,style="Label").grid(padx=5,row=5,column=1)
    connection.close()
    
def send_error_all_field_empty():
    show_translation_form(window)
    Label(window,text="You have to write in atleast of the fields",style="Label").grid(row=4,column=1)

    

def translate_word(english,korean):  
    if(english!="" and korean==""):
        translation_english_to_korean(english)
    elif(korean!="" and english==""):
        translation_korean_to_english(korean)  
    elif(english!="" and korean!=""):
        send_error_too_much_field_fill()           
    elif(english=="" and korean==""):
        send_error_all_field_empty()
        
        
        
def send_notification_register_sucessfully():
    show_register_form(window)
    Label(window,text="The word has been sent to the word bank successfully.",style="Label").grid(row=4,column=1)
    
    
    

def register_word(english,korean):
    connection_cursor=connection_data_base("base.db")
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    if(korean!="" and english!=""):
        new_word=(korean,english,cursor.lastrowid)
        cursor.execute("INSERT INTO Translation VALUES(?,?,?)",new_word)
        connection.commit()
        send_notification_register_sucessfully()
    else:
        send_error_all_field_empty()
    connection.close()


def saved_words(window):
    refresh_page(window)
    Label(window,text="List of words: ",style="Custom.TLabel").grid(row=2)
    connection_cursor=connection_data_base("base.db")
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    cursor.execute("SELECT English,Korean FROM Translation")
    Button(window,style="Custom.TButton",text="Translate a word",command=lambda:show_translation_form(window)).grid(row=0,column=0)
    Button(window,style="Custom.TButton",text="Register a word",command=lambda:show_register_form(window)).grid(row=1,column=0,pady=5)
    game_scroll = Scrollbar(window,orient='vertical')
    my_game = Treeview(window,yscrollcommand=game_scroll.set)
    game_scroll.grid(column=1, row=3, sticky=(N, S))

    my_game.grid(row=3,pady=25)
    game_scroll.config(command=my_game.yview)

    #define our column
        
    my_game['columns'] = ('English','Korean')

    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("English",anchor=CENTER, width=300)
    my_game.column("Korean",anchor=CENTER,width=300)
    #Create Headings 
    my_game.heading("English",text="English",anchor=CENTER)
    my_game.heading("Korean",text="Korean",anchor=CENTER)
    i=0
    for words in cursor.fetchall():
        my_game.insert(parent='',index='end',iid=i,text='',
        values=(words[0],words[1]))
        i+=1
    my_game.grid(row=3,column=0)
    
def create_form(window):
    Label(window, text="Translation App",style="Custom.TLabel").grid(row=0,column=0)
    english=show_english_part_form("Enter an English word")
    korean=show_korean_part_form("Enter a Korean word")
    return [english,korean]
    
     
def show_english_part_form(text):
    english_word=StringVar()
    label_english = Label(window, text=text,style="Label").grid(row=1,column=0)
    english_field = Entry(window,text="English", textvariable = english_word).grid(row=1,column=1)
    return english_word

    
    
def show_korean_part_form(text):
    korean_word=StringVar()
    label_korean = Label(window, text=text,style="Label").grid(row=2,column=0)
    korean_field = Entry(window,text="Korean",textvariable=korean_word).grid(row=2,column=1)
    return korean_word
    
def show_practice(back):
    refresh_page(window)
    Label(window,text="Practice: ",style="Custom.TLabel").grid(row=0)
    if(back=="T"):
        Button(window,text="Go Back",command=lambda:show_translation_form(window),style="Custom.TButton").grid(row=0,column=1)
    elif(back=="R"):
        Button(window,text="Go Back",style="Custom.TButton",command=lambda:show_register_form(window)).grid(row=0,column=1)
    Button(window,style="Custom.TButton",text="English",command=lambda:show_practice_form("English")).grid(row=1)
    Button(window,style="Custom.TButton",text="Korean",command=lambda:show_practice_form("Korean")).grid(row=3)


def show_register_form(window):
    refresh_page(window)
    entry_values=create_form(window)
    button_submit = Button(window,style="Custom.TButton",text="Register",command=lambda:register_word(entry_values[0].get(),entry_values[1].get())).grid(row=4,column=0,pady=5)
    button_change=Button(window,style="Custom.TButton",text="Translate a word",command=lambda:show_translation_form(window)).grid(row=5,column=0)
    button_view_words=Button(window,style="Custom.TButton",text="View All Saved Words",command=lambda:saved_words(window)).grid(row=6,column=0,pady=5)
    Button(window,style="Custom.TButton",text="Practice",command=lambda:show_practice("R")).grid(row=7)
    
    
    
def refresh_page(window):
    for child in window.winfo_children():
        child.destroy()

def show_translation_form(window):
    refresh_page(window)
    entry_values=create_form(window) 
    button_submit = Button(window,style="Custom.TButton",text="Translate",command=lambda:translate_word(entry_values[0].get(),entry_values[1].get())).grid(row=4,column=0,pady=5)
    button_change=Button(window,style="Custom.TButton",text="Register a new word",command=lambda:show_register_form(window)).grid(row=5,column=0)
    button_view_words=Button(window,style="Custom.TButton",text="View All Saved Words",command=lambda:saved_words(window)).grid(row=6,column=0,pady=5)
    Button(window,style="Custom.TButton",text="Practice",command=lambda:show_practice("T")).grid(row=7)
    
def show_word_korean(words,cursor,connection,nbTry,nbEasy):
    refresh_page(window)
    cursor.execute("SELECT English FROM Translation WHERE ID=?",[str(words[0])])
    j=0
    for word in cursor.fetchone():
        if j==0:
            Label(window,text=word,style="Label").grid(row=0,column=j,padx=5)
            Label(window,style="Label").grid(row=0,column=j+1,padx=5)
        else:
            Label(window,text=word,style="Label").grid(row=0,column=j+2,padx=5)
        j+=1
def show_word_english(words,cursor,connection,nbTry,nbEasy):
    refresh_page(window)
    cursor.execute("SELECT Korean FROM Translation WHERE ID=?",[str(words[0])])
    j=0
    for word in cursor.fetchone():
        if j==0:
            Label(window,text=word,style="Label").grid(row=0,column=j,padx=5)
            Label(window,style="Label").grid(row=0,column=j+1,padx=5)
        else:
            Label(window,text=word,style="Label").grid(row=0,column=j+2,padx=5)
        j+=1


    
def addFirst(words,word,cursor,connection,language,nbTry,nbEasy):
    nbTry+=1
    refresh_page(window)
    if(language=="Korean"):
        practice_korean(window, cursor, connection, words, nbTry, nbEasy)
    elif(language=="English"):
        practice_english(window, cursor, connection, words, nbTry, nbEasy)
        
        
        

def addLast(words,word,cursor,connection,language,nbTry,nbEasy):
    nbTry+=1
    nbEasy+=1
    words.pop(0)
    refresh_page(window)
    if(language=="Korean"):
        practice_korean(window, cursor, connection, words, nbTry, nbEasy)
    elif(language=="English"):
        practice_english(window, cursor, connection, words, nbTry, nbEasy)
        

def show_hard_easy_response(words,cursor,connection,language,nbTry,nbEasy):
    if language=="Korean":
        show_word_korean(words, cursor, connection,nbTry,nbEasy)
        Button(window,style="Custom.TButton",text="EASY",command=lambda:addLast(words, words[0],cursor,connection,"Korean",nbTry,nbEasy)).grid(row=2,column=0)
        Button(window,style="Custom.TButton",text="HARD",command=lambda:addFirst(words, words[0],cursor,connection,"Korean",nbTry,nbEasy)).grid(row=2,column=3)
    elif(language=="English"):
        show_word_english(words, cursor, connection,nbTry,nbEasy)
        Button(window,style="Custom.TButton",text="EASY",command=lambda:addLast(words, words[0],cursor,connection,"English",nbTry,nbEasy)).grid(row=2,column=0)
        Button(window,style="Custom.TButton",text="HARD",command=lambda:addFirst(words, words[0],cursor,connection,"English",nbTry,nbEasy)).grid(row=2,column=3) 


    
def init_practice_korean(window):
    db_path="base.db"
    connection_cursor=connection_data_base(db_path)
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    cursor.execute("SELECT Count(*) FROM Translation")
    nb_words=cursor.fetchone()[0]
    if(nb_words==0):
        refresh_page(window)
        Label(window,style="Label",text="There is no words in the data base, you have to register atleast one to practice").grid(row=11,column=0)
        Button(window,style="Custom.TButton",text="Go Back",command=lambda:show_translation_form(window)).grid(row=12,column=0)
    else:    
        words=[]
        for i in range(nb_words):
            randomIndex=randint(1, nb_words)
            while(randomIndex in words):
                randomIndex=randint(1, nb_words)
            words.append(randomIndex)
        refresh_page(window)
        cursor.execute("SELECT Korean FROM Translation WHERE ID=?",[str(words[0])])
        for word in cursor.fetchone():
            Label(window,text=word,style="Label").grid(row=1)
        nbTry=0
        nbEasy=0
        Button(window,style="Custom.TButton",text="NEXT",command=lambda:show_hard_easy_response(words,cursor,connection,"Korean",nbTry,nbEasy)).grid(row=2)

    
def practice_korean(window,cursor,connection,words,nbTry,nbEasy):   
    refresh_page(window)
    if(words==[]):
        Label(window,style="Label",text="It's the end of the practice, you got "+str(nbEasy)+" words right on the first try, your understanding of those words are up to "+str(((nbEasy/nbTry))*100)+"%").grid(row=11,column=0)
        Button(window,style="Custom.TButton",text="Go Back",command=lambda:show_translation_form(window)).grid(row=12,column=0)
    else:
        cursor.execute("SELECT Korean FROM Translation WHERE ID=?",[str(words[0])])
        for word in cursor.fetchone():
            Label(window,text=word,style="Label").grid(row=1)
        Button(window,style="Custom.TButton",text="NEXT",command=lambda:show_hard_easy_response(words,cursor,connection,"Korean",nbTry,nbEasy)).grid(row=2)

    
    
def init_practice_english(window):
    db_path="base.db"
    connection_cursor=connection_data_base(db_path)
    connection=connection_cursor[0]
    cursor=connection_cursor[1]
    cursor.execute("SELECT Count(*) FROM Translation")
    nb_words=cursor.fetchone()[0]
    if(nb_words==0):
        refresh_page(window)
        Label(window,style="Label",text="There is no words in the data base, you have to register atleast one to practice").grid(row=11,column=0)
        Button(window,style="Custom.TButton",text="Go Back",command=lambda:show_translation_form(window)).grid(row=12,column=0)
    else: 
        words=[]
        for i in range(nb_words):
            randomIndex=randint(1, nb_words)
            while(randomIndex in words):
                randomIndex=randint(1, nb_words)
            words.append(randomIndex)
        refresh_page(window)
        cursor.execute("SELECT English FROM Translation WHERE ID=?",[str(words[0])])
        for word in cursor.fetchone():
            Label(window,text=word,style="Label").grid(row=1)
        nbTry=0
        nbEasy=0
        Button(window,style="Custom.TButton",text="NEXT",command=lambda:show_hard_easy_response(words,cursor,connection,"English",nbTry,nbEasy)).grid(row=2)

    
def practice_english(window,cursor,connection,words,nbTry,nbEasy):
    refresh_page(window)
    if(words==[]):
        Label(window,style="Label",text="It's the end of the practice, you got "+str(nbEasy)+" words right on the first try, your understanding of those words are up to "+str(((nbEasy/nbTry))*100)+"%").grid(row=11,column=0)
        Button(window,style="Custom.TButton",text="Go Back",command=lambda:show_translation_form(window)).grid(row=12,column=0)
    else:
        cursor.execute("SELECT English FROM Translation WHERE ID=?",[str(words[0])])
        for word in cursor.fetchone():
            Label(window,text=word,style="Label").grid(row=1)
        Button(window,style="Custom.TButton",text="NEXT",command=lambda:show_hard_easy_response(words,cursor,connection,"English",nbTry,nbEasy)).grid(row=2)

    
def show_practice_form(language):
    if(language=="Korean"):
        init_practice_korean(window)
    elif(language=="English"):
        init_practice_english(window)
    
    
        
window = Tk()
window.title("WordBank")
style=Style()
window.configure(background="white")
style.configure("Label",background="white",font="Arial 12",padding=[5,5,5,5])
style.configure("Custom.TLabel",background="white",font="Arial 20",padding=[5,5,5,5])
style.configure("Custom.TButton",background="white",font="Arial 12 underline",padding=[5,5,5,5])
create_table()
show_translation_form(window)
        
window.mainloop()

