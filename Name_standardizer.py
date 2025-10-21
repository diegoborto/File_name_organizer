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

def choose_folder():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file explorer window
    folder_path = filedialog.askdirectory()
    print(f"Selected folder: {folder_path}")
    print('-------------------------------------------------------')
    return folder_path

def get_exif_datetime(path):
    global meta_creation, meta_modification
    img = Image.open(path)
    exif_data = img._getexif()
    if not exif_data:
        return None, None

    meta_creation = exif_data.get(36867)  # DateTimeOriginal
    meta_modification = exif_data.get(36868)  # DateTimeDigitized

    return meta_creation, meta_modification


def assign_date(input):
    global created, modified, meta_creation, meta_modification
    #to assign the number chosen by the user to the date provided by the program
    input = int(input)
    date_chosen = ''
    assert input >= 1 and input <= 4, "Input has a wrong value"

    if input == 1:
        date_chosen = str(created)
    elif input == 2:
        date_chosen = str(modified)
    elif input == 3:
        date_chosen = str(meta_creation)
    elif input == 4:
        date_chosen = str(meta_modification)

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

def get_info(path):
    global created, modified, meta_creation, meta_modification
    #file part
    stat = os.stat(path)
    created = datetime.fromtimestamp(stat.st_ctime)
    modified = datetime.fromtimestamp(stat.st_mtime)

    print('From the file it is possibile to obtain the following informations:')
    print("File created:", created)
    print("Last edit:", modified)
    print('-------------------------------------------------------')

    #metadata part
    meta_creation, meta_modification = get_exif_datetime(path)

    print('From the metadata of the photo it is possibile to obtain the following informations:')
    print("Photo created:", meta_creation)
    print("Photo edited:", meta_modification)
    print('-------------------------------------------------------')

def procedure(path):
    global conf, option, conf2
#   while conf != 'y' and conf != 'n':
#        conf = input("Proceed to rename the file? (y/n) ")
    conf = 'y'
    if conf == 'y':
        while option != '1' and option != '2' and option != '3' and option != '4':
            option = input('Select which date you want to use: (1, 2, 3 or 4): ')
        
        date_chosen = assign_date(option)

        print(' ')
        print('The file will be renamed as:', date_chosen)
        print(colored('NOTE: the action cannot be undone!','red'))

        while conf2 != 'y' and conf2 != 'n':
            conf2 = input("Proceed? (y/n) ")

        if conf2 == 'y':
            rename_file(path, date_chosen)
            print(colored('File renamed','green'))
    
    #elif conf == 'n' or conf2 == 'n':
        elif conf2 == 'n':
            print(colored('Process Cancelled','red'))
        
        
    #resetting the variables
    conf = 'a'
    conf2 = 'a' 
    option = 'a'  

#variable declaration
conf ='a'
conf2 ='a'
option = '5'
p_mode = 'a'
#------------------------------

print('Welcome to the file organizer!')
while p_mode != '1' and p_mode != '2':
    p_mode = input("What mode do you want to use? Type 1 for Folder mode or 2 for single file mode: ")

match p_mode:
    #folder mode
    case '1':
        print('Entering in folder mode.')
        path = choose_folder()
        
        # Iterate over all files in the folder
        for filename in os.listdir(path):
            #to avoid problems with hidden files
            if filename.startswith('.'):
                print(colored(f'Skipped file: {path_file}','red'))
                continue

            if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.PNG'):
                path_file = os.path.join(path,filename)
                print('')
                print(colored(f'Selected file: {path_file}','yellow'))
                #retrive information from the file
                get_info(path_file)
                #start the procedure to rename the file
                procedure(path_file)
            else:
                print(colored('Problem with the file {filename}', 'red'))
                print(colored('Extension not supported (yet)', 'red'))

    #file mode
    case '2':
        print('Entering in single file mode.')
        path = choose_file()
        #retrive information from the file
        get_info(path)
        #start the procedure to rename the file
        procedure(path)

print('')
print(colored('Program done.', 'green'))
