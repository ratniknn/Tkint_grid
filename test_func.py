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


#def del_file_suffix(self):
    # path_n = path_del.get()  # указанный путь из строки
    # dt = cal_del.get_date()  # выбранная дата из строки
    # # перевод формата даты Datetime.Date в Строку(формат str)
    # second = dt.ctime()
    # # Перевод даты из строки в формат Datetime.Datetime (можно обрабатывать теперь спокойно)
    # sec1 = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
    # # счетчики по удаленным файлам, папкам и объему


path_n = r'D:\1\5790\**'
print(path_n)
pf_n = glob.glob(path_n, recursive=True)

for i in glob.glob(path_n, recursive=True):
    if os.path.isfile(i) and pathlib.Path(i).suffix == '.xls':
        print(i)
        print(os.path.getctime(i))

# print(path_n)
# second = 1679333724
# sec1 = datetime.strptime(second, "%a %b %d %H:%M:%S %Y")
# count_file = 0
# count_dir = 0
# count_size = 0
# print('!!++!!')
# for p in Path(path_n).glob('*.xls'):
#     print(p)
#     print('!!')
#     tm = os.stat(p).st_mtime
#     dts = datetime.fromtimestamp(tm)
#     print(dts)
#     # подсчет объем файлов по условию ЕСЛИ дата более ранняя чем указаная(выбранная)
#     if dts < sec1:
#         count_size += (os.path.getsize(p) / 1048576)
#         # os.remove(p)
#         count_file += 1
# print(count_dir, count_size, count_file)


# with os.scandir(path_n) as it:
#     for entry in it:
#         if not entry.name.startswith('.') and entry.is_file():
#             print(entry.name)