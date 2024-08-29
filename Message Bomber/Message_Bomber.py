import tkinter as tk
from tkinter import ttk
import pyautogui as pg
import time
from tkinter import messagebox

class bomber_gui:
    def __init__(self, win):
        self.win = win
        self.win.title("Message Bomber")
        self.win.geometry("380x380+400+200")
        self.title_label = tk.Label(win, text = 'Message Bomber by Hariom', background='black', font=('Times New Roman', 18), fg='white')
        self.title_label.pack(side = 'top', fill = 'x')

        self.label_2 = tk.Label(win, text = 'Enter number of Messages', font = ('Calibri', 16))
        self.label_2.place(x = 10, y = 50)

        self.entry_1 = ttk.Entry(win, width = '25', font = ('Calibri', 16))
        self.entry_1.place(x = 10, y = 90)

        self.label_3 = tk.Label(win, text = 'Enter your Message', font = ('Calibri', 16))
        self.label_3.place(x = 10, y = 150)

        self.entry_2 = ttk.Entry(win, width = '25', font = ('Calibri', 16))
        self.entry_2.place(x = 10, y = 190)

        self.send_btn = ttk.Button(win, text = 'Send', width = '15', command = self.send_msg)
        self.send_btn.place(x = 190, y = 250)

    def send_msg(self):
        try:
            total_msg = int(self.entry_1.get())
            msg = self.entry_2.get()

            time.sleep(10)
            for i in range(total_msg):
                pg.write(msg)
                pg.press('enter')
            messagebox.showinfo('Success', 'Your message has been sent successfully')

        except Exception as e:
            print(e)
            messagebox.showerror("Invalid Input", 'Please check your input')
            

win = tk.Tk()
obj = bomber_gui(win)
win.mainloop()
