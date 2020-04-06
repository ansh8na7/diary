from tkinter import *
import sqlite3
import tkinter.messagebox
import secrets 
import string
from datetime import date
from datetime import datetime

conn = sqlite3.connect('database.db')   

c = conn.cursor()

ids = []
email = []
txt = []




class application:
    def __init__(self, master):
        self.master = master
        self.left = Frame(master, width=1280, height=720, bg='lightgreen')
        self.left.pack(side=LEFT)
        
        self.heading = Label(self.left, text="DIARY - LOGIN PAGE", font=('arial 40 bold'), fg='black', bg='lightgreen')
        self.heading.place(x=300, y=50)

        self.email = Label(self.left, text="Name :", font=('arial 28 bold'), fg='black', bg='lightgreen')
        self.email.place(x=400, y=300)

        self.pwd = Label(self.left, text="Password :", font=('arial 28 bold'), fg='black', bg='lightgreen')
        self.pwd.place(x=370, y=400)
	
        self.email_ent = Entry(self.left, width=30)
        self.email_ent.place(x=600, y=310)

        self.pwd_ent = Entry(self.left,show="*", width=30)
        self.pwd_ent.place(x=600, y=410)

        self.val1 = self.email_ent.get()
        self.val2 = self.pwd_ent.get()

        self.enter = Button(self.left, text="REGISTER", width=20, height=2, bg='steelblue', command=self.enter)
        self.enter.place(x=400, y=550)

        self.login = Button(self.left, text="LOGIN", width=20, height=2, bg='blue', command=self.reg_user)
        self.login.place(x=600, y=550)


    def reg_user(self):
        self.val1 = self.email_ent.get()
        self.val2 = self.pwd_ent.get()
        self.f=0
        sql5 = "SELECT text FROM logins "
        self.result = c.execute(sql5)
        
        for self.row in self.result:
            self.id = self.row[0]
            txt.append(self.id)            
        length = len(txt)
        for i in range(0,length-1,1):
            if txt[i] == None:
                txt[i] = txt[i+1]
        self.search = 0
        
        sql2 = "SELECT email,password,id FROM logins "
        self.result = c.execute(sql2)
        for self.row in self.result:
            self.val1 = self.email_ent.get()
            self.val2 = self.pwd_ent.get()
            self.e = self.row[0]
            self.p = self.row[1]
            self.id = self.row[2]
            if self.val1 == self.e and self.val2 ==  self.p :
                self.f=1
                self.search = self.row[2]+1
                #print(self.row[2]+1)
                break
        
        
        self.final_text = ''
        sql6 = "SELECT id,text FROM logins "
        self.result = c.execute(sql6)
        for self.row in self.result:
            if self.row[0] == self.search:
                self.final_text = self.row[1]
                #print(self.row[1])
                break

        
                
        
        if self.f == 0:
            tkinter.messagebox.showinfo("Warning", "Please enter correct username and password ")
        else :
            self.destroy()
            self.login.destroy()
            self.diary()
            self.enter.destroy()
            self.text = self.box.get("1.0",END)   
            f = open(self.final_text+".txt","r")
            total_text = f.read()
            self.box.insert(END, str(total_text))
            f.close()
            self.enter = Button(self.left, text="Append", width=20, height=2, bg='steelblue', command=self.update)
            self.enter.place(x=400, y=650)            
        
        
    def update(self):
        self.text = self.box.get("1.0",END)  
        f = open(self.final_text+".txt","w")
        f.write(self.text)
        tkinter.messagebox.showinfo("","Successfully saved your memories." )
        self.enter.destroy()
        print ('=================SAVED=================')
        
        
    
    
    def enter(self):
        self.val1 = self.email_ent.get()
        self.val2 = self.pwd_ent.get()
        if self.val1 == '':
            tkinter.messagebox.showinfo("Warning", "Please fill up User name")
        elif  self.val2 == '':
            tkinter.messagebox.showinfo("Warning", "Please fill up Password")
        elif self.val1 != '' and self.val2 != '':
            sql = "INSERT INTO 'logins' (email, password) VALUES(?, ?)"
            self.val1 = self.email_ent.get()	
            self.val2 = self.pwd_ent.get()
            c.execute(sql, (self.val1, self.val2))
            conn.commit()
            tkinter.messagebox.showinfo("","Successfully logged in." )
            self.destroy()
            self.diary()

    def destroy(self):
        self.email.destroy()
        self.pwd.destroy()
        self.email_ent.destroy()		
        self.pwd_ent.destroy()
        self.enter.destroy()

    def diary(self):
        self.heading = Label(self.left, text="DIARY - write something ", font=('Bookman 40 bold'), fg='black', bg='lightgreen')
        self.heading.place(x=300, y=50)
        self.box = Text(self.left, width=40, height=10, font=('arial 28 bold'),bg='green')
        self.box.place(x=200, y=200)
        self.enter = Button(self.left, text="SAVE", width=20, height=2, bg='steelblue', command=self.save)
        self.enter.place(x=400, y=650)

    def save(self):
        #now = datetime.now()
        #today = date.today()
        #d = today.strftime("%b-%d-%Y")
        self.text = self.box.get("1.0",END)            #to take input from the text box
        N=7
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
        print (res)
        sql = "INSERT INTO 'logins' (text) VALUES(?)"
        c.execute(sql,(res,))
        conn.commit()
        
        sql2 = "SELECT id FROM logins "
        self.result = c.execute(sql2)
        for self.row in self.result:
            self.id = self.row[0]
            ids.append(self.id)
            
        sql2 = "SELECT text FROM logins "
        self.result = c.execute(sql2)
        for self.row in self.result:
            self.id = self.row[0]
            txt.append(self.id)            
        length = len(txt)
        
        for i in range(0,length-1,1):
            if txt[i] == None:
                txt[i] = txt[i+1]

        f = open(res+".txt","a")
        f.write(self.text)
        f.close()
        tkinter.messagebox.showinfo("","Successfully saved." )
        print ('=================SAVED=================')
        
        
        root.quit()
        
        


root = Tk()
b = application(root)
root.geometry("1200x720+0+0")
root.resizable(False, False)
root.mainloop()


