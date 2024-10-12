# -*- encoding: utf-8 -*-

# Desc: Tools for the FM project
# Date: 2024-10-12
# Auth: JC OH
# Ver: 1.0.0


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


import os  
import sys
import shutil
import time
import datetime
import logging
import logging.handlers
import re
import json
import FM_Utils


logger = FM_Utils.set_logger('FM_Tools.log', logging.INFO)
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

# File Manager UI
class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('File Manager')
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout()
        self.mainSplitter = QSplitter(Qt.Horizontal)
        mainLayout.addWidget(self.mainSplitter)
        mainWidget.setLayout(mainLayout)
        
        topLayout = QHBoxLayout()
        self.pathLabel = QLabel('Directory: ')
        self.pathEdit = QLineEdit()
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setPlaceholderText('Select Directory')
        self.browserButton = QPushButton('Browser')
        self.browserButton.clicked.connect(self.browse_folder)       
        
        topSplitter  = QSplitter(Qt.Horizontal)
        topSplitter.addWidget(self.pathLabel)
        topSplitter.addWidget(self.pathEdit)
        topSplitter.addWidget(self.browserButton)
        topLayout.addWidget(topSplitter)
        mainLayout.addLayout(topLayout)
        
        midLayout = QVBoxLayout()
        # File Tree View
        self.fileTree = QTreeView()
        # Extension selection
        self.fileTree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # fileTree right-click menu
        self.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTree.customContextMenuRequested.connect(self.fileTreeMenu)
                
        midLayout.addWidget(self.fileTree)
        # self.mainSplitter.addWidget(self.fileTree)
        mainLayout.addLayout(midLayout)
        
        bottomLayout = QHBoxLayout()
    
    def fileTreeMenu(self, pos):
        menu = QMenu()
        
        getFileSizeAct = menu.addAction('Get File Size')

        if len(self.fileTree.selectedIndexes()) > 0:
            getFileSizeAct.triggered.connect(self.get_file_size)
        # openAction.triggered.connect(self.open_file)
        # deleteAction = menu.addAction('Delete')
        # deleteAction.triggered.connect(self.delete_file)
        # infoAction = menu.addAction('Info')
        # infoAction.triggered.connect(self.file_info)
        menu.exec_(self.fileTree.mapToGlobal(pos))
        
    def init_model(self):
        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath('')
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(self.fileModel.index(self.pathEdit.text()))
        self.fileTree.setColumnWidth(0, 250)
        self.fileTree.setColumnWidth(1, 100)
        self.fileTree.setColumnWidth(2, 100)
        self.fileTree.setColumnWidth(3, 100)
        
        # self.fileModel.setRootPath(self.pathEdit.text())
        
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.pathEdit.setText(folder)
            self.init_model()
            self.fileModel.setRootPath(folder)

    def get_file_size(self):
        indexes = self.fileTree.selectedIndexes()
        for index in indexes:
            file_path = self.fileModel.filePath(index)
            size = ''
            csvFile = ''
            size = FM_Utils.get_file_size(file_path)
            if os.path.isfile(file_path):
                csvFile = os.path.splitext(file_path)[0] + '_size.csv'
            elif os.path.isdir(file_path):
                # size = FM_Utils.get_directory_size(file_path)
                csvFile = file_path + '_size.csv'
            # if os.path.isfile(file_path):
            #     print('File')
            #     size = FM_Utils.get_file_size(file_path)
            #     # log_info(logger, 'File Size: ' + str(size))
            #     csvFile = os.path.splitext(file_path)[0] + '_size.csv'
            # elif os.path.isdir(file_path):
            #     print('Directory')
            #     print(file_path)
            #     size = FM_Utils.get_directory_size(file_path)
            #     # log_info(logger, 'Directory Size: ' + str(size))
            #     csvFile = file_path + '_size.csv'
            # QMessageBox.information(self, 'File Size', 'Size: ' + size)
            FM_Utils.get_file_info_to_csv(file_path, csvFile)
                
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManager()
    ex.show()
    sys.exit(app.exec_())
    # sys.exit(1)
