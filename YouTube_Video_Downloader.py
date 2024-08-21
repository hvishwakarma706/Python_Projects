from pytube import YouTube
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import requests
import io
import os
from tkinter import messagebox

class YT_Downnloader:
    def __init__(self,root):
        self.root=root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x450+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='#b3fff6')

        #================================== MAIN BODY ===============================#

        self.var_url=tk.StringVar()
        self.cr_name=ttk.Label(self.root,text=' YouTube Downloader | Developed by Hariom',font=('times new roman',15,'bold'),background='black',foreground='white')
        self.cr_name.pack(side='top',fill='x')
        ttk.Label(self.root,text='Video URL', font=('times new roman',15,'bold'),background='#b3fff6').place(x=10,y=50)
        self.vd_url=ttk.Entry(self.root,textvariable=self.var_url,font=('times new roman',15))
        self.vd_url.place(x=120,y=50,width=370)
        tk.Label(self.root, text='File Type', font=('times new roman',15,'bold'),background='#b3fff6').place(x=10,y=90)

        self.var_type=tk.StringVar()
        self.var_type.set('Video')
        style = ttk.Style()
        style.configure('Wild.TRadiobutton', background='#b3fff6', font=20)
        self.v_radio=ttk.Radiobutton(self.root, text='Video',variable=self.var_type,value='Video',style='Wild.TRadiobutton')
        self.v_radio.place(x=120,y=90)
        self.a_radio=ttk.Radiobutton(self.root, text='Audio',variable=self.var_type,value='Audio',style='Wild.TRadiobutton')
        self.a_radio.place(x=220,y=90)

        self.btn_search=ttk.Button(self.root,text='Search',command=self.search)
        self.btn_search.place(x=400,y=90, width=90)

        #-------------------------------- FRAME ----------------------------#

        self.frame1=tk.Frame(self.root,bd=2,relief='ridge',bg='lightyellow')
        self.frame1.place(x=10,y=130,width=480,height=180)

        self.vd_title=tk.Label(self.frame1,text='Video Title :- ',font=('times new roman',15,'bold'),bg='lightblue',anchor='w')
        self.vd_title.place(x=0,y=0,relwidth=1)

        self.vd_image=tk.Label(self.frame1,text='Video \nThumbnail',font=('times new roman',15),bg='#dddddd',bd=1)
        self.vd_image.place(x=5,y=32,width=180,height=140)

        tk.Label(self.frame1,text='Description',font=('Times New Roman',15,'bold')).place(x=190,y=32)
        self.vd_desc=tk.Text(self.frame1,font=('Calibri',12),bg='lightyellow')
        self.vd_desc.place(x=190,y=60,width=280,height=112)

        #-----------------------------------------------------------------------------------------------#

        self.lbl_size=ttk.Label(self.root, text='File Size : ', font=('times new roman',13,'bold'),background='#b3fff6')
        self.lbl_size.place(x=10,y=320)
        self.lbl_per=ttk.Label(self.root, text='Downloading : ', font=('times new roman',13,'bold'),background='#b3fff6')
        self.lbl_per.place(x=10,y=350)

        self.cl_btn=ttk.Button(self.root,command=self.clear,text='Clear')
        self.cl_btn.place(x=400,y=320,height=25,width=90)
        self.dn_btn=ttk.Button(self.root,text='Download',state='disabled',command=self.download)
        self.dn_btn.place(x=400,y=350,height=25,width=90)

        self.prog=ttk.Progressbar(self.root,orient='horizontal',length=500,mode='determinate')
        self.prog.place(x=10,y=390,width=480,height=20)

        ttk.Label(self.root,text='File Path : ',font=('Times New Roman',15),background='#b3fff6').place(x=10,y=420)
        self.path_entry=ttk.Entry(self.root,font=('Times New Roman',13),state='readonly')
        self.path_entry.place(x=110,y=420,width=300)
        self.path_btn=ttk.Button(self.root,text='Browse',command=self.browse)
        self.path_btn.place(x=415,y=420)


#************************************************** FUNCTIONS *******************************************************#

    def search(self):
        try:
            yt=YouTube(self.var_url.get())  

            response=requests.get(yt.thumbnail_url)
            img_byte=io.BytesIO(response.content)
            self.img=Image.open(img_byte)
            self.img=self.img.resize((180,140),Image.ANTIALIAS)
            self.img=ImageTk.PhotoImage(self.img)

            if self.var_type.get()=='Video':
                f_type=video_file=yt.streams.filter(progressive=True).first()
            elif self.var_type.get()=='Audio':
                f_type=audio_file=yt.streams.filter(only_audio=True).first()

            self.size=f_type.filesize
            self.max_size=self.size/1024000
            self.mb=str(round(self.max_size,2)) + 'MB'

            self.vd_image.config(image=self.img)
            self.vd_title.config(text=f'Video Title :- {yt.title}')
            self.vd_desc.delete('1.0','end')
            self.vd_desc.insert('end',yt.description[:200])
            self.lbl_size.config(text=f"File Size : "+ self.mb)
            self.dn_btn.config(state='normal')

        except Exception as e:
            messagebox.showerror(title='Unable to Connect With the Server', 
            message='We are unable to search the link you provided.\n\nPlease make sure that you have a porper internet connection.\nCheck whether the link you entered is correct or not.')

    def progress_(self,streams,chunk,bytes_rem):
        percentage=float(abs(bytes_rem-self.max_size)/self.size)*float(100)
        self.prog['value']=100 - percentage
        self.prog.update()
        self.lbl_per.config(text=f'Downloading : {str(round(100 - percentage,2))}%')
        self.lbl_per.update()

        if round(percentage,2)==100:
            messagebox.showinfo(title='Success',message='Download Complete..!!')
            

    def download(self):
        yt=YouTube(self.var_url.get(),on_progress_callback=self.progress_)

        try:
            if self.var_type.get()=='Video':
                f_type=yt.streams.filter(progressive=True).first()
                f_type.download(self.path)

            if self.var_type.get()=='Audio':
                f_type=yt.streams.filter(only_audio=True).first()
                out_file = f_type.download(self.path)

                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                
        except Exception as e:
            messagebox.showerror(title='Error',message=e)

    def clear(self):
        self.var_type.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.dn_btn.config(state='normal')
        self.vd_title.config(text='Video Title Here')
        self.vd_image.config(image='')
        self.vd_desc.delete('1.0','end')
        self.lbl_per.config(text='Downloading : ')
        self.lbl_size.config(text='Total Size : ')

    def browse(self):
        self.path=filedialog.askdirectory(title='Choose File Path')
        self.path_entry.config(state='normal')
        self.path_entry.delete(0,'end')
        self.path_entry.insert(0,self.path)
        self.path_entry.config(state='readonly')

win=tk.Tk()
obj=YT_Downnloader(win)
win.mainloop()
