#The aim of the program is to standardize the name of all the photo, converting it into YYYY_MM_DD_hh_mm_ss or YYYYMMDD_hhmmss
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import termcolor
from termcolor import colored
from PIL import Image
from PIL.ExifTags import TAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def choose_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file explorer window
    file_path = filedialog.askopenfilename()
    #print(f"Selected file: {file_path}")
    print('-------------------------------------------------------')
    return file_path

def choose_folder():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file explorer window
    folder_path = filedialog.askdirectory()
    print(f"Selected folder: {folder_path}")
    n_files = len(os.listdir(folder_path))
    print(f'The folder contains {n_files} files.')
    print('-------------------------------------------------------')
    return folder_path

def get_photo_meta(path):
    global meta_creation, meta_modification
    img = Image.open(path)
    exif_data = img._getexif()
    if not exif_data:
        return None, None

    meta_creation = exif_data.get(36867)  # DateTimeOriginal
    meta_modification = exif_data.get(36868)  # DateTimeDigitized

    print('From the metadata of the photo it is possibile to obtain the following informations:')
    print("Photo file_created:", meta_creation)
    print("Photo edited:", meta_modification)
    print('-------------------------------------------------------')



def assign_date(input):
    global file_created, file_modified, meta_creation, meta_modification
    #to assign the number chosen by the user to the date provided by the program
    input = int(input)
    date_chosen = ''
    assert input >= 0 and input <= 4, "Input has a wrong value"

    if input == 0: 
        return date_chosen

    if input == 1:
        date_chosen = str(file_created)
    elif input == 2:
        date_chosen = str(file_modified)
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
    global file_created, file_modified
    #file part
    stat = os.stat(path)
    file_created = datetime.fromtimestamp(stat.st_ctime)
    file_modified = datetime.fromtimestamp(stat.st_mtime)

    print('From the file it is possibile to obtain the following informations:')
    print("File created:", file_created)
    print("Last edit:", file_modified)
    print('-------------------------------------------------------')

def procedure(path):
    global conf, option, conf2
#   while conf != 'y' and conf != 'n':
#        conf = input("Proceed to rename the file? (y/n) ")
    conf = 'y'
    if conf == 'y':
        while option != '1' and option != '2' and option != '3' and option != '4' and option != '0':
            option = input('Select which date you want to use (type 1 to 4, 0 to skip): ')
        
        date_chosen = assign_date(option)

        if date_chosen == '':
            conf2 = 'n'
        else:
            print(' ')
            print('The file will be renamed as:', date_chosen)
            print('NOTE: the action cannot be undone!')

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

def get_video_meta(path):
    global meta_creation, meta_modification
    parser = createParser(path)
    metadata = extractMetadata(parser)

    if metadata:
        meta_creation = metadata.get("creation_date")
    else:
        return None 
    meta_modification = None

    print('From the metadata of the video it is possibile to obtain the following informations:')
    print("Video file_created:", meta_creation)
    print('-------------------------------------------------------')

def get_type_file(path):
    #get the extension and return the file type
    _ , extension = os.path.splitext(path)
    extension.lower()

    if extension == '.mp4':
        type_file = 'video_mp4'
    elif extension == '.jpg' or extension == '.jpeg' or extension == '.png':
        type_file = 'photo'
    else:
        type_file = 'else'

    return type_file

#------------------------------------------------------------------------------
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
            
            path_file = os.path.join(path,filename)

            type_file = get_type_file(path_file)

            if type_file == 'photo':
                print('')
                print(colored(f'Selected file: {path_file}','yellow'))
                #retrive information from the file
                get_info(path_file)
                get_photo_meta(path_file)
                #start the procedure to rename the file
                procedure(path_file)
            
            elif type_file == 'video_mp4':
                #retrive information from the file
                get_info(path_file)
                get_video_meta(path_file)
                #start the procedure to rename the file
                procedure(path_file)           
            else:
                print(colored('Problem with the file {filename}', 'red'))
                print(colored('Extension not supported (yet)', 'red'))

    #file mode
    case '2':
        print('Entering in single file mode.')
        path = choose_file()
        type_file = get_type_file(path)

        if type_file == 'photo':
            print('')
            print(colored(f'Selected file: {path}','yellow'))
            #retrive information from the file
            get_info(path)
            get_photo_meta(path)
            #start the procedure to rename the file
            procedure(path)
        
        elif type_file == 'video_mp4':
            #retrive information from the file
            get_info(path)
            get_video_meta(path)
            #start the procedure to rename the file
            procedure(path)           
        else:
            print(colored('Problem with the file {filename}', 'red'))
            print(colored('Extension not supported (yet)', 'red'))


print('')
print(colored('Program done.', 'green'))
