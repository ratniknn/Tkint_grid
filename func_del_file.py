import glob
import os
import pathlib
from pathlib import Path

# path = r'D:\1'
# target_path = 'Doc_monitoring'
# time_sec = 1687008500
# file_suffix = ['.xlsx', '.JPG']


def del_file_suffix(path, target_path, time_sec, file_suffix, scan_del):
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
                    path_tmp = os.path.join(path_j, target_path_tmp)
                    for i in glob.glob(path_tmp, recursive=True):
                        print(i) # тестовый принт
                        if pathlib.Path(i).suffix in file_suffix:# тестовый принт
                            print(i)# тестовый принт
                            if os.path.isfile(i):# тестовый принт
                                print(os.path.getmtime(i))# тестовый принт
                        if os.path.isfile(i) and pathlib.Path(i).suffix in file_suffix \
                                and os.path.getmtime(i) < time_sec:
                            if scan_del:
                                os.remove(i)
                            count += 1
    return count


# print(del_file_suffix(path, target_path, time_sec, file_suffix))