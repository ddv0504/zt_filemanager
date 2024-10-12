#-*- coding: utf-8 -*-
# Author: JC OH
# Created: 2024-10-12
# Updated: 2024-10-12
# Purpose: File Management Utility Functions

import os
import csv
import time
import datetime
import logging
import logging.handlers
import re
import json

from pathlib import Path

# Logging
def set_logger(log_file, log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler(log_file)
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger

# Logging Wrapper
def log_info(logger, msg):
    logger.info(msg)
    
def log_error(logger, msg):
    logger.error(msg)

def log_warning(logger, msg):
    logger.warning(msg)

def log_debug(logger, msg):
    logger.debug(msg)

# File Management
def get_file_list(path, ext):
    directory = Path(path)
    file_list = list(directory.glob(ext))
    return file_list

# File list all files in the directory including subdirectories
def get_file_list_all(path, ext='*'):
    directory = Path(path)
    file_list = list(directory.glob('**/*.' + ext))
    return file_list


# Get File Size
def get_file_size(file_path):
    return os.path.getsize(file_path)

# Get File Information (Size, Created, Modified, Accessed)
def get_file_info(file_path):
    file_info = {}
    if os.path.isdir(file_path):
        file_info['size'] = get_directory_size(file_path)
    if os.path.isfile(file_path):
        file_info['size'] = convert_file_size(get_file_size(file_path))
    file_info['created'] = time.ctime(os.path.getctime(file_path))
    file_info['modified'] = time.ctime(os.path.getmtime(file_path))
    file_info['accessed'] = time.ctime(os.path.getatime(file_path))
    return file_info

# Get File INFO To Text File
def get_file_info_to_text(file_path, output_file):
    file_info = get_file_info(file_path)
    with open(output_file, 'w') as f:
        f.write('Size: ' + file_info['size'] + '\n')
        f.write('Created: ' + file_info['created'] + '\n')
        f.write('Modified: ' + file_info['modified'] + '\n')
        f.write('Accessed: ' + file_info['accessed'] + '\n')
    
# Get File INFO To CSV File
def get_file_info_to_csv(file_path, output_file):
    file_info = get_file_info(file_path)
    with open(output_file, 'w', newline = '',encoding = 'utf-8') as file :
        

        f = csv.writer(file)
        
        # csv 파일에 header 추가
        f.writerow(['Size', 'Created', 'Modified', 'Accessed'])
        # print(file_info)
        f.writerow([file_info['size'], file_info['created'], file_info['modified'], file_info['accessed']])
        # for line in file_info['data']:
        #     f.writerow([line['en'],line['ko']])

# Get Directory Size
def get_directory_size(directory):
    path = Path(directory)
    total_size = 0
    for file in path.glob('**/*'):
        if file.is_file():
            total_size += file.stat().st_size
    # print(convert_file_size(total_size))
    return convert_file_size(total_size)

# Time to human readable format
def convert_time(time):
    print(time)
    # print(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
    # return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

# File size to human readable format
def convert_file_size(size):
    
    #  1 KB = 1024 Bytes
    #  1 MB = 1024 KB
    #  1 GB = 1024 MB
    #  1 TB = 1024 GB
    #  1 PB = 1024 TB
    
    if size < 1024:
        size = str(size) + 'B'
    elif size > 1024 and size < 1024 * 1024:
        size = str(round(size / 1024, 3)) + 'KB'
    elif size > 1024 * 1024 and size < 1024 * 1024 * 1024:
        size = str(round(size / 1024 / 1024, 3)) + 'MB'
    elif size > 1024 * 1024 * 1024 and size < 1024 * 1024 * 1024 * 1024:
        size = str(round(size / 1024 / 1024 / 1024, 3)) + 'GB'
    elif size > 1024 * 1024 * 1024 * 1024 and size < 1024 * 1024 * 1024 * 1024 * 1024:
        size = str(round(size / 1024 / 1024 / 1024 / 1024, 3)) + 'TB'
    else:
        size = str(round(size / 1024 / 1024 / 1024 / 1024 / 1024, 3)) + 'PB'
    return size

if __name__ == "__main__":
    path = r'P:\2403_A85\TY116\simulation\A85_TY116_ac3_C4_RIKA_left_test.ma'
    print(get_file_info(path))

