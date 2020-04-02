import os.path, shutil, time, datetime
from os import path
from PIL import Image, ExifTags

cwd = os.getcwd()
print('CWD = ' + cwd)
source = cwd + '\\watchFolder\\'
print('SRC = ' + source)
target = cwd + '\\OrganisedFolder\\'
print('TD  = ' + target)

#temp dates later dates will be created from input and file info
#date layout yyyy:mm:dd
dateOfBirth = '2017:08:10'

"""
    Calculate Age from the date given and the DoB that user enters
"""
def age_calc(dateA, dateB, filename):
    dateOfBirth = dateA.split(':')
    picDate = dateB.split(':')

    year = int(picDate[0]) - int(dateOfBirth[0])
    month = int(picDate[1]) - int(dateOfBirth[1])
    day = int(picDate[2]) - int(dateOfBirth[2])

    if day < 0:
        month -= 1
    if month < 0:
        month = 12 - abs(month)
        year -= 1
    if year == 0:
        age = str(month) + ' months'
    else:
        age = str(year) + ' Year ' + str(month) + ' Months'

    success = check_for_dir(age, filename)
    return(success)

"""
Check to see if Dir exists if not create it and move picture in
"""
def check_for_dir(folderName, filename):
    #convert age to dir name then check for dir
    path = target + folderName + '\\'
    #print(path)
    if os.path.exists(path) == False:
        print('Creating folder', folderName)
        #create a folder
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            #move file to dir
            shutil.copy(source + filename, path + filename)
            success = True
    else:
        if os.path.isdir(path):
            #move file to dir
            shutil.copy(source + filename, path + filename)
            success = True
        else:
            print('file with same name found')
            # Add comparison if duplicate rename file then copy to duplicates folder in dated folder
            #if compair == 'match':

            # else rename file and copy file
            success = False
    return(success)

"""
Get Pictures and dates
"""
def get_pictures(source):
    files = os.listdir(source)
    for file in files:
        path = source + '\\' + file
        with Image.open(path) as img:
            try:
                exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
                dateCreated = exif.get('DateTime', None)
                if dateCreated == None:
                    #print(file)
                    #if date in filename make extract and add : between year:month:day
                    splitname = file.split('_')
                    for x, part in enumerate(splitname):
                        if len(part) == 8:
                            if part[x].isdigit():
                                part = part[:4] + ':' + part[4:]
                                part = part[:7] + ':' + part[7:]
                                dateCreated = ''.join(part)
                                #print(file, dateCreated, 'No Date In Tag')
                else:
                    #print(file)
                    dateCreated = dateCreated.split(' ')
                    dateCreated = ''.join(dateCreated[0])
            except:
                dateCreated = datetime.datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")
                dateCreated = str(dateCreated)
                dateCreated = dateCreated.split(' ')
                dateCreated = ''.join(dateCreated[0])
                dateCreated = dateCreated.replace('-', ':')
                #print(dateCreated)
                #print('AttError', file, e)
        success = age_calc(dateOfBirth, dateCreated, file)
        if success == True:
            continue

def init_folders():
    #create testFolders
    watchFolder = cwd + '\\watchFolder'
    OrganisedFolder = cwd + '\\OrganisedFolder'
    #source folder
    if os.path.exists(watchFolder) == False:
        watchFolderReady = False
        print('Creating watchFolder')
        #create a folder
        try:
            os.mkdir(watchFolder)
        except OSError:
            print ("Creation of the directory %s failed" % watchFolder)
    else:
        #print('The watchFolder is folder Ready')
        watchFolderReady = True
    #target folder
    if os.path.exists(OrganisedFolder) == False:
        OrganisedFolderReady = False
        print('Creating OrganisedFolder')
        #create a folder
        try:
            os.mkdir(OrganisedFolder)
        except OSError:
            print ("Creation of the directory %s failed" % OrganisedFolder)
    else:
        #print('The OrganisedFolder is folder Ready')
        OrganisedFolderReady = True
    if watchFolderReady == True and OrganisedFolderReady == True:
        return(True)
    else:
        return(False)


os.system('cls' if os.name == 'nt' else 'clear')
if init_folders() == False:
    print('The folders are now setup please add images to the watchFolder and run the program again')
else:
    print('Inital Folders are setup correctly')
    get_pictures(source)
    print('Done! Please check the OrganisedFolder to see your organised pictures')


#dateOfBirth = input('enter date of birth using folowing format yyyy:mm:dd ->')
#folderName = age_calc(dateOfBirth, testDate)
#filename = 'test.txt'

#check_for_dir(folderName, filename)