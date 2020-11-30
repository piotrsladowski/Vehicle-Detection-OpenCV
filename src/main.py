#######################################
# Project: IO_Vehicle_Detection Project
# Authors: Mateusz Smendowski, Piotr Sladowski, Adam Twardosz
# Copyright (C) Mateusz Smendowski, Piotr Sladowski, Adam Twardosz 2020
#######################################

import sys
from os import path, environ
import platform
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QSize, Qt, QCoreApplication, QUrl, Slot
from PySide2.QtGui import QColor
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QGraphicsVideoItem
from PySide2.QtWidgets import *

from gui.ui_main import Ui_MainWindow
from vehicle_detection import VideoProcessor
import gui.all_icons_rc


# GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
GLOBAL_TABS_ENABLED = True
TITLE = "IO Vehicle Detection"
VIDEO_PATH = ''


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW SETUP
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"IO_VD Application", None))
        self.setWindowIcon(QtGui.QIcon(u":/icons/car_logo"))
        self.removeTitleBar(True)

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

        # MEDIA PLAYER
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoItem = QGraphicsVideoItem()

        self.videoScene = QGraphicsScene()
        self.ui.videoViewPlane.setScene(self.videoScene)
        self.ui.videoViewPlane.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.videoViewPlane.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.videoViewPlane.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.videoScene.addItem(self.videoItem)

        self.mediaPlayer.setVideoOutput(self.videoItem)
        
        # MEDIA PLAYER HANDLING
        self.ui.btnPlay.clicked.connect(self.playVideo)
        self.ui.btnStop.clicked.connect(self.stopVideo)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.ui.hSliderVideo.sliderMoved.connect(self.setPosition)

        # LOG BROWSER
        self.ui.textBrowser.setReadOnly(True)

        # CALL THE REST OF THE FEATURES FOR MAIN WINDOW
        self.UIDefinitions()

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

        fname = QFileDialog.getOpenFileName(self, 'Choose Video', path.join(environ[starting_directory], 'Videos'), "Video Files (*.mp4 *.mkv *.avi)")

        # SET lineEdit TO CHOSEN PATH
        self.ui.lineEdit.setText(fname[0])

    def processVideo(self):
        global VIDEO_PATH
        if self.ui.lineEdit.text() != '':
            self.ui.btnProcess.setEnabled(False)

            print("Processing video " + self.ui.lineEdit.text())
            VIDEO_PATH = self.ui.lineEdit.text()

            self.processor = VideoProcessor(self.ui.progressBar, VIDEO_PATH)
            self.processor.on_data_finish.connect(self.on_processor_finish)
            self.processor.start()
        else:
            print("No video selected")

    # AFTER VIDEO PROCESSING METHOD
    def on_processor_finish(self, output):
        """
        :param done:
        :param fvideo:
        :param flog:
        :param stats: dict("total_vehicles": int, "light_vehicles": int, "heavy_vehicles": int, "two_wheel_vehicles": int, "unknown_vehicles": int)
        """

        if output["done"]:
            print("Done processing, enabling postprocessing info!")
            self.toggleTabs()

            if type(output["outVideo"]) == str and output["outVideo"] is not None:
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(output["outVideo"])))
                self.mediaPlayer.setMuted(True)

            if type(output["outLog"]) == str and output["outLog"] is not None:
                with open(output["outLog"], 'r') as f:
                    for line in f:
                        self.ui.textBrowser.appendPlainText(line)
                    f.close()

            self.ui.videoViewPlane.show()
            self.fitVideoToGView(0.98)

            if type(output["stats"]) == dict and output["stats"] is not None:
                self.printStatistics(output["stats"])

    # PRINT STATISTICS TO STATS_TAB
    def printStatistics(self, stats):
        self.ui.labelTotalCountVar.setText(str(stats["total_vehicles"]))
        self.ui.labelNoPassVar.setText(str(stats["light_vehicles"]))
        self.ui.labelNoCgoVar.setText(str(stats["light_vehicles"]))
        self.ui.labelNoMotorVar.setText(str(stats["light_vehicles"]))
        self.ui.labelNoUnkVar.setText(str(stats["light_vehicles"]))

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
    def playVideo(self):
        global VIDEO_PATH
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
            self.ui.labelVideoName.setText(VIDEO_PATH + ' [ paused ]')
        else:
            self.mediaPlayer.play()
            self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/pause"))
            self.ui.labelVideoName.setText(VIDEO_PATH)

    def stopVideo(self):
        self.mediaPlayer.stop()
        self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
        self.ui.labelVideoName.setText('')

    def positionChanged(self, position):
        self.ui.hSliderVideo.setValue(position)

    def durationChanged(self, duration):
        self.ui.hSliderVideo.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    # ALLOW WINDOW TO MOVE ON THE SCREEN
    def moveWindow(self, event):
        # IF MAXIMIZED CHANGE TO NORMAL
        if self.returnStatus == 1:
            self.maximizeOrRestore()
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    # MAXIMIZE/RESTORE
    def maximizeOrRestore(self):
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
            self.fitVideoToGView(0.99)
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
            self.ui.btnMaximize.setToolTip("Maximize")
            self.ui.btnMaximize.setIcon(QtGui.QIcon(u":/icons/max"))
            self.ui.titleLabel.setText(TITLE)
            self.fitVideoToGView(0.9)

    # RETURN STATUS
    def returnStatus(self):
        return GLOBAL_STATE

    def removeTitleBar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def fitVideoToGView(self, scale):
        vSize = self.ui.videoViewPlane.size()
        nH = vSize.height()*scale
        nW = nH/9*16
        self.videoItem.setSize(QSize(nW, nH))
        self.ui.videoViewPlane.centerOn(0, 0)

    def UIDefinitions(self):
        def doubleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: self.maximizeOrRestore())

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
        self.ui.btnMaximize.clicked.connect(lambda: self.maximizeOrRestore())

        # CLOSE APPLICATION
        self.ui.btnClose.clicked.connect(lambda: self.close())


# ----------- MAIN_FUNC ----------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
