#The aim of the program is to standardize the name of all the photo, converting it into YYYY_MM_DD_hh_mm_ss or YYYYMMDD_hhmmss
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import termcolor
from termcolor import colored
from PIL import Image
from PIL.ExifTags import TAGS

def choose_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file explorer window
    file_path = filedialog.askopenfilename()
    print(f"Selected file: {file_path}")
    print('-------------------------------------------------------')
    return file_path

def get_exif_datetime(path):
    img = Image.open(path)
    exif_data = img._getexif()
    if not exif_data:
        return None, None

    meta_creation = exif_data.get(36867)  # DateTimeOriginal
    meta_modification = exif_data.get(36868)  # DateTimeDigitized

    return meta_creation, meta_modification

def assign_date(input, created, modified, meta_created, meta_modified):
    #to assign the number chosen by the user to the date provided by the program
    input = int(input)
    date_chosen = ''
    assert input >= 1 and input <= 4, "Input has a wrong value"

    if input == 1:
        date_chosen = str(created)
    elif input == 2:
        date_chosen = str(modified)
    elif input == 3:
        date_chosen = str(meta_created)
    elif input == 4:
        date_chosen = str(meta_modified)

    date_chosen = convert_date(date_chosen)

    return date_chosen

def convert_date(in_date):
    #to clean and prepare the date to be the file name
    assert type(in_date) is str, 'Input date is not converted to string'
    
    #CHANGE HERE THE FORMAT
    #format YYYY_MM_DD_hh_mm_ss
    #in_date = ((in_date.replace(':','_')).replace(' ','_')).replace('-','_')
    #or for the format YYYYMMDD_hhmmss
    in_date = ((in_date.replace(':','')).replace(' ','_')).replace('-','')

    if '.' in in_date:
        pos = in_date.find('.')
        out_date = in_date[:pos]
    else:
        out_date = in_date

    return out_date

def rename_file(path, date_chosen):
    #getting the file extension and folder path
    _ , extension = os.path.splitext(path)
    folder, _ = os.path.split(path)

    date_chosen += extension
    new_file = os.path.join(folder,date_chosen)

    os.rename(path, new_file)

    print('-------------------------------------------------------')
    print('New path of the file:')
    print(new_file)

    return


conf ='a'
conf2 ='a'
option = '5'

path = choose_file()

#file part
stat = os.stat(path)
created = datetime.fromtimestamp(stat.st_ctime)
modified = datetime.fromtimestamp(stat.st_mtime)

print('From the file it is possibile to obtain the following informations:')
print("File created:", created)
print("Last edit:", modified)
print('-------------------------------------------------------')

#metadata part
meta_created, meta_modified = get_exif_datetime(path)

print('From the metadata of the photo it is possibile to obtain the following informations:')
print("Photo created:", meta_created)
print("Photo edited:", meta_modified)
print('-------------------------------------------------------')


while conf != 'y' and conf != 'n':
    conf = input("Proceed to rename the file? (y/n) ")

if conf == 'y':
    while option != '1' and option != '2' and option != '3' and option != '4':
        option = input('Select which date you want to use: (1, 2, 3 or 4): ')
    
    date_chosen = assign_date(option, created, modified, meta_created, meta_modified)

    print(' ')
    print('The file will be renamed as:', date_chosen)
    print(colored('NOTE: the action cannot be undone!','red'))

elif conf == 'n':
    print(colored('Process Cancelled','red'))

while conf2 != 'y' and conf2 != 'n':
    conf2 = input("Proceed? (y/n) ")

if conf2 == 'y':
    rename_file(path, date_chosen)
    print(colored('File renamed','green'))
elif conf2 == 'n':
    print(colored('Process Cancelled','red'))

print(colored('Program done.', 'green'))
