import tkinter as tk
from tkinter import ttk
import func_del_file
import glob
import os
import pathlib

import babel.numbers
from datetime import datetime
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
        self.lbl1 = Label(self, text="1.Выберите папку с перечнем магазинов")
        self.lbl1.grid(row=1, sticky=W, pady=4, padx=5)
        self.lbl2 = Label(self, text="2.Выберите общую папку из перечня, \nв которой надо удалить файлы")
        self.lbl2.grid(row=2, sticky=W, pady=4, padx=5)
        self.lbl3 = Label(self, text="3.Выберите выберите дату, \nранее которой надо удалить файлы")
        self.lbl3.grid(row=3, sticky=W, pady=4, padx=5)
        self.lbl3 = Label(self, text="4.Нажмите удалить файлы и подтвердите удаление. \nВНИМАНИЕ!! Файлы удаляются безвозвратно.")
        self.lbl3.grid(row=4, sticky=W, pady=4, padx=5)

        self.path_del = Entry(self, width=56)
        self.path_del.grid(row=5, column=0, columnspan=2, padx=5, sticky=W)

        self.abtn = Button(self, text="Путь", command=self.OnOpen)
        self.abtn.grid(row=5, column=3)

        self.path_general = Combobox(self)
        self.path_general.grid(row=6, column=0, columnspan=2, padx=5, sticky=W+E)

        self.lbl_frame = Frame(self, width=55)
        self.lbl_frame.grid(row=7, column=0, padx=5)
        self.xls_val = IntVar()
        self.lbl_xls = Checkbutton(self.lbl_frame, text='*.xls', onvalue=1, offvalue=0, variable=self.xls_val)
        self.lbl_xls.grid(row=0, column=0)
        self.doc_val = IntVar()
        self.lbl_doc =Checkbutton(self.lbl_frame, text='*.doc\n*.docx', onvalue=1, offvalue=0, variable=self.doc_val)
        self.lbl_doc.grid(row=0, column=1)

        # создание поля выбора даты
        self.cal_del = DateEntry(self, width=12, hight=28, background='#3A81EA', locale='ru',
                                 foreground='white', borderwidth=5, border_radius=5, year=2016)
        self.cal_del.grid(row=8, column=0, columnspan=2, padx=5, sticky="we")

        self.btn_suf_del = Button(self, text='Удалить по \nрасширению', command=lambda: self.del_suf())
        self.btn_suf_del.grid(row=10, column=3)

        self.cbtn = Button(self, text="Анализ", command=lambda: self.count_file)
        self.cbtn.grid(row=8, column=3, pady=4)

        self.txt_log = Text(self, width=40, height=8)
        self.txt_log.grid(row=9, column=0, padx=5)

        self.enable =IntVar()
        self.no_del_path = Checkbutton(self, text='Удалять\nпустые \nпапки', onvalue=1, offvalue=0, variable=self.enable)
        self.no_del_path.grid(row=9, column=3)
        self.no_del_path.select()

        self.btn_del = Button(self, text="Удалить выбранное", command=lambda: self.del_file())
        self.btn_del.grid(row=10, column=0, padx=5)


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

    # Функция для подсчета файлов по дате в выбранной папке
    def count_file(self):
        print("__!!__")
        self.txt_log.delete('1.0', END)
        # строка из комбобокса. Целевая папка
        target_path = self.path_general.get()
        print('a' + target_path + 'b')
        # путь до первичной папки
        path_n = self.path_del.get()
        # получение даты из календаря- формат !!! Datetime.Date (геморой с переоводом)
        dt = self.cal_del.get_date()
        # перевод формата даты Datetime.Date в Строку(формат str)
        second = dt.ctime()
        # Перевод даты из строки в формат Datetime.Datetime (можно обрабатывать теперь спокойно)
        sec1 = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
        # получение списка расширения файлов для удаления
        list_suffix =[]
        if self.xls_val.get() == 1: list_suffix.append(['*.xls', '*.xlxs'])
        if self.doc_val.get() == 1: list_suffix.append(['*.doc', '*.docx'])

        for i in list_suffix:
            print(type(i))
        # счетчики по удаленным файлам, папкам и объему
        count_file = 0
        count_dir = 0
        count_size = 0

        # проходим методом glob() и walk() по выбранной директории и проверяем наличии пути до файла
        for i in Path(path_n).glob('*/'):
            # Формирование пути до папки "магазина"
            ty = path_n + '/' + i.name
            print(ty)
            # проходим по дереву каталогов в папке магазина. Получаем путь root и список папок по нему
            for root, dirs, files in os.walk(ty):
                # находим целевую папку для работы в ней
                if target_path in dirs:
                    # формируем путь до папок в целевом каталоге
                    pasts = os.path.join(ty, target_path)
                    print(pasts)
                    # проходим по вложенным папкам и формируем список путей и файлов. root1 - путь до папки с файлами
                    for root1, dirs1, files1 in os.walk(pasts):
                        for file in files1:
                            print("1" + Path(os.path.join(root1, file)).suffix)
                            if Path(os.path.join(root1, file)).suffix in list_suffix:
                                # формирование даты создания файла из свойств ()
                                d = os.stat(os.path.join(root1, file)).st_mtime
                                dts = datetime.fromtimestamp(d)
                                # подсчет объем файлов по условию ЕСЛИ дата более ранняя чем указаная(выбранная)
                                if dts < sec1:
                                    count_size += (os.path.getsize(os.path.join(root1, file)) / 1048576)
                                    count_file += 1
                            # подсчет пустых папок. Проверяем на пустоту папки.
                        for root1, dirs1, files1 in os.walk(pasts):
                            for dir1 in dirs1:
                                path_r = root1 + '/' + dir1
                                if not os.listdir(path_r):
                                    count_dir += 1
        date_file = dt.strftime('%d.%m.%Y')
        text_f = 'Найдено файлов ранее ' + date_file + ' - ' + str(count_file)
        self.txt_log.insert('1.0', text_f)
        text_dir = '\nНайдено кол-во пустых папок - ' + str(count_dir)
        self.txt_log.insert('2.0', text_dir)
        text_size = '\nОбъем выбранных файлов - ' + str(round(count_size, 2)) + ' Mb'
        self.txt_log.insert('3.0', text_size)


    # Функция для удаления файлов по дате в выбранной папке
    def del_file(self):
        result = askyesno(title="Подтвержение операции", message="Подтвердить операцию?")
        if result:
            showinfo("Результат", "Операция подтверждена")
            target_path = self.path_general.get()
            # путьдо первичной папки
            path_n = self.path_del.get()
            # получение даты из календаря- формат !!! Datetime.Date (геморой с переоводом)
            dt = self.cal_del.get_date()
            # перевод формата даты Datetime.Date в Строку(формат str)
            second = dt.ctime()
            # Перевод даты из строки в формат Datetime.Datetime (можно обрабатывать теперь спокойно)
            sec1 = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
            # счетчики по удаленным файлам, папкам и объему
            count_file = 0
            count_dir = 0
            count_size = 0
            # проходим методом glob() и walk() по выбранной директории и проверяем наличии пути до файла
            for i in Path(path_n).glob('*/'):
                # Формирование пути до аппки "магазина"
                ty = path_n + '/' + i.name
                # проходим по дереву каталогов в папке магазина. Получаем путь root и список папок по нему
                for root, dirs, files in os.walk(ty):
                    # находим целевую папку для работы в ней
                    if target_path in dirs:
                        # формируем путь до папок в целевом каталоге
                        pasts = os.path.join(ty, target_path)
                        # проходим по вложенным папкам и формируем список путей и файлов. root1 - путь до папки с файлами
                        for root1, dirs1, files1 in os.walk(pasts):
                            for file in files1:
                                # формирование даты создания файла из свойств ()
                                d = os.stat(os.path.join(root1, file)).st_mtime
                                dts = datetime.fromtimestamp(d)
                                # подсчет объем файлов по условию ЕСЛИ дата более ранняя чем указаная(выбранная)
                                if dts < sec1:
                                    count_size += (os.path.getsize(os.path.join(root1, file)) / 1048576)
                                    os.remove(os.path.join(root1, file))
                                    count_file += 1
                        # удаление пустых папок. Проверяем на пустоту папки.
                        if self.enable.get() == 1: # условие для удаления пустой папки. Данные их Checkbutton(галка)
                            for root1, dirs1, files1 in os.walk(pasts):
                                for dir1 in dirs1:
                                    path_r = root1 + '/' + dir1
                                    if not os.listdir(path_r):
                                        os.rmdir(path_r)
                                        count_dir += 1
            date_file = dt.strftime('%d.%m.%Y')
            text_f = '\nУдалено файлов ранее ' + date_file + ' - ' + str(count_file)
            self.txt_log.insert('5.0', text_f)
            text_dir = '\nУдалено пустых папок - ' + str(count_dir)
            self.txt_log.insert('6.0', text_dir)
            text_size = '\nОбъем удаленных файлов - ' + str(round(count_size, 2)) + ' Mb'
            self.txt_log.insert('7.0', text_size)
        else:
            showinfo("Результат", "Операция отменена")

    def del_suf(self):
        target_path = self.path_general.get()
        # путь до первичной папки
        path_n = self.path_del.get()
        # получение даты из календаря- формат !!! Datetime.Date (геморой с переоводом)
        dt = self.cal_del.get_date()
        # перевод формата даты Datetime.Date в Строку(формат str)
        second = dt.ctime()
        # Перевод даты из строки в формат Datetime.Datetime (можно обрабатывать теперь спокойно)
        sec1 = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
        print(sec1)
        # получение списка расширения файлов для удаления
        list_suffix = []
        if self.xls_val.get() == 1: list_suffix.append(['*.xls', '*.xlxs'])
        if self.doc_val.get() == 1: list_suffix.append(['*.doc', '*.docx'])

        for i in list_suffix:
            print(i)

        func_del_file.del_file_suffix(path_n, target_path, sec1, list_suffix)


def main():
    root = Tk()
    root.geometry("500x500")
    Example()
    root.mainloop()


if __name__ == '__main__':
    main()