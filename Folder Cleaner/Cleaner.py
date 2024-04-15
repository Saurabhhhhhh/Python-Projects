import os


# Functions
def createFolderIfNotExist(folderName):
    try:
        if not os.path.exists(folderName):
            os.makedirs(folderName)
    except Exception as e:
        print(f"Error creating folder {folderName}: {e}")

def moveFiles(folderName,files):
    try:
        for file in files:
            os.replace(file,f"{folderName}/{file}")
    except Exception as e:
        print(f"Error moving files to {folderName}: {e}")

def getFilesByExtension(extension):
    return [file for file in files if os.path.splitext(file)[1].lower() in extension]


# Listing files in the Directory
try:
    files = os.listdir()
    files.remove('Cleaner.py')
    # files.remove('Cleaner.exe')
except Exception as e:
    print(f"Error listing directory contents: {e}")


# Creating folders if not exits
folders = ['Images', 'Media', 'Docs', 'Softwares', 'Zips', 'Others']
for folder in folders:
    createFolderIfNotExist(folder)


# Extension lists
extensions = {
    "Images": ['.png','.jpg','.jpeg','.gif','.svg','.tif'],
    "Media": ['.mp3','.mp4','.avi','.wav','.mov','.flv','.avchd','.mkv','.m4a'],
    "Docs" : ['.txt', ".pdf",'.doc','.docx','.rtf','.html','.htm','.xls','.xlsx'],
    "Softwares": ['.exe', '.msi'],
    "Zips": ['.rar','.zip','.tar']
}


# Getting all the extension in the directory
filteredFiles = {}
for folder, exts in extensions.items():
    filteredFiles[folder] = getFilesByExtension(exts)


# Moving the files in their respective folders
for folder, filesList in filteredFiles.items():
    moveFiles(folder, filesList)


#Moving Other files to 'Others'
others = []
for file in files:
    if file not in set(filteredFiles) and file != 'Others':
        others.append(file)
try:
    moveFiles("Others", others)
except Exception as e:
    pass

print("Successful")