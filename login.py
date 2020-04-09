from tkinter import *
import sqlite3
import tkinter.messagebox
import secrets
import string
from datetime import date
from datetime import datetime
import time

conn = sqlite3.connect('database.db')

c = conn.cursor()

ids = []
email = []
txt = []

now = time.strftime("%I:%M:%S")
today = date.today()
d = today.strftime("%b-%d-%Y")

background = 'bisque2'

class application:
    def __init__(self, master):
        self.master = master
        self.left = Frame(master, width=1280, height=720, bg=background)
        self.left.pack(side=LEFT)

        self.heading = Label(self.left, text="DIARY - LOGIN PAGE", font=('arial 40 bold'), fg='red', bg=background)
        self.heading.place(x=400, y=50)

        self.cloak = Label(self.left, text=str(d)+"   "+str(now), font=('arial 20 bold'), fg='blue2', bg=background)
        self.cloak.place(x=470, y=200)

        self.email = Label(self.left, text="Username :", font=('arial 28 bold'), fg='orange', bg=background)
        self.email.place(x=370, y=300)

        self.pwd = Label(self.left, text="Password :", font=('arial 28 bold'), fg='orange', bg=background)
        self.pwd.place(x=370, y=400)

        self.email_ent = Entry(self.left, width=30)
        self.email_ent.place(x=600, y=310)

        self.pwd_ent = Entry(self.left,show="*", width=30)
        self.pwd_ent.place(x=600, y=410)

        self.val1 = self.email_ent.get()
        self.val2 = self.pwd_ent.get()

        self.enter = Button(self.left, text="REGISTER", width=20, height=2, bg='sandy brown', command=self.enter)
        self.enter.place(x=400, y=550)

        self.login = Button(self.left, text="LOGIN", width=20, height=2, bg='indian red', command=self.reg_user)
        self.login.place(x=600, y=550)

    def enter(self):
        self.val1 = self.email_ent.get()
        self.val2 = self.pwd_ent.get()
        if self.val1 == '' and self.val2 =='' :
            tkinter.messagebox.showinfo("Warning", "Please fill up Username and Password")
        elif  self.val2 == '':
            tkinter.messagebox.showinfo("Warning", "Please fill up Password")
        elif self.val1 == '' :
            tkinter.messagebox.showinfo("Warning", "Please fill up Username")
        elif self.val1 != '' and self.val2 != '':
            sql = "INSERT INTO 'logins' (email, password) VALUES(?, ?)"
            self.val1 = self.email_ent.get()
            self.val2 = self.pwd_ent.get()
            c.execute(sql, (self.val1, self.val2))
            conn.commit()
            tkinter.messagebox.showinfo("Account info","Successfully registered." )
            print (str(d)+"\t"+str(now))
            self.destroy()
            self.diary()

    def destroy(self):
        self.email.destroy()
        self.pwd.destroy()
        self.email_ent.destroy()
        self.pwd_ent.destroy()
        self.enter.destroy()
        self.login.destroy()

    def diary(self):
        self.cloak = Label(self.left, text="DATE :"+str(d), font=('arial 14 bold'), fg='blue2', bg=background)
        self.cloak.place(x=300, y=150)
        self.heading = Label(self.left, text="DIARY - write something", font=('Bookman 40 bold'), fg='green2', bg=background)
        self.heading.place(x=300, y=50)
        self.box = Text(self.left, width=60, height=12, font=('arial 24 bold'),bg='ivory2')
        self.box.place(x=100, y=200)
        self.enter = Button(self.left, text="SAVE", width=20, height=2, bg='steelblue', command=self.save)
        self.enter.place(x=500, y=650)


    def save(self):
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
        self.enter.destroy()
        self.end = Button(self.left, text="Quit", width=20, height=2,fg='red', bg='violet', command=self.exit)
        self.end.place(x=500, y=650)
        f = open("."+res+".txt","a")
        now = time.strftime("%I:%M:%S")
        today = date.today()
        d = today.strftime("%b-%d-%Y")
        f.write(self.text+str(d)+"  "+str(now)+"\n"+"Start writing here.....")
        f.close()
        tkinter.messagebox.showinfo("Info","Successfully saved." )
        print ('=================SAVED=================')

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


        self.final_text = 'unreg_user'
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
            self.val1 = self.email_ent.get()
            self.val2 = self.pwd_ent.get()
            self.destroy()
            self.login.destroy()
            self.diary()
            self.enter.destroy()
            print(self.final_text)
            self.text = self.box.get("1.0",END)
            z = open("."+self.final_text+".txt","r")
            total_text = z.read()
            self.box.insert(END, str(total_text))
            z.close()
            self.enter = Button(self.left, text="Save", width=20, height=2,fg='red', bg='violet', command=self.update)
            self.enter.place(x=500, y=650)



    def update(self):
        now = time.strftime("%I:%M:%S")
        today = date.today()
        d = today.strftime("%b-%d-%Y")
        self.text = self.box.get("1.0",END)
        f = open("."+self.final_text+".txt","w")
        f.write(self.text+str(d)+"  "+str(now)+"\n"+"Start writing here.....")
        tkinter.messagebox.showinfo("SAVED","Successfully saved your memories." )
        self.enter.destroy()
        self.end = Button(self.left, text="Quit", width=20, height=2,fg='red', bg='violet', command=self.exit)
        self.end.place(x=500, y=650)
        print (str(d)+"\t"+str(now))
        print ('=================SAVED=================')

    def exit(self):
        root.quit()

root = Tk()
root.title("Personal Diary")
b = application(root)
root.geometry("1280x720+0+0")
root.resizable(False,False)
root.mainloop()
