import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import ttk  # виджеты

from tkcalendar import Calendar, DateEntry

import expenses_helper as eh


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        self.lang = 'en'
        self.schema = eh.get_lang_schema(self.lang)
        self.style = ttk.Style()
        self.style.configure('Smpl.TLabel', padding=(10,10,60,10))
        self.style.configure('Bld.TLabel',font=('Helvetica',13,'bold'),padding=(0,10,0,10))
        self['background'] = '#EBEBEB'
        
        self.bold_font = 'Helvetica 13 bold'
        self.put_frames()
        self.put_menu()
        self.popup = Popup(self)

    def put_menu(self):
        self.config(menu=MainMenu(self))
        
    def put_frames(self):
        self.add_form_frame = AddForm(self).grid(row=0,column=0,sticky='nswe')
        self.stat_frame = StatFrame(self).grid(row=0,column=1,sticky='nswe')
        self.table_frame = TableFrame(self).grid(row=1,column=0,columnspan=2,sticky='nswe')
    
    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()
        self.put_menu()
        
    # def quit(self):
    #     self.destroy()
        
    def switch_lang(self, language):
        self.lang = language
        self.schema = eh.get_lang_schema(language)
        self.refresh()
        
class Popup:
    def __init__(self,master):
        self.master = master
        
    def show(self, window_type):
        getattr(self,window_type)()
        
    def quit(self):
        answer = mbox.askyesno('Quit', 'Are you sure?')
        if answer == True:
            self.master.destroy()
            
    def faq(self):
        mbox.showinfo('FAQ','This functionality not ready yet')
        


class MainMenu(tk.Menu):
    def __init__(self,mainwindow):
        super().__init__(mainwindow)

        # 'File'
        file_menu = tk.Menu(self)
        # 'Options'
        options_menu = tk.Menu(self)
        # 'Help'
        help_menu = tk.Menu(self)
        
        self.add_cascade(label='File',menu=file_menu)
        self.add_cascade(label='Options',menu=options_menu)
        self.add_cascade(label='Help',menu=help_menu)
        
        file_menu.add_command(label='Refresh', command=mainwindow.refresh)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=lambda: mainwindow.popup.show('quit'))
        
        lang_menu = tk.Menu(options_menu)
        self.s_var = tk.StringVar()
        self.s_var.set(self.master.lang)
        lang_menu.add_radiobutton(label='Русский',variable=self.s_var,value='ru',
        command= lambda: mainwindow.switch_lang(self.s_var.get()))
        lang_menu.add_radiobutton(label='English',variable=self.s_var,value='en',
        command= lambda: mainwindow.switch_lang(self.s_var.get()))
        options_menu.add_cascade(label='Switch language',menu=lang_menu)
        options_menu.add_separator()
        options_menu.add_command(label='Switch theme')
        help_menu.add_command(label='About Us')
        help_menu.add_separator()
        help_menu.add_command(label='FAQ',command=lambda: mainwindow.popup.show('faq'))


class AddForm(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.items = eh.get_all_expenses_items()
        self.put_widgets()
        
    def put_widgets(self):
        self.l_choose = ttk.Label(self,text=self.master.schema['l_choose'], style='Smpl.TLabel')
        self.f_choose = ttk.Combobox(self,values=self.items['names'])
        self.l_amount = ttk.Label(self,text=self.master.schema['l_amount'], style='Smpl.TLabel')
        self.f_amount = ttk.Entry(self,justify=tk.RIGHT, validate='key', 
                                  validatecommand=(self.register(self.validate_amount),'%P'))
        self.l_date = ttk.Label(self,text=self.master.schema['l_date'], style='Smpl.TLabel')
        self.f_date = DateEntry(self,foreground='black', 
                                normalforeground='black',
                                selectforeground='red',
                                background='white',
                                date_pattern='dd-mm-YYYY')
        self.btn_submit = ttk.Button(self,text=self.master.schema['btn_submit'],command=self.form_submit)

        self.l_choose.grid(row=0,column=0,sticky='w')
        self.f_choose.grid(row=0,column=1,sticky='e')
        self.l_amount.grid(row=1,column=0,sticky='w')
        self.f_amount.grid(row=1,column=1,sticky='e')
        self.l_date.grid(row=2,column=0,sticky='w')
        self.f_date.grid(row=2,column=1,sticky='e')
        self.btn_submit.grid(row=3,column=0,columnspan=2, sticky='n')

        self.f_date._top_cal.overrideredirect(False)

    def validate_amount(self, input):
        try:
            x = float(input)
            return True
        except ValueError:
            return False

    def form_submit(self):
        flag = True

        payment_date = eh.get_timestamp_from_string(self.f_date.get())
        
        try:
            expense_id = self.items['accordance'][self.f_choose.get()]
            amount = float(self.f_amount.get())
            
        except KeyError:
            if self.f_choose.get() != '':
                pass
            else:
                flag = False
        except ValueError:
            flag = False
        
        if flag:
            insert_payment = (amount, payment_date, expense_id)
            if eh.insert_payments(insert_payment):
                self.master.refresh()


class StatFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()
        
    def put_widgets(self):
        l_most_common_text = ttk.Label(self, text=self.master.schema['l_most_common'], style='Smpl.TLabel') 
        l_most_common_value = ttk.Label(self, text=eh.get_most_common_item(), style='Bld.TLabel')
        l_exp_item_text = ttk.Label(self, text=self.master.schema['l_exp_item'], style='Smpl.TLabel') 
        l_exp_item_value = ttk.Label(self, text=eh.get_most_exp_item(), style='Bld.TLabel')
        l_exp_day_text = ttk.Label(self, text=self.master.schema['l_exp_day'], style='Smpl.TLabel')
        l_exp_day_value = ttk.Label(self, text=eh.get_most_exp_day(self.master.lang), style='Bld.TLabel')
        l_exp_month_text = ttk.Label(self, text=self.master.schema['l_exp_month'], style='Smpl.TLabel')
        l_exp_month_value = ttk.Label(self, text=eh.get_most_exp_month(self.master.lang), style='Bld.TLabel')

        l_most_common_text.grid(row="0",column="0",sticky="w") 
        l_most_common_value.grid(row="0",column="1",sticky="e")
        l_exp_item_text.grid(row="1",column="0",sticky="w") 
        l_exp_item_value.grid(row="1",column="1",sticky="e") 
        l_exp_day_text.grid(row="2",column="0",sticky="w") 
        l_exp_day_value.grid(row="2",column="1",sticky="e") 
        l_exp_month_text.grid(row="3",column="0",sticky="w") 
        l_exp_month_value.grid(row="3",column="1",sticky="e") 


class TableFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()
        
    def put_widgets(self):
        table = ttk.Treeview(self, show='headings')
        l = self.master.schema
        heads = [
            l['l_head_id'], 
            l['l_head_name'], 
            l['l_head_amount'], 
            l['l_head_date']
        ]
        table['columns'] = heads

        for header in heads:
            table.heading(header,text=header,anchor='center')
            table.column(header,anchor='center')

        for row in eh.get_table_data():
            table.insert('',tk.END,values=row)

        scroll_pane = ttk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)



        
        
app = App()
app.mainloop()