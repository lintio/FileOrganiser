import os
from PIL import Image, ExifTags

dobYear = 2017
dobMonth = 8
dobDay = 10

source = os.getcwd()
print('CWD = ' + source)
target = source + '\\testFolders\\watchFolder\\'
print('TD  = ' + target)
files = os.listdir(target)
for file in files:
    path = target + '\\' + file
    #seems to not work with .jpeg files but if converted to .jpg works fine
    #if '.jpeg' in file:
        #print(file, 'is a jpeg')
    #    infile, ext = os.path.splitext(file)
    #    print(infile, 'is a jpeg')
    #    im = Image.open(path)
    #    rgb_im = im.convert('RGB')
    #    rgb_im.save(target + infile + ".png", "PNG")
    #    os.remove(target + file)
    #else:
    img = Image.open(path)
    try:
        exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        dateCreated = exif.get('DateTime', None)
        if dateCreated == None:
            #print(file)
            #if date in filename make extract and add : between year:month:day
            splitname = file.split('_')
            for x, part in enumerate(splitname):
                if len(part) == 8:
                    if part.isdigit():
                        part = part[:4] + ':' + part[4:]
                        part = part[:7] + ':' + part[7:]
                        dateCreated = ''.join(part)
                        #print(file, dateCreated, 'No Date In Tag')
        else:
            #print(file)
            dateCreated = dateCreated.split(' ')
            dateCreated = ''.join(dateCreated[0])
            #print(file, dateCreated)
        dateCreated = dateCreated.split(':')
        #calulate age at date created
        year = int(dateCreated[0])
        month = int(dateCreated[1])
        day = int(dateCreated[2])
        ageYears = year - dobYear
        ageMonths = month - dobMonth
        if ageMonths < 0:
            ageYears -= 1
            ageMonths = (12 - dobMonth) - abs(month) + 12
        ageDays = day - dobDay
        if ageDays < 0:
            age = str(ageYears) + ' years ' + str(ageMonths) + ' months'
        else:
            age = str(ageYears) + ' years ' + str(ageMonths) + ' months ' + str(ageDays) + ' days'
        print(file, dateCreated, age)
    except AttributeError as e:
        print('AttError', file, e)
        continue


        
