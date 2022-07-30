from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import os
import sys
from datetime import datetime


#main_path = '/storage/local/docum/tmp'
extensions = {
    'image': ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']
}


def create_folders_from_list(folder_path, folder_name):
    if not os.path.exists(f'{folder_path}/{folder_name}'):
        os.mkdir(f'{folder_path}/{folder_name}')


def get_field(exif, field):
    for (k, v) in exif.items():
        if TAGS.get(k) == field:
            return v


def get_file_paths(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    return file_paths


def get_date_t(file_name):
    img = Image.open(file_name)
    img_exif = img.getexif()
    date_time = get_field(img_exif, 'DateTimeOriginal')
    print(f'File : {file_name} date : {date_time}')
    if date_time is not None:
        print(f'-{date_time}-')
        date_time_obj = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
        date_time = date_time_obj.strftime("%Y-%m-%d")
        return date_time


def sort_files(folder_path):
    file_paths = get_file_paths(folder_path)
    ext_list = list(extensions.items())
    for file_path in file_paths:
        extension = file_path.split('.')[-1]
        file_name = file_path.split('/')[-1]
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                file_date = get_date_t(file_path)
                create_folders_from_list(main_path, file_date)
                if file_date is not None:
                    print(f'Moving {file_name} in {file_date} folder \n')
                    os.rename(file_path, f'{main_path}/{file_date}/{file_name}')


if __name__ == "__main__":
    try:
        print(f'Path : {sys.argv[1]}')
        main_path = sys.argv[1]
        sort_files(main_path)
    except IndexError:
        print("Empty argument")
        print('Enter path to image folder')
        print('Example - /storage/local/docum/photo_iphoneJ')
