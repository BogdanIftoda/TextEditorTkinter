import os
from tkinter import *
import tkinter.font as tkFont
from tkinter.messagebox import *
from tkinter.filedialog import *
from datetime import datetime
import webbrowser


class TextEditor:

    __root = Tk()   

    # Розмір вікна за замовчуванням
    __thisWidth = 300
    __thisHeight = 300
    # Шрифт і його розмір зазамовчуванням
    Font = tkFont.Font(family='Lucida Console', size=10)
    mainfont=Font
    # Додавання віджету Text
    __thisTextArea = Text(__root, wrap='none', font=Font, undo=1) # Для переносу цілого слова
    # Додавання віджену Text для line_numbers
    __thisLine_number_bar = Text(__root,  font = Font,  width=4, padx=3, takefocus=0,  border=0,
                       background='#f0f0f0', state='disabled',  wrap='none')
    # Додавання віджету Menu
    __thisMenuBar = Menu(__root)
    # Створення рядків меню
    # tearoff відключає можливість пересувати менюшку
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFormatMenu = Menu(__thisMenuBar, tearoff=0)
    __thisViewMenu = Menu(__thisMenuBar, tearoff=0)
    __thisThemesMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisDocMenu = Menu(__thisMenuBar, tearoff=0)

    # Додавання scrollbar
    __thisScrollBar_y = Scrollbar(__thisTextArea, orient=VERTICAL)
    __thisScrollBar_x = Scrollbar(__thisTextArea, orient=HORIZONTAL)

    __file = None

    new_file_icon = PhotoImage(file='icons/newfile.png')
    open_file_icon = PhotoImage(file='icons/openfile.png')
    save_file_icon = PhotoImage(file='icons/saveFile.png')
    save_file_as_icon = PhotoImage(file='icons/saveFileAs.png')
    cut_icon = PhotoImage(file='icons/cut.png')
    copy_icon = PhotoImage(file='icons/copy.png')
    paste_icon = PhotoImage(file='icons/paste.png')
    undo_icon = PhotoImage(file='icons/undo.png')
    redo_icon = PhotoImage(file='icons/redo.png')
    find_text_icon = PhotoImage(file='icons/find_text.png')
    exit_icon = PhotoImage(file='icons/close.png')
    select_icon = PhotoImage(file='icons/select.png')
    deselect_icon = PhotoImage(file='icons/deselect.png')
    delete_icon = PhotoImage(file='icons/delete.png')
    time_and_date_icon = PhotoImage(file='icons/time_and_date.png')
    link_icon = PhotoImage(file='icons/link.png')
    about_icon = PhotoImage(file='icons/about.png')
    about_author_icon = PhotoImage(file='icons/about_author.png')


    def __init__(self, **kwargs):

        # Встановлення іконки текстового редактора
        try:
            self.__root.wm_iconbitmap("Text_Editor.ico")
        except:
            pass

        # Set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Встановлення заголовку вікна
        self.title = "TextEditor_by_Bogdan"
        self.set_title()
        # Отримання значення висоти і ширини вікна
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)


        self.__thisLine_number_bar.pack(side='left',  fill='y')
        # Розтягування елементу Text на все вікно
        self.__thisTextArea.pack(expand='yes', fill='both')

        self.__root.protocol("WM_DELETE_WINDOW", self.quitApplication)

        # Додавання віджетів
        # Додавання функції New File
        self.__thisFileMenu.add_command(label="New File", image=self.new_file_icon, compound='left', accelerator='Ctrl+N',
                                        command=self.newFile)

        # Додавання функції Open
        self.__thisFileMenu.add_command(label="Open ", image=self.open_file_icon, compound='left', accelerator='Ctrl+O',
                                        command=self.openFile)

        # Додавання функції Save
        self.__thisFileMenu.add_command(label="Save", image=self.save_file_icon, compound='left', accelerator='Ctrl+S',
                                        command=self.saveFile)

        # Додавання функції Save as
        self.__thisFileMenu.add_command(label="Save as", image=self.save_file_as_icon, compound='left', accelerator='Ctrl+Alt+S',
                                        command=self.saveFile_as)

        # Створення лінії в діалоговому вікні
        self.__thisFileMenu.add_separator()
        # Додавання функції Виходу
        self.__thisFileMenu.add_command(label="Exit", image=self.exit_icon, compound='left', accelerator='Ctrl+Q',
                                        command=self.quitApplication)

        # Додавання пункту меню File
        self.__thisMenuBar.add_cascade(label="File",
                                       menu=self.__thisFileMenu)        

    	# Додавання функції Undo
        self.__thisEditMenu.add_command(label="Undo", image=self.undo_icon, compound='left', accelerator='Ctrl+Z',
                                        command=self.undo)

        # Додавання функції Redo
        self.__thisEditMenu.add_command(label="Redo", image=self.redo_icon, compound='left', accelerator='Ctrl+Y',
                                        command=self.redo)

        self.__thisEditMenu.add_separator()

        # Додавання функції Cut
        self.__thisEditMenu.add_command(label="Cut", image=self.cut_icon, compound='left', accelerator='Ctrl+X',
                                        command=self.cut)

        # Додавання функції Copy
        self.__thisEditMenu.add_command(label="Copy", image=self.copy_icon, compound='left', accelerator='Ctrl+C',
                                        command=self.copy)

        # Додавання функції Paste
        self.__thisEditMenu.add_command(label="Paste", image=self.paste_icon, compound='left', accelerator='Ctrl+V',
                                        command=self.paste)

        # Додавання функції Find
        self.__thisEditMenu.add_command(label="Find", image=self.find_text_icon, compound='left', accelerator='Ctrl+F',
                                        command=self.find_text)

        # Додавання функції Delete
        self.__thisEditMenu.add_command(label="Delete", accelerator='Del', image=self.delete_icon, compound='left',
                                        command=self.delete)

        self.__thisEditMenu.add_separator()

        # Додавання функції SelectAll
        self.__thisEditMenu.add_command(label="SelectAll", image=self.select_icon, compound='left', accelerator='Ctrl+A',
                                        command=self.selectall)

        # Додавання функції DeselectAll
        self.__thisEditMenu.add_command(label="Deselect", image=self.deselect_icon, compound='left', accelerator='Ctrl+Shift+A',
                                        command=self.deselectall)

        # Додавання функції Time and Date
        self.__thisEditMenu.add_command(label="Time and Date", accelerator='Ctrl+Tab', image=self.time_and_date_icon, compound='left',
                                        command=self.time_and_date)

        # Додавання пункту меню Edit
        self.__thisMenuBar.add_cascade(label="Edit",
                                       menu=self.__thisEditMenu)

        self.__thisFormatMenu.add_command(label='Font Change', accelerator='Ctrl+F1',
                                          command=self.font_changer)

        self.word_wrap = BooleanVar()
        self.__thisFormatMenu.add_checkbutton(label='Word Wrap', onvalue=True, offvalue=False, 
        							  variable=self.word_wrap, command=self.wrap)

        self.__thisMenuBar.add_cascade(label="Format",
                                       menu=self.__thisFormatMenu)

        self.show_line_number = IntVar()
        self.show_line_number.set(1)
        self.__thisViewMenu.add_checkbutton(label='Show Line Number', variable=self.show_line_number,
                          					command=self.update_line_numbers)

		# Змінна для зберігання стану віджета Checkbutton
        self.show_cursor_info = IntVar()
        # Змінній присвоюється значення 1
        self.show_cursor_info.set(1)
        # Додавання checkbutton в меню View
        self.__thisViewMenu.add_checkbutton(label='Show Cursor Location at Bottom', 
								variable=self.show_cursor_info, command=self.show_cursor_info_bar)


        self.to_highlight_line = BooleanVar()
        self.__thisViewMenu.add_checkbutton(label='Highlight Current Line', onvalue=1,
                          offvalue=0, variable=self.to_highlight_line, command=self.toggle_highlight)

        self.__thisViewMenu.add_cascade(label='Themes', menu=self.__thisThemesMenu)

        self.color_schemes = {
		    'Default': '#FFFFFF.#000000',
		    'Greygarious': '#83406A.#D1D4D1',
		    'Aquamarine': '#5B8340.#D1E7E0',
		    'Bold Beige': '#4B4620.#FFF0E1',
		    'Cobalt Blue': '#ffffBB.#3333aa',
		    'Olive Green': '#D1E7E0.#5B8340',
		    'Night Mode': '#FFFFFF.#000000',
			}

        self.theme_choice = StringVar()
        self.theme_choice.set('Default')

        for i in sorted(self.color_schemes):
        	self.__thisThemesMenu.add_radiobutton(label=i, variable=self.theme_choice,
												 command=self.change_theme)
        # Додавання функції bigger_font
        self.__thisViewMenu.add_command(label="Bigger font", accelerator='Ctrl + клавіша "+"',
                                        command=self.bigger)
        
        # Додавання функції smaller_font
        self.__thisViewMenu.add_command(label="Smaller font", accelerator='Ctrl + клавіша "-"',
                                        command=self.smaller)

        # Додавання функції default_font
        self.__thisViewMenu.add_command(label="Default font", accelerator='Ctrl + 0',
                                        command=self.default_font)

        # Додавання пункту меню View
        self.__thisMenuBar.add_cascade(label="View",
                                       menu=self.__thisViewMenu)

        # Додавання функцій опису TextEditor
        self.__thisHelpMenu.add_command(label="About Text Editor", image=self.about_icon, compound='left', accelerator='F2',
                                        command=self.showAbout)

        self.__thisHelpMenu.add_command(label="About Author", image=self.about_author_icon, compound='left',
                                        command=self.showAboutAuthor)

        # Додавання пункту меню Help
        self.__thisMenuBar.add_cascade(label="Help",
                                       menu=self.__thisHelpMenu)

        self.docs = IntVar()
        # Змінній присвоюється значення 1
        self.docs.set(0)
        # Додавання функцій Documentation
        self.__thisDocMenu.add_radiobutton(label = "Python", variable = self.docs, value=0 , image=self.link_icon, compound='left', command = self.doc)

        self.__thisDocMenu.add_radiobutton(label = "JavaScript", variable = self.docs, value=1 ,image=self.link_icon, compound='left', command = self.doc)

        self.__thisDocMenu.add_radiobutton(label = "Django", variable = self.docs, value=2 ,image=self.link_icon, compound='left', command = self.doc)

        self.__thisDocMenu.add_radiobutton(label = "MySql", variable = self.docs, value=3 ,image=self.link_icon, compound='left', command = self.doc)

        self.__thisDocMenu.add_radiobutton(label = "HTML", variable = self.docs, value=4 ,image=self.link_icon, compound='left', command = self.doc)       

        self.__thisDocMenu.add_radiobutton(label = "CSS", variable = self.docs, value=5 ,image=self.link_icon, compound='left', command = self.doc)

        self.__thisDocMenu.add_radiobutton(label = "PHP", variable = self.docs, value=6 ,image=self.link_icon, compound='left', command = self.doc)

        # Додавання пункту меню Documentation
        self.__thisMenuBar.add_cascade(label = "Documentation", menu = self.__thisDocMenu)

        self.__root.config(menu=self.__thisMenuBar)

        # Настройка скрола, з правої сторони, вертикально
        self.__thisScrollBar_y.pack(side=RIGHT, fill=Y)

        self.__thisScrollBar_x.pack(side=BOTTOM, fill=X, anchor='w')

        # Прив'язування прокрутки скрола по осі Y
        self.__thisScrollBar_y.config(command=self.multiple_yview)

        self.__thisScrollBar_x.config(command=self.__thisTextArea.xview)

        # Встановлення скрола для текстового поля
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar_y.set, 
        						   xscrollcommand=self.__thisScrollBar_x.set)

        # self.__thisTextArea.xview('moveto', '1.0')
        self.__thisLine_number_bar.config(yscrollcommand=self.__thisScrollBar_y.set)

        # Додавання функції Show_cursor_info_bar
        self.cursor_info_bar = Label(self.__thisTextArea, text='Line: 1 | Column: 1')

        # Розташування cursor_info_bar
        self.cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

    def multiple_yview(self,*args):
        self.__thisTextArea.yview(*args)
        self.__thisLine_number_bar.yview(*args)

    def OnMouseWheel(self, event):
        self.__thisTextArea.yview("scroll", event.delta,"units")
        self.__thisLine_number_bar.yview("scroll",event.delta,"units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"

    def save_if_modified(self, event=None):
        if self.__thisTextArea.edit_modified():  # modified
            # yes = True, no = False, cancel = None
            response = messagebox.askyesnocancel(
                "Save?", "This document has been modified. Do you want to save changes?")
            if response:  # yes/save
                result = self.saveFile()
                if result == "saved":  # saved
                    return True
                else:  # save cancelled
                    return None
            else:
                return response  # None = cancel/abort, False = no/discard
        else:  # not modified
            return True

    # Ф-ція створення файла
    def newFile(self, event=None):
        result = self.save_if_modified()
        if result != None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.__thisTextArea.delete(1.0, END)
            self.__thisTextArea.edit_modified(False)
            self.__thisTextArea.edit_reset()  # Видаллення усіх undo і redo
            self.__file = None
            self.set_title()
            self.on_content_changed()

    # Ф-ція відкривання файла
    def openFile(self, event=None, local_file=None):
        result = self.save_if_modified()
        if result != None:
            if local_file == None:
                local_file = askopenfilename(defaultextension=".txt",
                                             filetypes=[("All Files", "*.*"),
                                                        ("Text Documents", "*.txt"),
                                                        ("Python", "*.py"),
                                                        ("C#", "*.cs;*.csx;*.cake"),
                                                        ("Go", "*.go"),
                                                        ("Java", "*.java,"),
                                                        ("JSON", "*.json"),
                                                        ("JavaScript", "*.js"),
                                                        ("HTML", "*.html;*.htm"),
                                                        ("PHP", "*.php"),
                                                        ("CSS", "*.css"),
                                                        ("SQL database", "*.sql"),
                                                        ("Database", "*.db;*.dbf")
                                                        ])

            if local_file != None and local_file != '':
                with open(local_file, encoding='utf-8') as f:
                    fileContent = f.read()
                self.__thisTextArea.delete(1.0, END)
                self.__thisTextArea.insert(1.0, fileContent)
                self.__thisTextArea.edit_modified(False)
                self.__file = local_file
                self.set_title()
                self.on_content_changed()

    # Ф-ція зберігання файла
    def saveFile(self, event=None):
        if self.__file == None:
            result = self.saveFile_as()
        else:
            result = self.saveFile_as(local_file=self.__file)
        return result
    
    # Ф-ція  зберігання файла_як
    def saveFile_as(self, event=None, local_file=None):
        if local_file == None:
            local_file = asksaveasfilename(initialfile='Untitled.txt',
                                           defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"),
                                                      ("Text Documents", "*.txt"),
                                                      ("Python", "*.py"),
                                                      ("C#", "*.cs;*.csx;*.cake"),
                                                      ("Go", "*.go"),
                                                      ("Java", "*.java,"),
                                                      ("JSON", "*.json"),
                                                      ("JavaScript", "*.js"),
                                                      ("HTML", "*.html;*.htm"),
                                                      ("PHP", "*.php"),
                                                      ("CSS", "*.css"),
                                                      ("SQL database", "*.sql"),
                                                      ("Database", "*.db;*.dbf")
                                                      ])

        try:
            with open(local_file, 'w', encoding='utf-8') as f:
                text = self.__thisTextArea.get(1.0, END)
                f.write(text)
                self.__thisTextArea.edit_modified(False)
                self.__file = local_file
                self.set_title()
                return "saved"

        except FileNotFoundError:
            print("FileNotFoundError")
            return "cancelled"

    # Ф-ція виходу
    def quitApplication(self, event=None):
        result = self.save_if_modified()
        if result != None:
            self.__root.destroy()
        # exit()

    # Ф-ція зміни заголовків
    def set_title(self, event=None):
        if self.__file != None:
            title = os.path.basename(self.__file)
        else:
            title = "Untitled"
        self.__root.title(title + " - " + self.title)


    # Ф-ція скасувати
    def undo(self, event=None):
        try:
            self.__thisTextArea.edit_undo()
            self.on_content_changed()
        except:
            pass
    
    # Ф-ція повторити
    def redo(self, event=None):
        try:
            self.__thisTextArea.edit_redo()
            self.on_content_changed()
        except:
            pass
    
    # Ф-ція вирізати
    def cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")
        self.on_content_changed()

    # Ф-ція копіювання
    def copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")
        self.on_content_changed()

    # Ф-ція вставлення
    def paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")
        self.on_content_changed()

    # Ф-ція видалення 
    def delete(self, event=None):
        self.__thisTextArea.event_generate('<<Clear>>')
        self.on_content_changed()

    # Ф-ція вибрати все
    def selectall(self):
        self.__thisTextArea.tag_add("sel", '1.0', 'end')
        self.on_content_changed()

    # Ф-ція скасувати вибране
    def deselectall(self, event=None):
        self.__thisTextArea.tag_remove("sel", '1.0', 'end')

    # Ф-ція час та дата
    def time_and_date(self, event=None):
        self.__thisTextArea.insert(
            END, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Ф-ція
    def find_text(self,event=None):
	    search_toplevel = Toplevel(self.__root)
	    search_toplevel.title('Find Text')
	    search_toplevel.transient(self.__root)

	    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')

	    search_entry_widget = Entry(
	        search_toplevel, width=25)
	    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
	    search_entry_widget.focus_set()
	    ignore_case_value = IntVar()
	    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
	        row=1, column=1, sticky='e', padx=2, pady=2)
	    Button(search_toplevel, text="Find All", underline=0,
	           command=lambda: self.search_output(
	               search_entry_widget.get(), ignore_case_value.get(),
	               search_toplevel, search_entry_widget)
	           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
        # Ф-ція закриванян вікна пошуку
	    def close_search_window():
	        self.__thisTextArea.tag_remove('match', '1.0', END)
	        search_toplevel.destroy()
	    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
	    return "break"

    # Ф-ція
    def search_output(self,get_value, if_ignore_case,
                  search_toplevel, search_box):
	    self.__thisTextArea.tag_remove('match', '1.0', END)
	    matches_found = 0
	    if get_value:
	        start_pos = '1.0'
	        while True:
	            start_pos = self.__thisTextArea.search(get_value, start_pos,
	                                            nocase=if_ignore_case, stopindex=END)
	            if not start_pos:
	                break
	            end_pos = '{}+{}c'.format(start_pos, len(get_value))
	            self.__thisTextArea.tag_add('match', start_pos, end_pos)
	            matches_found += 1
	            start_pos = end_pos
	        self.__thisTextArea.tag_config(
	            'match', foreground='red', background='yellow')
	    search_box.focus_set()
	    search_toplevel.title('{} matches found'.format(matches_found))

    # Ф-ція переносу по словах
    def wrap(self):
        if self.word_wrap.get() == True:
        	self.__thisTextArea.config(wrap="word")
        	self.__thisScrollBar_x.pack_forget()
        	self.on_content_changed()
        else:
        	self.cursor_info_bar.pack_forget()
        	self.__thisTextArea.config(wrap="none")
        	self.__thisScrollBar_x.pack(side=BOTTOM, fill=X, anchor='w')
        	self.cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
        	self.on_content_changed()


    def font_changer(self, event=None):
        self.font_toplevel = Toplevel(self.__root)
        self.font_toplevel.title("Font changer")
        self.font_toplevel.transient(self.__root)

        #Змінні
        self.var=StringVar()
        self.var.set(self.mainfont.actual('family'))
        self.var1=IntVar()
        self.var1.set(self.mainfont.actual('size'))
        self.var2=StringVar()
        self.var2.set(self.mainfont.actual('weight'))
        self.var3=StringVar()
        self.var3.set(self.mainfont.actual('slant'))
        self.var4=IntVar()
        self.var4.set(self.mainfont.actual('underline'))
        self.var5=IntVar()
        self.var5.set(self.mainfont.actual('overstrike'))
        #Зразок шрифту
        self.font_1=tkFont.Font()
        for i in ['family', 'weight', 'slant', 'overstrike', 'underline', 'size']:
            self.font_1[i]=self.mainfont.actual(i)

        def checkface(event):
            try:
                self.var.set(str(self.listbox.get(self.listbox.curselection())))
                self.font_1.config(family=self.var.get(), size=self.var1.get(), weight=self.var2.get(), slant=self.var3.get(), 
                                    underline=self.var4.get(), overstrike=self.var5.get())
            except:
                pass

        def checksize(event):
            try:
                self.var1.set(str(self.size.get(self.size.curselection())))
                self.font_1.config(family=self.var.get(), size=self.var1.get(), weight=self.var2.get(), slant=self.var3.get(), 
                                    underline=self.var4.get(), overstrike=self.var5.get())
            except:
                pass

        def applied():
            self.result=(self.var.get(), self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get())
            self.mainfont['family']=self.var.get()
            self.mainfont['size']=self.var1.get()
            self.mainfont['weight']=self.var2.get()
            self.mainfont['slant']=self.var3.get()
            self.mainfont['underline']=self.var4.get()
            self.mainfont['overstrike']=self.var5.get()

        def out():
            self.result=(self.var.get(), self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get())
            self.mainfont['family']=self.var.get()
            self.mainfont['size']=self.var1.get()
            self.mainfont['weight']=self.var2.get()
            self.mainfont['slant']=self.var3.get()
            self.mainfont['underline']=self.var4.get()
            self.mainfont['overstrike']=self.var5.get()
            self.font_toplevel.destroy()

        def cancel():
            self.result=None
            self.mainfont['family']='Lucida Console'
            self.mainfont['size']=10
            self.mainfont['weight']='normal'
            self.mainfont['slant']='roman'
            self.mainfont['underline']=0
            self.mainfont['overstrike']=0
            self.font_toplevel.destroy()

        self.mainframe = Frame(self.font_toplevel)
        self.mainframe.pack(side='top', pady=10, padx=10 , ipady=20, ipadx=20, expand='yes', fill='both')
        self.mainframe0 = Frame(self.font_toplevel)
        self.mainframe0.pack(side='top', expand='yes', fill='x', padx=10, pady=10)
        self.mainframe1 = Frame(self.font_toplevel)
        self.mainframe1.pack(side='top', expand='yes', fill='both')
        self.mainframe2 = Frame(self.font_toplevel)
        self.mainframe2.pack(side='top', pady=10, padx=10, expand='yes', fill='both')
        self.frame = LabelFrame(self.mainframe,text='Select Font')
        self.frame.pack(side='left', pady=10, padx=10 , ipady=20, ipadx=20, expand='yes', fill='both')
        self.frame1 = LabelFrame(self.mainframe,text='Select Font Size')
        self.frame1.pack(side='left', pady=10, padx=10 , ipady=20, ipadx=20, expand='yes', fill='both')
        Entry(self.frame, textvariable=self.var).pack(side='top', padx=5, pady=5, expand='yes', fill='x')
        self.listbox = Listbox(self.frame, bg='ivory2')
        self.listbox.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
        for i in tkFont.families():
            self.listbox.insert(END,i)

        Entry(self.frame1, textvariable=self.var1).pack(side='top', padx=5, pady=5, expand='yes', fill='x')
        self.size = Listbox(self.frame1, bg='ivory2')
        self.size.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
        for i in range(31):
            self.size.insert(END,i)

        Label(self.mainframe1, bg='white', text='''
ABCDEabcde12345
''', font=self.font_1).pack(expand='no', padx=5, pady=10)

        self.bold=Checkbutton(self.mainframe0, text='Bold', onvalue='bold', offvalue='normal', variable=self.var2)
        self.bold.pack(side='left', expand='yes', fill='x')
        self.italic=Checkbutton(self.mainframe0, text='Italic', onvalue='italic', offvalue='roman', variable=self.var3)
        self.italic.pack(side='left', expand='yes', fill='x')
        self.underline=Checkbutton(self.mainframe0, text='Underline', onvalue=1, offvalue=0, variable=self.var4)
        self.bold.pack(side='left', expand='yes', fill='x')
        self.overstrike=Checkbutton(self.mainframe0, text='Overstrike', onvalue=1, offvalue=0, variable=self.var5)
        self.overstrike.pack(side='left', expand='yes', fill='x')

        Button(self.mainframe2, text='OK', command=out).pack(side='left', padx=5, pady=5, expand='yes',fill='x')
        Button(self.mainframe2, text='Apply', command=applied).pack(side='left', padx=5, pady=5, expand='yes',fill='x')
        Button(self.mainframe2, text='Cancel', command=cancel).pack(side='left', padx=5, pady=5, expand='yes',fill='x')

        self.listbox.bind('<<ListboxSelect>>', checkface)
        self.size.bind('<<ListboxSelect>>', checksize)


    # Ф-ція показу номеру рядка
    def get_line_numbers(self):
	    output = ''
	    if self.show_line_number.get():
	        line, col = self.__thisTextArea.index("end").split('.')	
	        for i in range(1, int(line)):
	            output += str(i) + '\n'
	    return output

    def update_line_numbers(self,event=None):
	    line_numbers = self.get_line_numbers()
	    self.__thisLine_number_bar.config(state='normal')
	    self.__thisLine_number_bar.delete('1.0', 'end')
	    self.__thisLine_number_bar.insert('1.0', line_numbers)
	    self.__thisLine_number_bar.yview(END)
	    self.__thisLine_number_bar.config(state='disabled')

    # Ф-ція показу курсора
    def show_cursor_info_bar(self):
    	show_cursor_info_checked = self.show_cursor_info.get()
    	if show_cursor_info_checked:
        	self.cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    	else:
        	self.cursor_info_bar.pack_forget()


    def update_cursor_info_bar(self,event=None):
	    line, col = self.__thisTextArea.index(INSERT).split('.')
	    line_num, col_num = str(int(line)), str(int(col) + 1)  # col starts at 0
	    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
	    self.cursor_info_bar.config(text=infotext)

    # Ф-ція для оновлення положення курсора і рядка
    def on_content_changed(self,event=None):
	    self.update_line_numbers()
	    self.update_cursor_info_bar()

    # Ф-ції підсвічування рядка
    def highlight_line(self,interval=100):
	    self.__thisTextArea.tag_remove("active_line", 1.0, "end")
	    self.__thisTextArea.tag_add(
	        "active_line", "insert linestart", "insert lineend+1c")
	    self.__thisTextArea.after(interval, self.toggle_highlight)


    def undo_highlight(self):
	    self.__thisTextArea.tag_remove("active_line", 1.0, "end")


    def toggle_highlight(self,event=None):
	    if self.to_highlight_line.get():
	        self.highlight_line()
	    else:
	        self.undo_highlight()

   # Ф-ція зміни теми
    def change_theme(self,event=None):
	    selected_theme = self.theme_choice.get()
	    fg_bg_colors = self.color_schemes.get(selected_theme)
	    foreground_color, background_color = fg_bg_colors.split('.')
	    self.__thisTextArea.config(
	        background=background_color, fg=foreground_color)

    # Ф-ція збільшення шрифту
    def bigger(self, event=None):
        max_size = 70
        size = int(self.Font.cget("size"))
        size += 2
        if size != max_size:
            self.Font.configure(size=size)

    # Ф-ція зменшення шрифту 
    def smaller(self, event=None):
        min_size = 0
        size = int(self.Font.cget("size"))
        size -= 2
        if size != min_size:
            self.Font.configure(size=size)

    # Ф-ція шрифту за замовчуванням
    def default_font(self, event=None):
    	size = 10
    	self.Font.configure(size=size)

   	# Про редактор
    def showAbout(self, event=None):
        showinfo("TextEditor_by_Bogdan", '''Version 1.0
Chornivka Corporation, 2020.
This product is licensed!
''')

    # Про автора
    def showAboutAuthor(self):
        showinfo('About the Author',
                 'The Author of the programm is Bogdan Iftoda\nThanks for using my TextEditor!')

    # Документація
    def doc(self):
    	chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    	webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

    	if self.docs.get() == 0:
    		webbrowser.get('chrome').open_new_tab('https://docs.python.org/3/')
    	elif self.docs.get() == 1:
            webbrowser.get('chrome').open_new_tab('https://devdocs.io/javascript/')
    	elif self.docs.get() == 2:
            webbrowser.get('chrome').open_new_tab('https://docs.djangoproject.com/en/3.0/')
    	elif self.docs.get() == 3:
            webbrowser.get('chrome').open_new_tab('https://dev.mysql.com/doc/')
    	elif  self.docs.get() == 4:
            webbrowser.get('chrome').open_new_tab('https://devdocs.io/html/')
    	elif self.docs.get() == 5:
            webbrowser.get('chrome').open_new_tab('https://devdocs.io/css/')
    	elif self.docs.get() == 6:
            webbrowser.get('chrome').open_new_tab('https://www.php.net/docs.php')
             

    def main(self, event=None):
        self.__thisTextArea.bind('<Control-N>', self.newFile)
        self.__thisTextArea.bind('<Control-n>', self.newFile)
        self.__thisTextArea.bind('<Control-O>', self.openFile)
        self.__thisTextArea.bind('<Control-o>', self.openFile)
        self.__thisTextArea.bind('<Control-S>', self.saveFile)
        self.__thisTextArea.bind('<Control-s>', self.saveFile)
        self.__thisTextArea.bind('<Control-Alt-S>', self.saveFile_as)
        self.__thisTextArea.bind('<Control-Alt-s>', self.saveFile_as)
        self.__thisTextArea.bind('<Control-Q>', self.quitApplication)
        self.__thisTextArea.bind('<Control-q>', self.quitApplication)
        self.__thisTextArea.bind('<Control-Z>', self.undo)
        self.__thisTextArea.bind('<Control-Y>', self.redo)
        self.__thisTextArea.bind('<Control-Shift-A>', self.deselectall)
        self.__thisTextArea.bind('<Control-F>', self.find_text)
        self.__thisTextArea.bind('<Control-f>', self.find_text)
        self.__thisTextArea.bind('<Control-Tab>', self.time_and_date)
        self.__thisTextArea.bind('<Delete>', self.delete)
        self.__thisTextArea.bind("<MouseWheel>", self.OnMouseWheel)
        self.__thisLine_number_bar.bind("<MouseWheel>", self.OnMouseWheel)
        self.__thisTextArea.bind('<KeyPress-F1>', self.font_changer)
        self.__thisTextArea.bind('<Control-Key-equal>', self.bigger)
        self.__thisTextArea.bind('<Control-Key-minus>', self.smaller)
        self.__thisTextArea.bind('<Control-Key-0>', self.default_font)
        self.__thisTextArea.bind('<KeyPress-F2>', self.showAbout)
        self.__thisTextArea.bind('<Any-KeyPress>', self.on_content_changed)
        self.__thisTextArea.bind('<Button-1>', self.on_content_changed)
        self.__thisTextArea.tag_configure('active_line', background='ivory2')
        self.__thisTextArea.bind("<Button-3>", lambda event: self.__thisEditMenu.post(event.x_root, event.y_root))


    def run(self):
        # Run main application
        self.__root.mainloop()
        


# Run main application
texteditor = TextEditor(width=600, height=400)
texteditor.main()
texteditor.run()
