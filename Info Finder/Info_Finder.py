from ctypes import alignment
from statistics import mode
import tkinter as tk
from tkinter import ttk
import wikipedia

class mini_wikipedia:
    def __init__(self, root):
        self.root = root
        self.root.title("Info Finder")
        self.root.geometry("550x550+100+100")
        self.root.config(background ='white')
        self.root.resizable(False, False)

        self.top_frame = tk.Frame(self.root, background='white')

        self.text_label = ttk.Label(self.top_frame, text = 'Enter keyword :', font=('Calibri', 14),background='white')
        self.text_label.grid(row = 0, column = 0, padx = 20)

        self.entry = ttk.Entry(self.top_frame, font = ('Calibri',14), background = 'white', width = 28)
        self.entry.grid(row = 0, column = 1, padx = 0, pady = 10)

        self.search_btn = ttk.Button(self.top_frame, text = 'Search', command = self.search_wiki)
        self.search_btn.grid(row = 0, column = 2, padx = 10)


        self.top_frame.pack(side = 'top', fill = 'x', pady = 0)

        self.bottom_frame = tk.Frame(self.root)

        self.scroll = tk.Scrollbar(self.bottom_frame, orient = 'vertical')
        self.scroll.pack(side = 'right', fill = 'y')

        self.text_area = tk.Text(self.bottom_frame, width = '45',background='#fafae3',font = ('Calibri',16), yscrollcommand = self.scroll.set, wrap = 'word')
        self.scroll.config(command = self.text_area.yview)
        self.text_area.pack(side = 'left')

        self.bottom_frame.pack(side = 'bottom', fill ='x',padx = 20, pady = 20)

        self.entry.bind("<Return>", self.enter_btn_func)
        

    def enter_btn_func(self, event):
        self.search_wiki()

    def search_wiki(self):
        self.ans_value = self.entry.get()
        self.text_area.delete(1.0, 'end')

        try:
            self.wiki_result = wikipedia.summary(self.ans_value)
            self.text_area.insert('insert', self.wiki_result)
    
        except wikipedia.exceptions.PageError:
            self.text_area.insert('insert', f'Unable to fetch information about {self.ans_value}.\nPlease try searching using different keyword..!!')
            # self.text_area.insert('insert', e)

        except wikipedia.exceptions.DisambiguationError as e:
            self.text_area.insert('insert', f"Please enter more specific word..!!\n{e}")


app = tk.Tk()
win = mini_wikipedia(app)
app.mainloop()
