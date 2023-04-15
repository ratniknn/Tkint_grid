import glob
import os
import pathlib
from pathlib import Path

# path = r'D:\1\5429'
# target_path = 'Doc_monitoring'
# time_sec = 1687008500
# file_suffix = ['.xlsx', '.JPG']


def del_file_suffix(path, target_path, time_sec, file_suffix):
    count = 0
    # проходим методом glob() и walk() по выбранной директории и проверяем наличии пути до файла
    # проверка названия целевой папки. Если его нет подставляем **
    if target_path == '[Выбрать все файлы во всех папках]':
        target_path_tmp = '**'
    else:
        target_path_tmp = target_path + r'\**'
        print(target_path_tmp)
    for resours_dirs in Path(path).glob('*'):
        path_tmp = os.path.join(resours_dirs, target_path_tmp)
        for i in glob.glob(path_tmp, recursive=True):
            # print(i)
            if pathlib.Path(i).suffix in file_suffix:
                print(i)
                if os.path.isfile(i):
                    print(os.path.getctime(i))
            if os.path.isfile(i) and pathlib.Path(i).suffix in file_suffix \
                    and os.path.getctime(i) < time_sec:
                # os.remove(i)
                count += 1
        return count


# print(del_file_suffix(path, target_path, time_sec, file_suffix))