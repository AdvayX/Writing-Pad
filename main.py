from statistics import StatisticsError
import tkinter as tk
from tkinter import END, filedialog
from tkinter import messagebox as tmsg
from tkinter import font
from tkinter import PhotoImage
import os
import sys
import tempfile
import webbrowser as wb


#Main class
class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("780x580")
        self.minsize(780,580)
        self.title("Writing Pad")
        self.configure(background="white") 
        self.yourmenubar=tk.Menu(self)
        self.config(menu=self.yourmenubar,borderwidth=2) 
        self.font_family="Ariel"
        self.font_size=14
        self.font_style="normal"
        self.menus={}
        self.current_file=None
        self.word_wrap=True
        #GUI Iconbitmap
        def resource_path(relative_path):
            try:
                base_path=sys._MEIPASS
            except:
                base_path=os.path.abspath(".")
            return os.path.join(base_path,relative_path)
        icon=PhotoImage(file=resource_path("logo.png"))

        self.iconphoto(True,icon)
        #main frame
        self.mainframe=tk.Frame(self)
        self.mainframe.pack(fill="both",expand=True)

        #vertical scrollbar
        self.scrollbarv=tk.Scrollbar(self.mainframe)
        self.scrollbarv.pack(side="right",fill='y')

        #horizontal scrollbar
        self.scrollbarh=tk.Scrollbar(self.mainframe,orient="horizontal")
        self.scrollbarh.pack(side="bottom",fill='x')

        #status bar
        self.statusbol=False
        self.status_bar=tk.Label(self,text="Ln 1,Col 1",anchor="e",relief="groove")
        self.status_bar.pack(side="bottom",fill="x")
        if not self.statusbol:
            self.status_bar.pack_forget()
        else:
            pass           

    def open_font_window(self):
        self.fontwindow=tk.Toplevel(self)
        self.fontwindow.title("Font")
        self.fontwindow.geometry("700x450")
        self.fontwindow.maxsize(700,450)
        self.fontwindow.minsize(700,450)

        #list scrollbar
        #fontfamily
        self.scrollfont=tk.Scrollbar(self.fontwindow)
        self.scrollfont.place(x=175,y=40,height=243)

        #fontstyle
        self.scrollstyle=tk.Scrollbar(self.fontwindow)
        self.scrollstyle.place(x=385,y=40,height=243) 

        #fontsize  
        self.scrollsize=tk.Scrollbar(self.fontwindow)
        self.scrollsize.place(x=535,y=40,height=243) 

        #fontlabel
        font_label=tk.Label(self.fontwindow,text="Font",font=("bold",16)) 
        font_label.place(x=20,y=10)
        
        #font family listbox
        self.font_listbox=tk.Listbox(self.fontwindow,height=15,width=25,yscrollcommand=self.scrollfont.set,exportselection=False)
        self.scrollfont.config(command=self.font_listbox.yview)
        self.font_listbox.place(x=20,y=40)

        #all font family
        all_font=font.families()
        for item in all_font:
            self.font_listbox.insert(tk.END,item)

        #style listbox
        style_label=tk.Label(self.fontwindow,text="Style",font=("bold",16))
        style_label.place(x=260,y=10)

        self.style_listbox=tk.Listbox(self.fontwindow,height=15,width=20,yscrollcommand=self.scrollstyle.set,exportselection=False)
        self.scrollstyle.config(command=self.style_listbox.yview)
        self.style_listbox.place(x=260,y=40)

        styles=["normal","bold","italic","bold italic"]
        for item in styles:
            self.style_listbox.insert(tk.END,item)  

        #font size
        self.size_label=tk.Label(self.fontwindow,text="Size",font=("bold",16))
        self.size_label.place(x=470,y=10)

        self.size_listbox=tk.Listbox(self.fontwindow,height=15,width=10,yscrollcommand=self.scrollsize.set,exportselection=False)
        self.scrollsize.config(command=self.size_listbox.yview) 
        self.size_listbox.place(x=470,y=40)

        for i in range(8,73):
            self.size_listbox.insert(tk.END,i)

        #preview label
        self.preview_frame=tk.Frame(self.fontwindow,width=350,height=120,relief="solid",bd=2)
        self.preview_frame.place(x=350,y=375,anchor="center")
        self.preview_frame.grid_propagate(False)
        tk.Label(self.fontwindow,text="Sample",font=("bold",16)).place(x=300,y=305)

        self.preview_label=tk.Label(self.preview_frame,text=" AaBbYyZz ",relief="solid",font=("Ariel",18))
        self.preview_label.pack(expand=True)

        #apply button
        apply_btn=tk.Button(self.fontwindow,text="Apply",command=self.applyfont,padx=20)
        apply_btn.place(x=550,y=425)

        #cancel button
        cancel_button=tk.Button(self.fontwindow,text="Cancel",command=self.cancel,padx=20)
        cancel_button.place(x=620,y=425)

        #Events
        self.font_listbox.bind("<<ListboxSelect>>",self.update_preview)
        self.style_listbox.bind("<<ListboxSelect>>",self.update_preview)
        self.size_listbox.bind("<<ListboxSelect>>",self.update_preview) 

    #font function defining
    #preview update function
    def update_preview(self, event=None):

        #Default Values
        family=self.font_family
        size=self.font_size
        weight="normal"
        slant="roman" 

        #font family
        if self.font_listbox.curselection():
            index=self.font_listbox.curselection()[0]
            family=self.font_listbox.get(index) 

        #style
        if self.style_listbox.curselection():
            index=self.style_listbox.curselection()[0]
            style=self.style_listbox.get(index)
            if style=="bold":
                weight="bold"
            elif style=="italic":
                slant="italic"
            elif style=="bold italic":
                weight="bold"
                slant="italic"

        #size
        if self.size_listbox.curselection():
            index=self.size_listbox.curselection()[0]
            size=int(self.size_listbox.get(index))

        #preview_font
        preview_font=font.Font(family=family,size=size,weight=weight,slant=slant)             
        self.preview_label.config(font=preview_font)

        #save temporary selection
        self.temp_family=family
        self.temp_size=size
        self.temp_weight=weight
        self.temp_slant=slant

    #apply font
    def applyfont(self):
        final_font=font.Font(family=self.temp_family,size=self.temp_size,weight=self.temp_weight,slant=self.temp_slant)
        self.screen.config(font=final_font)
        self.fontwindow.destroy()

    #cancel command
    def cancel(self):
        self.fontwindow.destroy()    

    #Menu creating function
    def createmenu(self,menuname):
        newmenu=tk.Menu(self.yourmenubar,tearoff=0,activeborderwidth=5)
        self.yourmenubar.add_cascade(label=menuname,menu=newmenu)
        self.menus[menuname]=newmenu

    #Submenus adding function    
    def add_submenu(self,targetmenu,submenu,subcommand=None,seperator=None,accelerator=None):
        if targetmenu in self.menus:
            parentmenu=self.menus[targetmenu]
            parentmenu.add_command(label=submenu,command=subcommand,accelerator=accelerator)
            if seperator=="y":
                parentmenu.add_separator()
            else:
                None            
        else:
            print(f"Error: '{targetmenu}' named menu is not in this dictionary!") 

    #Main screen or input area adding
    def add_screen(self):
        self.screen=tk.Text(self.mainframe,font=(self.font_family,self.font_size,self.font_style),borderwidth=0,
        highlightthickness=0,yscrollcommand=self.scrollbarv.set,xscrollcommand=self.scrollbarh.set,padx=8,pady=2,
        undo=True)
        self.scrollbarv.config(command=self.screen.yview)
        self.scrollbarh.config(command=self.screen.xview)
        self.screen.pack(expand=True,fill="both")             

#Main window 
if __name__=='__main__':
    window=Notepad()

    #Defining function of menues and submenus
    
    #File menu function
    #To open a file
    def open_file():
        file= filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
        )
        try:
            if file:
                with open(file,"r") as f:
                    content=f.read()
                    window.screen.insert("1.0",content)
                window.current_file=file       
            else:
                window.current_file=None
        except:
            tmsg.showerror("FILE ERROR","THIS FILE DOESN'T EXIST!")        

    #For new file    
    def new_file():
        window.screen.delete("1.0","end")
        window.current_file=None       


    #To save the file
    def save_file():
        if window.current_file:
            with open(window.current_file,'w') as f:
                f.write(window.screen.get("1.0","end"))
        else:
            file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
        ) 
            if file:
                with open(file,"w") as f:
                    f.write(window.screen.get("1.0","end"))
                window.current_file=file
            else:
                window.current_file=None

    #print hard copy
    def print_hard_copy():
        content=window.screen.get("1.0","end") 
        temp_file=tempfile.mktemp(".txt")
        with open(temp_file,"w") as f:
            f.write(content)

        os.startfile(temp_file,"Print")
        
    #event binding
    window.bind("<Control-s>",lambda event:save_file())
    window.bind("<Control-n>",lambda event:new_file())
    window.bind("<Control-o>",lambda event:open_file())
    window.bind("<Control-p>",lambda event:print_hard_copy())                                    
    
    #Edit Menu
    #Event Binding
    window.bind("<Control-z>",lambda event:undo())
    window.bind("<Delete>",lambda event:delete())

    #textarea key binding
    window.bind("<KeyRelease>",lambda e:update_all())
    window.bind("<ButtonRelease-1>",lambda e:update_all())

    #edit menu function defining
    def undo():
        try:
            window.screen.edit_undo()
        except:
            pass 

    def cut():
        window.screen.event_generate("<<Cut>>")

    def copy():
        window.screen.event_generate("<<Copy>>")

    def paste():
        window.screen.event_generate("<<Paste>>")

    def delete():
        try:
            window.screen.delete("sel.first","sel.last") 
        except:
            pass 

    #Dymanic menu edit
    def update_edit_menu():
        try:
            content=window.screen.get("1.0","end-1c")
            if content:
                window.menus["Edit"].entryconfig("Copy",state="normal")
                window.menus["Edit"].entryconfig("Cut",state="normal")
                window.menus["Edit"].entryconfig("Delete",state="normal")
            else:
                window.menus["Edit"].entryconfig("Copy",state="disabled")
                window.menus["Edit"].entryconfig("Cut",state="disabled")
                window.menus["Edit"].entryconfig("Delete",state="disabled")
        except:
            pass    
    #disable undo
    def update_undo():
        content=window.screen.get("1.0","end-1c")
        if content:
            window.menus["Edit"].entryconfig("Undo",state="normal")
        else:
            window.menus["Edit"].entryconfig("Undo",state="disabled")

    #update all
    def update_all():
        update_edit_menu()
        update_undo()
        update_status_bar()
    #Format menu function
    #word wrap function 
    def toggle_word_wrap():
        if window.word_wrap:
            window.screen.config(wrap="none") 
            window.word_wrap=False
            window.menus["Format"].entryconfig("Word Wrap     \U00002705",label="Word Wrap")
            window.menus["View"].entryconfig("Status Bar",state="normal")
            if window.statusbol:
                window.status_bar.pack(side="bottom",fill="x")       
        else:
            window.screen.config(wrap="word")
            window.word_wrap=True
            window.menus["Format"].entryconfig("Word Wrap",label="Word Wrap     \U00002705")                   
            window.menus["View"].entryconfig("Status Bar",state="disabled",accelerator="")

    #Help menu function
    def help():
        window.help=tk.Toplevel()
        window.help.title("Help")
        window.help.geometry("350x200")
        window.help.maxsize(350,200)
        window.help.minsize(350,200)
        window.resizable(False,False)

        #Title
        title=tk.Label(window.help,text="Contact Support",font=("Ariel",14,"bold"))
        title.pack(pady=10)

        #subtitle
        subtitle=tk.Label(window.help,text="For feedback and suggestions,\n visit my GitHub profile.",font=("Ariel",12))
        subtitle.pack(pady=10)

        #GitHublabel
        GitHub_label=tk.Label(window.help,text="GitHub",fg="blue",cursor="hand2",font=("Ariel",11,"underline"))
        GitHub_label.pack(pady=10)

        #GitHub click
        GitHub_label.bind("<Button-1>",lambda e: wb.open("https://github.com/AdvayX"))
    

    def about():
        tmsg.showinfo("About","This Writing Pad Application is Developed by AdvayX.") 

    #status bar   
    #update status
    def update_status_bar(event=None):
        if window.statusbol and not window.word_wrap:
            row,col=window.screen.index("insert").split(".")
            window.status_bar.config(text=f"Ln {row},Col {int(col)+1}")
        

    #toggle status bar
    def toggle_status_bar():
        if window.statusbol:
            window.status_bar.pack_forget()
            window.statusbol=False
            window.menus["View"].entryconfig("Status Bar",accelerator="")
        else:
            if not window.word_wrap:
                window.status_bar.pack(side="bottom",fill="x")
                window.statusbol=True
                window.menus["View"].entryconfig("Status Bar",accelerator="\U00002705")


    window.createmenu("Files")
    window.add_submenu("Files","New",new_file,None,"Ctrl+N")
    window.add_submenu("Files","Open...",open_file,None,"Ctrl+O")
    window.add_submenu("Files","Save",save_file,None,"Ctrl+S")
    window.add_submenu("Files","Save As...",save_file,'y')
    window.add_submenu("Files","Print...",print_hard_copy,'y',"Ctrl+P")
    window.add_submenu("Files","Exit",window.destroy)

    window.createmenu("Edit")
    window.add_submenu("Edit","Undo",undo,"y","Ctrl+Z")
    window.add_submenu("Edit","Copy",copy,None,"Ctrl+C")
    window.add_submenu("Edit","Cut",cut,None,"Ctrl+X")
    window.add_submenu("Edit","Paste",paste,None,"Ctrl+V")
    window.add_submenu("Edit","Delete",delete,None,"Del")

    window.createmenu("Format")
    window.add_submenu("Format","Word Wrap     \U00002705",toggle_word_wrap,"y")
    window.add_submenu("Format","Font...", window.open_font_window)

    window.createmenu("View")
    window.add_submenu("View","Status Bar",toggle_status_bar)
    window.menus["View"].entryconfig("Status Bar",state="disabled")

    window.createmenu("Help")
    window.add_submenu("Help","Help",help,'y')
    window.add_submenu("Help","About",about)

    window.add_screen()
    window.mainloop()    