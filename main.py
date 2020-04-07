import os.path, shutil, time, datetime
from os import path
from PIL import Image, ExifTags
from datetime import datetime

class Picture:
    def __init__(self, picName, picDate, birthDate, dateFrom, yearSelect, folderName='None_set'):
        self.picName = picName
        self.picDate = picDate
        self.birthDate = birthDate
        self.dateFrom = dateFrom
        self.folderName = folderName
        
photos = []

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
    global photos
    birthDate = datetime.strptime(birthDateInput, '%d/%m/%Y').date()
    count = 0
    files = os.listdir(source)
    for file in files:
        count += 1
        path = source + '\\' + file
        try:
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
            photos.append(photo)
            #print(photo.picName, photo.dateFrom, photo.folderName, photo.picDate)
        except:
            count -= 1
            continue
    return(count)

def calc_age():
    for photo in photos:
        picDate = photo.picDate
        birthDate = photo.birthDate
        #testResult = photo.picDate - photo.birthDate
        #print('In Days', testResult, picDate)
        # if the day is less then birth day then - 1 month
        if picDate.day - birthDate.day <= -1:
            dateDiff = (picDate.year - birthDate.year) * 12 + ((picDate.month - birthDate.month) -1)
        else:
            dateDiff = (picDate.year - birthDate.year) * 12 + (picDate.month - birthDate.month)
        #print('months =', dateDiff, picDate)
        # if months >= year select change result from months to years and months
        if dateDiff >= yearSelect:
            years = dateDiff / 12
            months = dateDiff - (12 * int(years))
            #print(int(years), months)
            #print('months =', dateDiff, picDate)
            if months == 0:
                namePart2 = ''
            elif months == 1:
                namePart2 = ' ' + str(months) + ' month'
            else:
                namePart2 = ' ' + str(months) + ' months'
            if int(years) == 1:
                namePart1 = str(int(years)) + ' year'
            else:
                namePart1 = str(int(years)) + ' years'
            result = namePart1 + namePart2
        else:
            if dateDiff <= 1:
                result = str(dateDiff) + ' month'
            else:
                result = str(dateDiff) + ' months'
            #result = str(dateDiff) + ' months'
        #print(result, picDate)
        photo.folderName = result

def check_for_dir():
    for photo in photos:
        #convert age to dir name then check for dir
        path = target + photo.folderName + '\\'
        #print(path)
        if os.path.exists(path) == False:
            print('Creating folder', photo.folderName)
            #create a folder
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                ("Creation of the directory %s successful" % path)
                #move file to dir
                shutil.move(source + photo.picName, path + photo.picName)
                #print('file copied!')
        else:
            if os.path.isdir(path):
                #move file to dir
                shutil.move(source + photo.picName, path + photo.picName)
                #print('file copied!')
            else:
                print('file with same name found')

os.system('cls' if os.name == 'nt' else 'clear')
if init_folders() == False:
    print('The folders are now setup please add images to the Pics_ToSort folder and run the program again')
else:
    print('Inital Folders are setup correctly')
    birthDateInput = input('Date of Birth (dd/mm/yyyy) -> ')
    yearSelect = int(input('For the how meny months do you want to switch to years? (e.g. 18 would become 1 years 6 months) -> '))
    count = get_pictures(source, birthDateInput, yearSelect)
    calc_age()
    copy = input(str(count) + ' Photos found would you like to start (Y/N) -> ').upper()
    if copy == 'Y' or 'YES':
        check_for_dir()
    print('Done! Please check the Pics_Sorted folder to see your organised pictures')
    print('Files that are not pictures have been left in your Pics_ToSort folder')