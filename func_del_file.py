import glob
import os
import pathlib
from pathlib import Path

# path = r'D:\1'
# target_path = 'Doc_monitoring'
# time_sec = 1687008500
# file_suffix = ['.xlsx', '.JPG']


def del_file_suffix(path, target_path, time_sec, file_suffix, scan_del, rbtn_val):
    list_n = []
    count_size = 0
    count = 0
    print(path)
    # проходим методом glob() и walk() по выбранной директории и проверяем наличии пути до файла
    # проверка названия целевой папки. Если его нет подставляем **
    if target_path == '[Выбрать все файлы во всех папках]':
        target_path_tmp = '**'
    else:
        target_path_tmp = target_path + r'\**'
        print(target_path_tmp)
    for j in os.listdir(path):
        path_j = os.path.join(path, j)
        if os.path.isdir(path_j):
            print(j)
            for resours_dirs in Path(path_j).glob('*'):
                print(resours_dirs)
                if target_path_tmp == '**' or resours_dirs.name in target_path:
                    if not os.path.isfile(resours_dirs):
                        path_tmp = os.path.join(resours_dirs, target_path_tmp)
                    for i in glob.glob(path_tmp, recursive=True):
                        tmp_time = 0
                        if rbtn_val == 0:
                            tmp_time = os.path.getmtime(i)
                        else:
                            tmp_time = os.path.getctime(i)
                        print(i) # тестовый принт
                        if os.path.isfile(i) and pathlib.Path(i).suffix in file_suffix:# тестовый принт
                            print(i)# тестовый принт
                            if os.path.isfile(i):# тестовый принт
                                print(os.path.getmtime(i))# тестовый принт
                        if 'Удалить все файлы' in file_suffix:
                            if os.path.isfile(i) and tmp_time < time_sec:
                                count_size += os.path.getsize(i) / 1048576
                                if scan_del:
                                    os.remove(i)
                                count += 1
                        else:
                            if os.path.isfile(i) and pathlib.Path(i).suffix in file_suffix \
                                and tmp_time < time_sec:
                                count_size += os.path.getsize(i) / 1048576
                                if scan_del:
                                    os.remove(i)
                                count += 1
    list_n.append(count)
    list_n.append(count_size)
    return list_n


# print(del_file_suffix(path, target_path, time_sec, file_suffix))