#######################################
# Project: IO_Vehicle_Detection Project
# Authors: Mateusz Smendowski, Piotr Sladowski, Adam Twardosz
# Copyright (C) Mateusz Smendowski, Piotr Sladowski, Adam Twardosz 2020
#######################################

import sys
import os 
import platform
import time
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QSize, Qt, QCoreApplication, QUrl
from PySide2.QtGui import QColor
from PySide2.QtWidgets import *

os.add_dll_directory(os.path.abspath("./dlls"))
import vlc

from gui.ui_main import Ui_MainWindow
from vehicle_detection import VideoProcessor
import gui.all_icons_rc


# GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
GLOBAL_TABS_ENABLED = True
TITLE = "Vehicle Detector"
VIDEO_PATH = ''
RESULTS = {}
PROCESS_TIME = 0
PROGRESS = 0.0
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW SETUP
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"VD Application", None))
        self.setWindowIcon(QtGui.QIcon(u":/icons/car_logo"))
        self.ui.titleLabel.setText(TITLE)
        self.removeTitleBar(True)

        # INITIAL SIZE SETTINGS
        startSize = QSize(800, 600)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        # CONSOLE OUTPUT TO CHECK PLATFORM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        # DISABLE TABS AT STARTUP
        self.toggle_tabs()

        # ----------- EVENT_FUNC ----------- #

        # WIDGET TO MOVE
        self.ui.titleBar.mouseMoveEvent = self.moveWindow

        # CHOOSE VIDEO FILE
        self.ui.btnChooseFolder.clicked.connect(self.choose_video)

        # COMBO BOX SETTINGS
        self.speed_settings = [ "YOLOv3-tiny (-90% acc, +800% spd)",
                                "YOLOv3-320 (-20% acc, +20% spd)",
                                "YOLOv4 <Default>",
                                "YOLOv3-608 (+10% acc, -50% spd)" 
                                ]
        self.state_combo()

        # PROCESS VIDEO FILE
        self.ui.btnProcess.clicked.connect(self.process_video)

        # PROGRESS BAR SETTINGS
        self.ui.progressBar.setRange(0, 1000)
        self.ui.progressBar.setValue(0)

        # UPDATING VIDEO SLIDER EVERY 200 ms
        self.videoTimer = QtCore.QTimer(self)
        self.videoTimer.setInterval(100)
        self.videoTimer.timeout.connect(self.update_media_info)

        # UPDATING TIME_LEFT EVERY 1 SEC WHEN PROCESSING
        self.processTimer = QtCore.QTimer(self)
        self.processTimer.setInterval(950)
        self.processTimer.timeout.connect(self.update_progress_time)

        self.progressTimer = QtCore.QTimer(self)
        self.progressTimer.setInterval(200)
        self.progressTimer.timeout.connect(self.update_progress_bar)

        # LOG BROWSER
        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # CALL THE REST OF THE FEATURES FOR MAIN WINDOW
        self.UIDefinitions()

        # SHOW MainWindow()
        self.show()
    # ~~~~~ END OF CONSTRUCTOR ~~~~~ #

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def state_combo(self):
        self.ui.cbSpeedAccur.addItems(self.speed_settings)
        self.ui.cbSpeedAccur.setCurrentIndex(2)

    def choose_video(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Video', os.path.join(os.path.expanduser('~')), "Video Files (*.mp4 *.mkv *.avi)")

        # SET lineEdit TO CHOSEN PATH
        self.ui.lineEdit.setText(fname[0])

    def process_video(self):
        global VIDEO_PATH, PROGRESS
        PROGRESS = 0.0
        if self.ui.lineEdit.text() != '':
            self.ui.btnProcess.setEnabled(False)
            self.ui.cbSpeedAccur.setEnabled(False)

            print("Processing video " + self.ui.lineEdit.text())
            VIDEO_PATH = self.ui.lineEdit.text()
            # setting speed and accuracy model for vehicle detection
            model = self.ui.cbSpeedAccur.currentIndex()

            self.processor = VideoProcessor(VIDEO_PATH, model)
            self.processor.on_data_finish.connect(self.on_processor_finish)
            self.processor.on_progress.connect(self.on_progress_func)
            self.processor.start()
            self.pTime = time.time()
            self.processTimer.start()
            self.progressTimer.start()
        else:
            print("No video selected")

    # AFTER VIDEO PROCESSING METHOD
    def on_processor_finish(self, output):
        self.pTime = time.time() - self.pTime
        print("Elapsed time: {}".format(self.pTime))
        print("FPS: {}".format(self.ui.progressBar.maximum() / self.pTime))

        global RESULTS, VIDEO_PATH
        RESULTS = output

        self.update_progress_bar()
        self.progressTimer.stop()
        self.processTimer.stop()
        self.setup_media_player()

        if RESULTS["done"]:
            print("Done processing, enabling postprocessing info!")
            if type(RESULTS["outVideo"]) == str and RESULTS["outVideo"] is not None:
                VIDEO_PATH = RESULTS["outVideo"]
                
                print("Processed video " + VIDEO_PATH)

                self.media = self.instance.media_new(VIDEO_PATH)
                self.mediaPlayer.set_media(self.media)
                self.media.parse()

                if platform.system() == "Linux": # for Linux using the X Server
                    self.mediaPlayer.set_xwindow(int(self.ui.frameMediaPlayer.winId()))
                elif platform.system() == "Windows": # for Windows
                    self.mediaPlayer.set_hwnd(int(self.ui.frameMediaPlayer.winId()))
                elif platform.system() == "Darwin": # for MacOS
                    self.mediaPlayer.set_nsobject(int(self.ui.frameMediaPlayer.winId()))

            if type(RESULTS["stats"]) == dict and RESULTS["stats"] is not None:
                self.print_statistics(RESULTS["stats"])

            if type(RESULTS["outLog"]) == str and RESULTS["outLog"] is not None:
                with open(RESULTS["outLog"], 'r') as f:
                    for line in f:
                        self.ui.textBrowser.appendPlainText(line)
                    f.close()

            self.toggle_tabs()
            self.ui.tabWidget.setCurrentIndex(1)
            self.play_video()

    def on_progress_func(self, prog):
        global PROGRESS
        PROGRESS = prog

    # PRINT STATISTICS TO STATS_TAB
    def print_statistics(self, stats):
        self.ui.labelTotalCountVar.setText(str(stats["total_vehicles"]))
        self.ui.labelNoPassVar.setText(str(stats["light_vehicles"]))
        self.ui.labelNoCgoVar.setText(str(stats["heavy_vehicles"]))
        self.ui.labelNoMotorVar.setText(str(stats["two_wheel_vehicles"]))
        self.ui.labelNoUnkVar.setText(str(stats["unknown_vehicles"]))

    # TABS TOGGLING
    def toggle_tabs(self):
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

    # UPDATE labelTimeLeft EVERY SECOND
    def update_progress_time(self):
        global PROCESS_TIME
        PROCESS_TIME += 1
        percent = self.ui.progressBar.value()/self.ui.progressBar.maximum() * 100
        if percent != 0:
            time_left = int(PROCESS_TIME * (100 - percent) / percent)
        else:
            time_left = 0
        self.print_time_lTL(time_left)

    def update_progress_bar(self):
        self.ui.progressBar.setValue(PROGRESS * 1000)

    def print_time_lTL(self, given_time):
        time_print = time.strftime('%H:%M:%S', time.gmtime(given_time))
        self.ui.labelTimeLeft.setText(time_print)

    # MEDIA CONTROL METHODS
    def setup_media_player(self):
        # MEDIA PLAYER
        self.instance = vlc.Instance()
        self.media = None
        self.mediaPlayer = self.instance.media_player_new()
        self.mediaPlayer.audio_set_mute(True)

        # MEDIA PLAYER HANDLING
        self.ui.btnPlay.clicked.connect(self.play_video)
        self.ui.btnStop.clicked.connect(self.stop_video)
        self.ui.hSliderVideo.setMaximum(1000)
        self.ui.hSliderVideo.setValue(0)
        self.ui.hSliderVideo.sliderMoved.connect(self.set_position)

    def play_video(self):
        global VIDEO_PATH
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.isPaused = True
            self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
            self.ui.labelVideoName.setText(VIDEO_PATH + ' [ paused ]')
        else:
            self.mediaPlayer.play()
            self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/pause"))
            self.ui.labelVideoName.setText(VIDEO_PATH)
            self.videoTimer.start()
            self.isPaused = False

    def stop_video(self):
        self.mediaPlayer.stop()
        self.ui.btnPlay.setIcon(QtGui.QIcon(u":/icons/play"))
        self.ui.labelVideoName.setText('')

    def update_media_info(self):
        self.print_time_vTL(self.mediaPlayer.get_time())
        self.ui.hSliderVideo.setValue(self.mediaPlayer.get_position() * 1000)

        if not self.mediaPlayer.is_playing():
            self.ui.hSliderVideo.setValue(1000)
            self.videoTimer.stop()
            if not self.isPaused:
                self.stop_video()

    def set_position(self, position):
        self.videoTimer.stop()
        self.mediaPlayer.set_position(position / 1000.0)
        self.videoTimer.start()

    def print_time_vTL(self, given_time):
        time_print = time.strftime('%M:%S', time.gmtime(int(round(given_time / 1000))))
        self.ui.videoTimeLabel.setText(time_print)

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
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
            self.ui.btnMaximize.setToolTip("Maximize")
            self.ui.btnMaximize.setIcon(QtGui.QIcon(u":/icons/max"))
            self.ui.titleLabel.setText(TITLE)

    # RETURN STATUS
    def returnStatus(self):
        return GLOBAL_STATE

    def removeTitleBar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

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
