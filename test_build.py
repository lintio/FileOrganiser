import os.path, shutil, time, datetime
from os import path
from PIL import Image, ExifTags
from datetime import datetime

class Picture:
    def __init__(self, picName, picDate, birthDate, dateFrom, yearSelect):
        self.picName = picName
        self.picDate = picDate
        self.birthDate = birthDate
        self.dateFrom = dateFrom
        if picDate.day < birthDate.day:
            dateDiff = (picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month) - 1
            if dateDiff >= yearSelect:
                if picDate.month - birthDate.month < 0:
                    self.folderName = str((picDate.year - birthDate.year) - 1) + ' years ' + str(12 - abs(picDate.month - birthDate.month)) + ' Months'
                else:
                    self.folderName = str(picDate.year - birthDate.year) + ' years ' + str((picDate.month - birthDate.month) - 1) + ' Months'
            else:
                self.folderName = str((picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month) - 1) + ' Months'
        elif (picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month) == 0:
            self.folderName = '0 Months'
        else:
            dateDiff = (picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month)
            if dateDiff >= yearSelect:
                if picDate.month - birthDate.month < 0:
                    self.folderName = str((picDate.year - birthDate.year) - 1) + ' years ' + str(12 - abs(picDate.month - birthDate.month)) + ' Months'
                else:
                    self.folderName = str((picDate.year - birthDate.year)) + ' years ' + str(picDate.month - birthDate.month) + ' Months'
            else:
                self.folderName = str((picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month)) + ' Months'


cwd = os.getcwd()
print('CWD = ' + cwd)
source = cwd + '\\Pics_ToSort\\'
print('SRC = ' + source)
target = cwd + '\\Pics_Sorted\\'
print('TD  = ' + target)

def init_folders(): # Done and working
    #create testFolders
    Pics_ToSort = cwd + '\\Pics_ToSort'
    Pics_Sorted = cwd + '\\Pics_Sorted'
    #source folder
    if os.path.exists(Pics_ToSort) == False:
        Pics_ToSortReady = False
        print('Creating Pics_ToSort')
        #create a folder
        try:
            os.mkdir(Pics_ToSort)
        except OSError:
            print ("Creation of the directory %s failed" % Pics_ToSort)
    else:
        #print('The Pics_ToSort is folder Ready')
        Pics_ToSortReady = True
    #target folder
    if os.path.exists(Pics_Sorted) == False:
        Pics_SortedReady = False
        print('Creating Pics_Sorted')
        #create a folder
        try:
            os.mkdir(Pics_Sorted)
        except OSError:
            print ("Creation of the directory %s failed" % Pics_Sorted)
    else:
        #print('The Pics_Sorted is folder Ready')
        Pics_SortedReady = True
    if Pics_ToSortReady == True and Pics_SortedReady == True:
        return(True)
    else:
        return(False)
def get_pictures(source, birthDateInput, yearSelect):
    birthDate = datetime.strptime(birthDateInput, '%d/%m/%Y').date()
    count = 0
    files = os.listdir(source)
    for file in files:
        count += 1
        path = source + '\\' + file
        with Image.open(path) as img:
            try:
                exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
                dateCreated = exif.get('DateTime', None)
                if dateCreated == None:
                    #if date in filename make extract and add : between year:month:day
                    splitname = file.split('_')
                    for x, part in enumerate(splitname):
                        if len(part) == 8:
                            if part[x].isdigit():
                                part = part[:4] + ':' + part[4:]
                                part = part[:7] + ':' + part[7:]
                                dateCreated = ''.join(part)
                    dateSource = 'Name'
                    dateCreated = datetime.strptime(dateCreated, '%Y:%m:%d').date()
                else:
                    dateCreated = dateCreated.split(' ')
                    dateCreated = ''.join(dateCreated[0])
                    dateCreated = datetime.strptime(dateCreated, '%Y:%m:%d').date()
                    dateSource = 'MetaDate'
            except:
                dateCreated = datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")
                dateCreated = str(dateCreated)
                dateCreated = dateCreated.split(' ')
                dateCreated = ''.join(dateCreated[0])
                dateCreated = dateCreated.replace('-', ':')
                dateCreated = datetime.strptime(dateCreated, '%Y:%m:%d').date()
                dateSource = 'Modified:'
        #print(count, dateFrom, dateCreated, type(dateCreated), file)
        photo = Picture(file, dateCreated, birthDate, dateSource, yearSelect)
        print(photo.picName, photo.dateFrom, photo.folderName, photo.picDate)


os.system('cls' if os.name == 'nt' else 'clear')
if init_folders() == False:
    print('The folders are now setup please add images to the Pics_ToSort folder and run the program again')
else:
    print('Inital Folders are setup correctly')
    birthDateInput = input('Date of Birth (dd/mm/yyyy): ')
    yearSelect = int(input('For the how meny months do you want to switch to years? (e.g. 18 would become 1 years 6 months):'))
    print('The output will show the following: \n [File name, Where the files date has come from, The folder name, The file date]')
    get_pictures(source, birthDateInput, yearSelect)
    print('Done! Please check the Pics_Sorted folder to see your organised pictures')