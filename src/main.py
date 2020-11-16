#!/usr/bin/env python
#######################################
# Project: IO_Vehicle_Detection Project
# Authors: Mateusz Smendowski, Piotr Sladowski, Adam Twardosz
# Copyright (C) Mateusz Smendowski, Piotr Sladowski, Adam Twardosz 2020
#######################################

import sys
import os
import platform
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QSize, Qt, QCoreApplication, QUrl
from PySide2.QtGui import QColor
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtWidgets import *

from gui.ui_main import Ui_MainWindow
import gui.all_icons_rc


# GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
GLOBAL_TABS_ENABLED = True
TITLE = "IO Vehicle Detection"
VIDEO_PROCESSED = False
VIDEO_PATH = ''

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW SETUP
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"IO_VD Application", None))
        self.setWindowIcon(QtGui.QIcon(u":/icons/car_logo"))
        self.remove_title_bar(True)

        # INITIAL SIZE SETTINGS
        startSize = QSize(800, 600)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        # CONSOLE OUTPUT TO CHECK PLATFORM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        # DISABLE TABS AT STARTUP
        self.toggleTabs()

        # ----------- EVENT_FUNC ----------- #

        # WIDGET TO MOVE
        self.ui.titleBar.mouseMoveEvent = self.moveWindow

        # CHOOSE VIDEO FILE
        self.ui.btnChooseFolder.clicked.connect(self.chooseVideo)

        # PROCESS VIDEO FILE
        self.ui.btnProcess.clicked.connect(self.processVideo)

        # MEDIA PLAYER NOTES
        # TODO: Use QGraphicsVideoItem instead of QVideoWidget

        # MEDIA PLAYER HANDLING
        # self.ui.btnPlay.clicked.connect(self.play_video)
        # self.ui.btnStop.clicked.connect(self.stop_video)
        # self.ui.mediaPlayer.positionChanged.connect(self.position_changed)
        # self.ui.mediaPlayer.durationChanged.connect(self.duration_changed)

        # CALL THE REST OF THE FEATURES FOR MAIN WINDOW
        self.ui_definitions()

        # SHOW MainWindow()
        self.show()
    # ~~~~~ END OF CONSTRUCTOR ~~~~~ #

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def chooseVideo(self):
        starting_directory = ''
        if platform.system() == "Windows":
            starting_directory = 'USERPROFILE'
        else:
            starting_directory = 'HOME'

        fname = QFileDialog.getOpenFileName(self, 'Open Video', os.path.join(os.environ[starting_directory], 'Videos'), "Video Files (*.mp4 *.mkv *.avi)")

        # SET lineEdit TO CHOSEN PATH
        self.ui.lineEdit.setText(fname[0])

    def processVideo(self):
        global VIDEO_PATH
        if self.ui.lineEdit.text() != '':
            print("Processing video " + self.ui.lineEdit.text())
            VIDEO_PATH = self.ui.lineEdit.text()
            # TODO: func.processVideo specify function where the Video_file is processed
            # TODO: func.processVideo update progressBar whit percent

            self.whenProcessed(self.ui.lineEdit.text())

    def whenProcessed(self, filename):
        global VIDEO_PROCESSED
        if not VIDEO_PROCESSED:
            self.toggleTabs()
            VIDEO_PROCESSED = True

        # if filename != '':
        #     self.ui.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        #     # self.ui.mediaPlayer.setMuted(True)
        #
        if os.path.exists('./example.log'):
            self.ui.textBrowser.setSource(QUrl.fromLocalFile(os.path.abspath('./example.log')))

    # TABS TOGGLING
    def toggleTabs(self):
        global GLOBAL_TABS_ENABLED
        areEnabled = GLOBAL_TABS_ENABLED
        if areEnabled:
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setTabEnabled(2, False)
            self.ui.tabWidget.setTabEnabled(3, False)
            GLOBAL_TABS_ENABLED = False
        else:
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setTabEnabled(3, True)
            GLOBAL_TABS_ENABLED = True

    # MEDIA CONTROL METHODS
    # def play_video(self):
    #     if self.ui.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.ui.mediaPlayer.pause()
    #         self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/pause"))
    #         # text = self.ui.mediaPlayer.media(self).canonicalUrl().fileName()
    #         # self.ui.labelVideoName.setText(text + ' [ paused ]')
    #     else:
    #         self.ui.mediaPlayer.play()
    #         self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
    #         # self.ui.labelVideoName.setText(self.ui.mediaPlayer.media().canonicalUrl().fileName())
    #
    # def stop_video(self):
    #     self.ui.mediaPlayer.stop()
    #     self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
    #     self.ui.labelVideoName.setText('')
    #
    # def position_changed(self, position):
    #     self.ui.hSliderVideo.setValue(position)
    #
    # def duration_changed(self, duration):
    #     self.ui.hSliderVideo.setRange(0, duration)
    #
    # def set_position(self, position):
    #     self.ui.mediaPlayer.setPosition(position)

    # ALLOW WINDOW TO MOVE ON THE SCREEN
    def moveWindow(self, event):
        # IF MAXIMIZED CHANGE TO NORMAL
        if self.return_status == 1:
            self.maximize_restore()
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    # MAXIMIZE/RESTORE
    def maximize_restore(self):
        global GLOBAL_STATE
        global TITLE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.drop_shadow_layout.setContentsMargins(0, 0, 0, 0)
            self.ui.btnMaximize.setToolTip("Restore")
            self.ui.btnMaximize.setIcon(QtGui.QIcon(u":/icons/res"))
            self.ui.titleLabel.setText("")
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
            self.ui.btnMaximize.setToolTip("Maximize")
            self.ui.btnMaximize.setIcon(QtGui.QIcon(u":/icons/max"))
            self.ui.titleLabel.setText(TITLE)

    # RETURN STATUS
    def return_status(self):
        return GLOBAL_STATE

    def remove_title_bar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def ui_definitions(self):
        def doubleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: self.maximize_restore())

        # STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.titleBar.mouseDoubleClickEvent = doubleClickMaximizeRestore
        else:
            self.ui.btnsFrame.setContentsMargins(8, 0, 0, 5)
            self.ui.btnsFrame.setMinimumHeight(35)

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # MINIMIZE
        self.ui.btnMinimize.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.btnMaximize.clicked.connect(lambda: self.maximize_restore())

        # CLOSE APPLICATION
        self.ui.btnClose.clicked.connect(lambda: self.close())


# ----------- MAIN_FUNC ----------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
