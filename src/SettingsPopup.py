import sys
import os
import string
from random import *
import base64
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, QVBoxLayout,
    QHBoxLayout, QHeaderView, QLabel, QTreeView, QTreeWidget, QTreeWidgetItem,
    QToolBar, QLineEdit, QCheckBox, QCompleter, QSpacerItem, QSizePolicy,
    QComboBox, QMessageBox, QDialog, QDialogButtonBox, QFileSystemModel,
    QDirModel, QFileDialog)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt, QModelIndex
import sqlite3
from sqlite3 import Error

from ConfigureIO import *

class General(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initVariables()

    def initUI(self):
        mainlayout = QVBoxLayout()
        formlayout = QFormLayout()

        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        recentLabel = QLabel("Definition of recent")
        self.recentComboBox = QComboBox(self)
        periodItemList = ["1 day", "3 days", "1 week", "1 month", "3 months", "6 months", "1 year"]
        self.recentComboBox.addItems(periodItemList)
        self.recentComboBox.currentIndexChanged.connect(self.recentChanged)
        formlayout.addRow(recentLabel, self.recentComboBox)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)
        self.applyButton.clicked.connect(self.apply)
        self.applyButton.setEnabled(False)

        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        mainlayout.addLayout(formlayout)
        mainlayout.addWidget(vspacer)
        mainlayout.addLayout(buttonLayout)
        self.setLayout(mainlayout)

    def initVariables(self):
        settings = readSettingItems(['General'])
        if 'General' in settings.keys():
            if 'Recent' in settings['General'].keys():
                self.recent = settings['General']['Recent']
                self.recentComboBox.setCurrentIndex(self.recent)
            else:
                self.recent = 0
                self.recentComboBox.setCurrentIndex(self.recent)

    def apply(self):
        data = {'General': {'Recent': self.recent}}
        writeSettingItems(data)
        self.applyButton.setEnabled(False)

    def recentChanged(self, item):
        if self.recent != item:
            self.recent = item
            self.applyButton.setEnabled(True)

class Account(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initVariables()

    def initUI(self):
        mainlayout = QFormLayout()
        usernameLabel = QLabel("Username/Email")
        self.usernameLineEdit = QLineEdit(self)
        passwordLabel = QLabel("Password")
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        showingPasswordLabel = QLabel("Show Password")
        self.showPasswordCheckBox = QCheckBox(self)

        buttonLayout = QHBoxLayout()
        self.loginButton = QPushButton("Login", self)
        self.loginButton.clicked.connect(self.loginout)
        #self.logoutButton = QPushButton("Logout", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.loginButton)
        #buttonLayout.addWidget(self.logoutButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainlayout.addRow(usernameLabel, self.usernameLineEdit)
        mainlayout.addRow(passwordLabel, self.passwordLineEdit)
        mainlayout.addRow(showingPasswordLabel, self.showPasswordCheckBox)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

    def initVariables(self):
        settings = readSettingItems(['Account'])
        if 'Account' in settings.keys():
            if 'Username' in settings['Account'].keys():
                self.username = settings['Account']['Username']
                self.usernameLineEdit.setText(self.username)
            else:
                self.username = ""
                self.username.setText(self.username)
            if 'Password' in settings['Account'].keys():
                self.password = settings['Account']['Password']
                self.passwordLineEdit.setText(self.password)
            else:
                self.password = ""
                self.passwordLineEdit.setText(self.password)
            self.showPasswordCheckBox.setCheckState(0)
            self.checkLogin()

    def loginout(self):
        if self.loginButton.text() == "Login":
            self.loginButton.setText("Logout")
            self.usernameLineEdit.setEnabled(False)
            self.passwordLineEdit.setEnabled(False)
        elif self.loginButton.text() == "Logout":
            self.loginButton.setText("Login")
            self.usernameLineEdit.setEnabled(True)
            self.passwordLineEdit.setEnabled(True)
            self.usernameLineEdit.setText("")
            self.passwordLineEdit.setText("")

    def checkLogin(self):
        if len(self.username)*len(self.password):
            self.loginButton.setText("Logout")
            self.usernameLineEdit.setEnabled(False)
            self.passwordLineEdit.setEnabled(False)

class Organizer(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initVariables()

    def initUI(self):
        mainlayout = QFormLayout()
        # Add elements
        self.organizeFileCheckBox = QCheckBox(self)
        self.organizeFileCheckBox.stateChanged.connect(self.organizeStateChanged)
        organizeFileLabel = QLabel("Organize my files")

        copyFileLayout = QHBoxLayout()
        copyFileLabel = QLabel("    Copy files to")
        self.copyFileLineEdit = QLineEdit(self)
        self.copyFileButton = QPushButton("Browse...")
        self.copyFileButton.clicked.connect(self.copyFileBrowse)
        copyFileLayout.addWidget(copyFileLabel)
        copyFileLayout.addWidget(self.copyFileLineEdit)
        copyFileLayout.addWidget(self.copyFileButton)

        self.sortFileCheckBox = QCheckBox(self)
        self.sortFileCheckBox.stateChanged.connect(self.sortStateChanged)
        sortFileLabel = QLabel("Sort files into subdirectories")
        self.renameFileCheckBox = QCheckBox(self)
        self.renameFileCheckBox.stateChanged.connect(self.renameStateChanged)
        renameFileLabel = QLabel("Rename files")
        # Buttons
        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.resetButton = QPushButton("Reset", self)
        self.applyButton.clicked.connect(self.apply)
        self.applyButton.setEnabled(False)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        # Add to layout
        mainlayout.addRow(self.organizeFileCheckBox, organizeFileLabel)
        mainlayout.addRow(copyFileLayout)
        mainlayout.addRow(self.sortFileCheckBox, sortFileLabel)
        mainlayout.addRow(self.renameFileCheckBox, renameFileLabel)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

    def initVariables(self):
        settings = readSettingItems(['Organizer'])
        if 'Organizer' in settings.keys():
            if 'Organize' in settings['Organizer'].keys():
                self.organize = settings['Organizer']['Organize']
                self.organizeFileCheckBox.setCheckState(self.organize)
            else:
                self.organize = 0
                self.organizeFileCheckBox.setCheckState(self.organize)
            if 'Path' in settings['Organizer'].keys():
                self.chosenDir = settings['Organizer']['Path']
                self.copyFileLineEdit.setText(self.chosenDir)
            else:
                self.chosenDir = ""
                self.copyFileLineEdit.setText(self.chosenDir)
            if 'Sort' in settings['Organizer'].keys():
                self.sort = settings['Organizer']['Sort']
                self.sortFileCheckBox.setCheckState(self.sort)
            else:
                self.sort = 0
                self.sortFileCheckBox.setCheckState(self.sort)
            if 'Rename' in settings['Organizer'].keys():
                self.rename = settings['Organizer']['Rename']
                self.renameFileCheckBox.setCheckState(self.rename)
            else:
                self.rename = 0
                self.renameFileCheckBox.setCheckState(self.rename)

    def organizeStateChanged(self, state):
        if self.organize != state:
            self.organize = state
            self.applyButton.setEnabled(True)

    def sortStateChanged(self, state):
        if self.sort != state:
            self.sort = state
            self.applyButton.setEnabled(True)

    def renameStateChanged(self, state):
        if self.rename != state:
            self.rename = state
            self.applyButton.setEnabled(True)

    def copyFileBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        newChosenDir = dlg.getExistingDirectory()
        if self.chosenDir != newChosenDir:
            self.chosenDir = newChosenDir
            self.copyFileLineEdit.setText(self.chosenDir)
            self.applyButton.setEnabled(True)

    def apply(self):
        data = {'Organizer': {'Organize': self.organize,
                              'Path': self.chosenDir,
                              'Sort': self.sort,
                              'Rename': self.rename}
               }
        writeSettingItems(data)
        self.applyButton.setEnabled(False)

class CheckableDirModel(QDirModel):
    updateCheckBoxSignal = pyqtSignal([QModelIndex, int])
    def __init__(self, parent=None):
        QDirModel.__init__(self, None)
        self.checks = {}

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.CheckStateRole:
            return QDirModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable

    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return Qt.Unchecked

    def setData(self, index, value, role):
        if (role == Qt.CheckStateRole and index.column() == 0):
            self.checks[index] = value
            self.updateCheckBoxSignal.emit(index, value)
            return True

        return QDirModel.setData(self, index, value, role)

class Watch(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initVariables()

    def initUI(self):
        mainlayout = QFormLayout()
        self.model = CheckableDirModel()
        #self.model = QFileSystemModel()

        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setSortingEnabled(False)
        self.tree.setHeaderHidden(True)
        self.model.updateCheckBoxSignal.connect(self.updateCheckBoxes)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.apply)
        self.applyButton.setEnabled(False)
        self.resetButton = QPushButton("Reset", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Add to layout
        mainlayout.addRow(self.tree)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

    def initVariables(self):
        settings = readSettingItems(['Watched'])
        if 'Watched' in settings.keys():
            if len(settings['Watched']):
                self.watchList = settings['Watched']
                if len(self.watchList):
                    for watchItem in self.watchList:
                        tempPath = watchItem[0]
                        tempIndex = self.model.index(tempPath, 0)
                        retData = self.model.filePath(tempIndex)
                        # Set checkbox
                        if len(retData):
                            self.model.setData(tempIndex, watchItem[1], Qt.CheckStateRole)
                            # Expand path
                            while tempIndex.parent().isValid():
                                tempIndex = tempIndex.parent()
                                self.tree.expand(tempIndex)

            else:
                self.watchList = []

    def updateCheckBoxes(self, index, value):
        changeFlag = False
        fullpath = self.model.filePath(index)
        newWatchMission = [fullpath, value]
        if newWatchMission in self.watchList:
            pass
        else:
            if len(self.watchList):
                tempList = list(filter(lambda x: fullpath in x, self.watchList))
                if len(tempList) == 1:
                    tempMissionIndex = self.watchList.index(tempList[0])
                    if value == 0:
                        self.watchList.pop(tempMissionIndex)
                    else:
                        self.watchList[tempMissionIndex] = newWatchMission
                elif len(tempList) == 0:
                    if value != 0:
                        self.watchList.append(newWatchMission)
                changeFlag = True
        self.applyButton.setEnabled(changeFlag)
        # to do: update checkboxes states: 0, 1, 2.

    def apply(self):
        data = {'Watched': self.watchList }
        writeSettingItems(data)
        self.applyButton.setEnabled(False)

class Proxy(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()
        self.initVariables()

    def initUI(self):
        mainlayout = QFormLayout()
        # Create widget elements
        proxytypeLabel = QLabel("Proxy type")
        self.proxytypeComboBox = QComboBox(self)
        proxyTypeItemList = ["No Proxy", "HTTP Proxy", "SOCKS 5 Proxy"]
        self.proxytypeComboBox.addItems(proxyTypeItemList)
        self.proxytypeComboBox.currentIndexChanged.connect(self.proxyTypeChanged)
        serverLabel = QLabel("Server")
        self.serverLineEdit = QLineEdit(self)
        self.serverLineEdit.textChanged.connect(self.serverTextChanged)
        portLabel = QLabel("Port")
        self.portLineEdit = QLineEdit(self)
        self.portLineEdit.textChanged.connect(self.portTextChanged)
        usernameLabel = QLabel("Username (if required)")
        self.usernameLineEdit = QLineEdit(self)
        self.usernameLineEdit.textChanged.connect(self.usernameTextChanged)
        passwordLabel = QLabel("Password (if required)")
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.textChanged.connect(self.passwordTextChanged)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.apply)
        self.applyButton.setEnabled(False)
        self.resetButton = QPushButton("Reset", self)
        hspacer = QWidget()
        hspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.addWidget(hspacer)
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.resetButton)

        vspacer = QWidget()
        vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Add to layout
        mainlayout.addRow(proxytypeLabel, self.proxytypeComboBox)
        mainlayout.addRow(serverLabel, self.serverLineEdit)
        mainlayout.addRow(portLabel, self.portLineEdit)
        mainlayout.addRow(usernameLabel, self.usernameLineEdit)
        mainlayout.addRow(passwordLabel, self.passwordLineEdit)
        mainlayout.addRow(vspacer)
        mainlayout.addRow(buttonLayout)
        self.setLayout(mainlayout)

    def initVariables(self):
        settings = readSettingItems(['Proxy'])
        if 'Proxy' in settings.keys():
            # Proxy Type
            if 'Type' in settings['Proxy'].keys():
                self.proxytype = settings['Proxy']['Type']
                self.proxytypeComboBox.setCurrentIndex(self.proxytype)
            else:
                self.proxytype = 0
                self.proxytypeComboBox.setCurrentIndex(self.proxytype)
            # Server
            if 'Server' in settings['Proxy'].keys():
                self.server = settings['Proxy']['Server']
                self.serverLineEdit.setText(self.server)
            else:
                self.server = ""
                self.serverLineEdit.setText(self.server)
            # Port
            if 'Port' in settings['Proxy'].keys():
                self.port = settings['Proxy']['Port']
                self.portLineEdit.setText(str(self.port))
            else:
                self.port = 0
                self.portLineEdit.setText(str(self.port))
            # Username
            if 'Username' in settings['Proxy'].keys():
                self.username = settings['Proxy']['Username']
                self.usernameLineEdit.setText(self.username)
            else:
                self.username = ""
                self.usernameLineEdit.setText(self.username)
            # Password
            if 'Password' in settings['Proxy'].keys():
                self.password = settings['Proxy']['Password']
                self.passwordLineEdit.setText(self.password)
            else:
                self.password = ""
                self.passwordLineEdit.setText(self.password)

    def proxyTypeChanged(self, item):
        if self.proxytype != item:
            self.proxytype = item
            self.applyButton.setEnabled(True)

    def serverTextChanged(self, item):
        if item != self.server:
            self.server = item
            self.applyButton.setEnabled(True)

    def portTextChanged(self, item):
        itemNum = 0
        if len(item):
            itemNum = int(item)
        if itemNum != self.port:
            self.port = itemNum
            self.applyButton.setEnabled(True)

    def usernameTextChanged(self, item):
        if item != self.username:
            self.username = item
            self.applyButton.setEnabled(True)

    def passwordTextChanged(self, item):
        if item != self.password:
            self.password = item
            self.applyButton.setEnabled(True)

    def apply(self):
        data = {'Proxy': {'Type': self.proxytype,
                          'Server': self.server,
                          'Port': self.port,
                          'Username': self.username,
                          'Password': self.password}}
        writeSettingItems(data)
        self.applyButton.setEnabled(False)

class SettingsPopup(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.initUI()

    def initUI(self):
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 360
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        #self.layout = QHBoxLayout()
        #self.layout.setSpacing(0)
        #self.layout.setContentsMargins(0,0,0,0)
        self.settingTopicList = QListWidget(self)
        self.settingTopicList.setStyleSheet("max-width: 200px; max-height: 350; font-size: 15pt")
        self.settingTopicList.setGeometry(self.width/15, self.height/15, self.width*4/15, self.height*13/15)  # left, top, width, height
        listItems = ["General", "Account", "Organizer", "Watched Directories", "Proxy"]
        self.settingTopicList.addItems(listItems)
        self.settingTopicList.item(0).setSelected(True)
        itemWidth = self.settingTopicList.item(0).sizeHint().width()
        itemHeight = 50
        for i in range(len(listItems)):
            self.settingTopicList.item(i).setSizeHint(QSize(itemWidth, itemHeight))
        self.settingTopicList.itemClicked.connect(self.subpageChosen)
        self.initSubpages()
        self.loadSubpage(listItems[0])

    def centerWindow(self):
        frameGeo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def paintEvent(self, e):
        pass

    def closeEvent(self, event):
        # Also write unsaved settings to config file (?), to do.
        print("Closed from dialog")

    def initSubpages(self):
        self.generalPage = General(self)
        self.generalPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.accountPage = Account(self)
        self.accountPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.organizerPage = Organizer(self)
        self.organizerPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.watchPage = Watch(self)
        self.watchPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.proxyPage = Proxy(self)
        self.proxyPage.setGeometry(self.width*5.5/15, self.height/15, self.width*8.5/15, self.height*13/15)
        self.hideSubpages()


    def hideSubpages(self):
        self.generalPage.hide()
        self.accountPage.hide()
        self.organizerPage.hide()
        self.watchPage.hide()
        self.proxyPage.hide()

    def subpageChosen(self, item):
        self.hideSubpages()
        self.loadSubpage(item.text())

    def loadSubpage(self, pageName):
        if pageName == "General":
            self.loadGeneral()
        elif pageName == "Account":
            self.loadAccount()
        elif pageName == "Organizer":
            self.loadOrganizer()
        elif pageName == "Watched Directories":
            self.loadWatch()
        elif pageName == "Proxy":
            self.loadProxy()

    def loadGeneral(self):
        self.generalPage.show()

    def loadAccount(self):
        self.accountPage.show()

    def loadOrganizer(self):
        self.organizerPage.show()

    def loadWatch(self):
        self.watchPage.show()

    def loadProxy(self):
        self.proxyPage.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = SettingsPopup()
    screen.show()
    sys.exit(app.exec_())
