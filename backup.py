##
# Script to compress files and put them in a separate location
# with logging which files are backupped and whoch not
# created for windows OS
# fixed backup location = 'V:\Rob\Backups\'
# Rob Ellenbroek, Nov 2019, HYD
# Written in Python 3.6
# todo: combine tine / datatime stuff
###


import os
import sys
import zipfile
import shutil
from time import gmtime, strftime
import logging
import pandas as pd
from datetime import datetime

# returns string formatted current time
def update_time():
    dateTimeObj = datetime.now()
    if dateTimeObj.minute < 10:
        minute = '0'+str(dateTimeObj.minute)
    else:
        minute = str(dateTimeObj.minute)
    if dateTimeObj.second < 10:
        second = '0'+str(dateTimeObj.second)
    else:
        second = str(dateTimeObj.second)
    unformatted_time = (str(dateTimeObj.hour),':',minute,':',second)
    return ''.join(unformatted_time)

# print with timestamp
def print_ts(lc_message):
    time = update_time()
    print(time,'-',lc_message)

#copy files and folder and compress into a zip file
def doprocess(source_folder, target_zip):
    zipf = zipfile.ZipFile(target_zip, "w")
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            try:
                logging.info (os.path.join(subdir, file))
                zipf.write(os.path.join(subdir, file))
            except:
                logging.warning (os.path.join(subdir, file))
                logging.warning ('Failed')
    try:
        lcstring = "Created ", target_zip
        logging.info (lcstring)
    except:
        pass
    print_ts ("Created "+ target_zip)

if __name__ =='__main__':

    lckeuze = ''
    i = 1
    lc_dict = {}
    dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lc_date = strftime("%Y-%m-%d", gmtime())
    
    # dertermine drive kletters on system
    drives = ['%s' % d for d in dl if os.path.exists('%s:' % d)]
    
    while not((lckeuze.upper() in drives)):
        print('Van welke schijf wil je een backup maken (maak een keuze uit: ')
        lckeuze = input(drives)

    # determine folders on chosen drive
    mappen = [dI for dI in os.listdir(lckeuze+':\\') if os.path.isdir(os.path.join(lckeuze+':\\',dI))]
    
    # create a dictionary with folders
    for j in mappen:
        lc_dict[i] = j
        i = i + 1

    print('Mappen gevonden op '+lckeuze.upper()+':\\ ')
    for k, v in lc_dict.items():
        print('{:<8} {:<15}'.format(k, v))
    
    ln_source = input('Van welke map op '+lckeuze+':\\ wilt u een backup maken?')

    lc_folder = lc_dict[int(ln_source)]

    lc_source_folder = lckeuze.upper() + ':\\' + lc_folder + '\\'
    lc_target_folder = 'V:\\Rob\\Backups\\'+lckeuze.upper()+'_'+lc_folder.upper()+'\\'
    print(lc_source_folder)
    print(lc_target_folder)

    try:
        os.makedirs(lc_target_folder)
    except OSError as e:
        pass

    # determine folders in Backup folder
    ll_folders = [dI for dI in os.listdir(lc_source_folder) if os.path.isdir(os.path.join(lc_source_folder,dI))]

    file = lc_date + '_backup.log'
    logging.basicConfig(filename=lc_target_folder+file,level=logging.DEBUG)

    for m in ll_folders:
        string = 'Starting execution of folder '+ (m)
        print_ts (string)
        logging.info (':Starting execution of folder '+ (m))
        target_zip = lc_target_folder + lc_date + '_' + (m) + '_backup.zip'
        source_folder2 = lc_source_folder+(m)
        doprocess(source_folder2, target_zip)
        
