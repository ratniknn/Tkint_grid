import time
from datetime import datetime

from func_del_file import *
import os
from pathlib import Path
from tkinter import Tk, Text, BOTH, W, N, E, S, filedialog, END, Radiobutton, Checkbutton, IntVar
from tkinter.messagebox import showinfo, askyesno
from tkinter.ttk import Frame, Button, Label, Style, Entry, Combobox

from tkcalendar import DateEntry


class Example(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.master.title("ООО Спортмастер -удаление файлов по выбранной дате")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)
        self.rowconfigure(6, pad=3)
        self.rowconfigure(7, pad=3)
        self.rowconfigure(8, pad=3)
        self.rowconfigure(9, pad=3)
        self.rowconfigure(10, pad=3)

        self.lbl = Label(self, text="Удаление файлов по дате")
        self.lbl.grid(row=0, sticky=W, pady=4, padx=5)
        self.lbl1 = Label(self, text="1.Выберите папку с перечнем магазинов \n"
                                     "2.Выберите общую папку из перечня, \nв которой надо удалить файлы \n"
                                     "3.Выберите выберите дату, \nранее которой надо удалить файлы(отбор фалов ведется по дате \n последнего изменения/модернизации) \n"
                                     "4.Выберите расширение для удаляемых файлов \n"
                                     "5.Нажмите удалить файлы и подтвердите удаление. \nВНИМАНИЕ!! Файлы удаляются безвозвратно.")
        self.lbl1.grid(row=1, sticky=W, pady=4, padx=5)
        # self.lbl2 = Label(self, text="2.Выберите общую папку из перечня, \nв которой надо удалить файлы")
        # self.lbl2.grid(row=2, sticky=W, pady=4, padx=5)
        # self.lbl3 = Label(self, text="3.Выберите выберите дату, \nранее которой надо удалить файлы")
        # self.lbl3.grid(row=3, sticky=W, pady=4, padx=5)
        # self.lbl3 = Label(self, text="4.Нажмите удалить файлы и подтвердите удаление. \nВНИМАНИЕ!! Файлы удаляются безвозвратно.")
        # self.lbl3.grid(row=4, sticky=W, pady=4, padx=5)

        # строка для показа выбранного пути до основной папки
        self.path_del = Entry(self, width=56)
        self.path_del.grid(row=2, column=0, columnspan=2, padx=5, sticky=W)
        # кнопка вызова окна выбора папки
        self.abtn = Button(self, text="Путь", command=self.OnOpen)
        self.abtn.grid(row=2, column=3)
        # комбо-бокс для выбора папки внутри основной папки
        self.path_general = Combobox(self)
        self.path_general.grid(row=3, column=0, columnspan=2, padx=5, sticky=W+E)

        # комбо-бокс для выбора папки внутри основной папки
        list_suffix = [['.xls', '.xlsx'], ['.doc', '.docx'], ['.jpeg', '.jpg', '.JPG'],
                       ['.dwg', '.DWG', '.bak', '.BAK'], ['.bak', '.BAK'] ]
        self.file_suffix_del = Combobox(self, values=list_suffix)
        self.file_suffix_del.grid(row=4, column=0, columnspan=2, padx=5, sticky=W + E)

        # self.lbl_frame = Frame(self, width=55)
        # self.lbl_frame.grid(row=7, column=0, padx=5)
        # self.xls_val = IntVar()
        # self.lbl_xls = Checkbutton(self.lbl_frame, text='*.xls', onvalue=1, offvalue=0, variable=self.xls_val)
        # self.lbl_xls.grid(row=0, column=0)
        # self.doc_val = IntVar()
        # self.lbl_doc =Checkbutton(self.lbl_frame, text='*.doc\n*.docx', onvalue=1, offvalue=0, variable=self.doc_val)
        # self.lbl_doc.grid(row=0, column=1)

        # создание поля выбора даты
        self.cal_del = DateEntry(self, width=12, hight=28, background='#3A81EA', locale='ru',
                                 foreground='white', borderwidth=5, border_radius=5, year=2016)
        self.cal_del.grid(row=5, column=0, columnspan=2, padx=5, sticky="we")

        self.cbtn = Button(self, text="Анализ", command=self.del_file_suf)
        self.cbtn.grid(row=5, column=3, pady=4)

        self.txt_log = Text(self, width=40, height=8)
        self.txt_log.grid(row=6, column=0, padx=5)

        self.btn_suf_del = Button(self, text='Удалить по \nрасширению')
        self.btn_suf_del.grid(row=7, column=0)

        self.enable =IntVar()
        self.no_del_path = Checkbutton(self, text='Удалять\nпустые \nпапки', variable=self.enable)
        self.no_del_path.grid(row=6, column=3)
        tmp = self.enable.get()
        print(tmp)

        # self.btn_del = Button(self, text="Удалить выбранное", command=self.del_file)
        # self.btn_del.grid(row=10, column=0, padx=5)


    # функция для открытия окна выбора папки
    def OnOpen(self):
        path_name = filedialog.askdirectory()
        self.path_del.delete(0, 'end')
        self.path_del.insert(0, path_name)
        self.gen_path()

    # функция выбора списка папок для Combobox
    def gen_path(self):
        path = self.path_del.get()
        path_list = [r'[Выбрать все файлы во всех папках]']
        count = 0
        for resours_dirs in Path(path).glob('*'):
            for dir1 in resours_dirs.glob('*'):
                second_path = dir1.name
                # собираем перечень папок. Исключаем повторения.
                if second_path in path_list:
                    continue
                else:
                    # проверка является путь до объекта папкой или нет. Если да добавляем в список для выбора.
                    if os.path.isdir(dir1):
                        print(dir1.name)
                        path_list.append(second_path)
                        count += 1
        print(count)
        print(path_list)
        # пересоздаём ComboBox со списком папок
        self.path_general["values"] = path_list
        self.path_general["stat"] = 'readonly'

    def del_file_suf(self):
        path = self.path_del.get()
        target_path=self.path_general.get()
        dt = self.cal_del.get_date()
        # перевод формата даты Datetime.Date в Строку(формат str)
        second = dt.ctime()
        sec_ctime = time.strptime(second)
        print(time.mktime(sec_ctime))
        # Перевод даты из строки в формат Datetime.Datetime (можно обрабатывать теперь спокойно)
        time_sec = time.mktime(sec_ctime)
        # date_maby = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
        file_suffix = self.file_suffix_del.get()
        result = askyesno(title="Подтвержение операции", message="Подтвердить операцию?")
        if result:
            showinfo("Результат", "Операция подтверждена")
            count_file = del_file_suffix(path, target_path, time_sec, file_suffix)
            date_file = dt.strftime('%d.%m.%Y')
            text_f = 'Удалено файлов ранее ' + date_file + ' - ' + str(count_file) + '\n'
            self.txt_log.insert('5.0', text_f)
        else:
            showinfo("Результат", "Операция отменена")


def main():
    root = Tk()
    root.geometry("500x530")
    Example()
    root.mainloop()


if __name__ == '__main__':
    main()