# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.drop_shadow_layout = QVBoxLayout(self.centralwidget)
        self.drop_shadow_layout.setSpacing(0)
        self.drop_shadow_layout.setObjectName(u"drop_shadow_layout")
        self.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"background-color: rgb(44, 53, 72);")
        self.dropShadowFrame.setFrameShape(QFrame.NoFrame)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.dropShadowFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.titleBar = QFrame(self.dropShadowFrame)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setMinimumSize(QSize(0, 35))
        self.titleBar.setMaximumSize(QSize(16777215, 35))
        self.titleBar.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.titleBar.setFrameShape(QFrame.NoFrame)
        self.titleBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.titleBar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.titleFrame = QFrame(self.titleBar)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setFrameShape(QFrame.StyledPanel)
        self.titleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.titleFrame)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 5, 0)
        self.titleIcon = QLabel(self.titleFrame)
        self.titleIcon.setObjectName(u"titleIcon")
        self.titleIcon.setMinimumSize(QSize(35, 35))
        self.titleIcon.setMaximumSize(QSize(35, 35))
        self.titleIcon.setPixmap(QPixmap(u":/icons/car_logo"))
        self.titleIcon.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.titleIcon)

        self.titleLabel = QLabel(self.titleFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"color: white;")

        self.horizontalLayout_2.addWidget(self.titleLabel)

        self.titleLabel.raise_()
        self.titleIcon.raise_()

        self.horizontalLayout.addWidget(self.titleFrame)

        self.btnsFrame = QFrame(self.titleBar)
        self.btnsFrame.setObjectName(u"btnsFrame")
        self.btnsFrame.setMaximumSize(QSize(120, 16777215))
        self.btnsFrame.setFrameShape(QFrame.NoFrame)
        self.btnsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.btnsFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btnMinimize = QPushButton(self.btnsFrame)
        self.btnMinimize.setObjectName(u"btnMinimize")
        self.btnMinimize.setMinimumSize(QSize(35, 35))
        self.btnMinimize.setLayoutDirection(Qt.LeftToRight)
        self.btnMinimize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:  rgb(35, 40, 49);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/min", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMinimize.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.btnMinimize)

        self.btnMaximize = QPushButton(self.btnsFrame)
        self.btnMaximize.setObjectName(u"btnMaximize")
        self.btnMaximize.setMinimumSize(QSize(35, 35))
        self.btnMaximize.setLayoutDirection(Qt.LeftToRight)
        self.btnMaximize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:  rgb(35, 40, 49);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/max", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMaximize.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.btnMaximize)

        self.btnClose = QPushButton(self.btnsFrame)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setMinimumSize(QSize(35, 35))
        self.btnClose.setLayoutDirection(Qt.LeftToRight)
        self.btnClose.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(35, 40, 49);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/x", QSize(), QIcon.Normal, QIcon.Off)
        self.btnClose.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.btnClose)

        self.btnMaximize.raise_()
        self.btnClose.raise_()
        self.btnMinimize.raise_()

        self.horizontalLayout.addWidget(self.btnsFrame)


        self.verticalLayout.addWidget(self.titleBar)

        self.tabWidget = QTabWidget(self.dropShadowFrame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(12)
        self.tabWidget.setFont(font1)
        self.tabWidget.setCursor(QCursor(Qt.ArrowCursor))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"QTabWidget::pane { \n"
"	border: 0; \n"
"}\n"
"QTabBar::tab {\n"
"	padding: 2px;\n"
"	width: 186.5%;\n"
"	\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"	border-bottom-color: rgb(44, 53, 72);\n"
"	border-top-left-radius: 5px;\n"
"	border-top-right-radius: 5px;\n"
"	\n"
"	background-color: rgb(35, 40, 49);		\n"
"	color: white;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {	\n"
"	background-color: rgb(44, 53, 72);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"	margin-top: 2px;\n"
"}")
        self.tabInput = QWidget()
        self.tabInput.setObjectName(u"tabInput")
        self.tabInput.setMinimumSize(QSize(100, 0))
        font2 = QFont()
        font2.setFamily(u"Roboto")
        font2.setPointSize(10)
        self.tabInput.setFont(font2)
        self.tabInput.setStyleSheet(u"border: 2px solid rgb(44, 53, 72);")
        self.verticalLayout_2 = QVBoxLayout(self.tabInput)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frameChooseFile = QFrame(self.tabInput)
        self.frameChooseFile.setObjectName(u"frameChooseFile")
        self.frameChooseFile.setFrameShape(QFrame.StyledPanel)
        self.frameChooseFile.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frameChooseFile)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 20, 10, 20)
        self.lineEdit = QLineEdit(self.frameChooseFile)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        font3 = QFont()
        font3.setFamily(u"MS Shell Dlg 2")
        font3.setPointSize(10)
        self.lineEdit.setFont(font3)
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"	color: white;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.lineEdit.setFrame(True)

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.btnChooseFolder = QPushButton(self.frameChooseFile)
        self.btnChooseFolder.setObjectName(u"btnChooseFolder")
        self.btnChooseFolder.setMinimumSize(QSize(150, 30))
        self.btnChooseFolder.setFont(font2)
        self.btnChooseFolder.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: white;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/folder_open", QSize(), QIcon.Normal, QIcon.Off)
        self.btnChooseFolder.setIcon(icon3)

        self.gridLayout.addWidget(self.btnChooseFolder, 1, 1, 1, 1)

        self.frameSpacer1 = QFrame(self.frameChooseFile)
        self.frameSpacer1.setObjectName(u"frameSpacer1")
        self.frameSpacer1.setFrameShape(QFrame.StyledPanel)
        self.frameSpacer1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frameSpacer1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.frameSpacer1)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)
        self.label.setStyleSheet(u"color: white;\n"
"")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label)


        self.gridLayout.addWidget(self.frameSpacer1, 0, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.frameChooseFile)

        self.btnProcess = QPushButton(self.tabInput)
        self.btnProcess.setObjectName(u"btnProcess")
        self.btnProcess.setMinimumSize(QSize(0, 50))
        font4 = QFont()
        font4.setFamily(u"Roboto")
        font4.setPointSize(14)
        font4.setBold(True)
        font4.setWeight(75)
        self.btnProcess.setFont(font4)
        self.btnProcess.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: white;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/file", QSize(), QIcon.Normal, QIcon.Off)
        self.btnProcess.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.btnProcess)

        self.frameProgress = QFrame(self.tabInput)
        self.frameProgress.setObjectName(u"frameProgress")
        self.frameProgress.setStyleSheet(u"border-radius: 10;\n"
"background-color: rgb(37, 45, 61);\n"
"")
        self.frameProgress.setFrameShape(QFrame.StyledPanel)
        self.frameProgress.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameProgress)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 100, 10, 40)
        self.frameProgressInfo = QFrame(self.frameProgress)
        self.frameProgressInfo.setObjectName(u"frameProgressInfo")
        self.frameProgressInfo.setStyleSheet(u"border:0px;")
        self.frameProgressInfo.setFrameShape(QFrame.NoFrame)
        self.frameProgressInfo.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frameProgressInfo)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(15, 10, 15, 10)
        self.labelProgress = QLabel(self.frameProgressInfo)
        self.labelProgress.setObjectName(u"labelProgress")
        self.labelProgress.setMaximumSize(QSize(16777215, 20))
        self.labelProgress.setFont(font2)
        self.labelProgress.setStyleSheet(u"border: 0px;\n"
"color: white;")
        self.labelProgress.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.labelProgress)

        self.labelTimeLeft = QLabel(self.frameProgressInfo)
        self.labelTimeLeft.setObjectName(u"labelTimeLeft")
        font5 = QFont()
        font5.setFamily(u"Roboto")
        font5.setPointSize(10)
        font5.setBold(True)
        font5.setWeight(75)
        self.labelTimeLeft.setFont(font5)
        self.labelTimeLeft.setStyleSheet(u"color: white;\n"
"border:opx;")
        self.labelTimeLeft.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.labelTimeLeft)


        self.verticalLayout_3.addWidget(self.frameProgressInfo)

        self.progressBar = QProgressBar(self.frameProgress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 30))
        self.progressBar.setMaximumSize(QSize(16777215, 30))
        font6 = QFont()
        font6.setFamily(u"Roboto")
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setWeight(75)
        self.progressBar.setFont(font6)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"	background-color: rgb(44, 53, 72);\n"
"	border-style: none;\n"
"	border-radius: 15px;\n"
"	color: white;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"	border-radius: 15px;\n"
"	\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.494, x2:1, y2:0.5, stop:0.0738636 rgba(29, 22, 22, 255), stop:0.914773 rgba(198, 147, 59, 255));\n"
"}")
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_3.addWidget(self.progressBar)


        self.verticalLayout_2.addWidget(self.frameProgress)

        self.tabWidget.addTab(self.tabInput, "")
        self.tabVideo = QWidget()
        self.tabVideo.setObjectName(u"tabVideo")
        self.verticalLayout_7 = QVBoxLayout(self.tabVideo)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frameMediaPlayer = QFrame(self.tabVideo)
        self.frameMediaPlayer.setObjectName(u"frameMediaPlayer")
        self.frameMediaPlayer.setMinimumSize(QSize(0, 400))
        self.frameMediaPlayer.setStyleSheet(u"background-color: black;")
        self.frameMediaPlayer.setFrameShape(QFrame.StyledPanel)
        self.frameMediaPlayer.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.frameMediaPlayer)

        self.frameMediaInfo = QFrame(self.tabVideo)
        self.frameMediaInfo.setObjectName(u"frameMediaInfo")
        self.frameMediaInfo.setMaximumSize(QSize(16777215, 109))
        self.frameMediaInfo.setFrameShape(QFrame.StyledPanel)
        self.frameMediaInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frameMediaInfo)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frameVideoDescription = QFrame(self.frameMediaInfo)
        self.frameVideoDescription.setObjectName(u"frameVideoDescription")
        self.frameVideoDescription.setMinimumSize(QSize(0, 20))
        self.frameVideoDescription.setMaximumSize(QSize(16777215, 20))
        self.frameVideoDescription.setFrameShape(QFrame.StyledPanel)
        self.frameVideoDescription.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frameVideoDescription)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(20, 0, 0, 0)
        self.labelVideoName = QLabel(self.frameVideoDescription)
        self.labelVideoName.setObjectName(u"labelVideoName")
        font7 = QFont()
        font7.setFamily(u"Roboto")
        font7.setPointSize(10)
        font7.setItalic(True)
        self.labelVideoName.setFont(font7)
        self.labelVideoName.setStyleSheet(u"color: gray;")
        self.labelVideoName.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_11.addWidget(self.labelVideoName)


        self.verticalLayout_8.addWidget(self.frameVideoDescription)

        self.frameMediaControls = QFrame(self.frameMediaInfo)
        self.frameMediaControls.setObjectName(u"frameMediaControls")
        self.frameMediaControls.setFrameShape(QFrame.StyledPanel)
        self.frameMediaControls.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frameMediaControls)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 10, 5, 5)
        self.frameControlBtns = QFrame(self.frameMediaControls)
        self.frameControlBtns.setObjectName(u"frameControlBtns")
        self.frameControlBtns.setStyleSheet(u"margin-left: auto;\n"
"margin-right: auto;")
        self.frameControlBtns.setFrameShape(QFrame.NoFrame)
        self.frameControlBtns.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frameControlBtns)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(300, -1, 300, -1)
        self.btnStop = QPushButton(self.frameControlBtns)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setMinimumSize(QSize(30, 30))
        self.btnStop.setMaximumSize(QSize(30, 30))
        self.btnStop.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: white;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/play", QSize(), QIcon.Normal, QIcon.Off)
        self.btnStop.setIcon(icon5)

        self.horizontalLayout_10.addWidget(self.btnStop)

        self.btnPlay = QPushButton(self.frameControlBtns)
        self.btnPlay.setObjectName(u"btnPlay")
        self.btnPlay.setMinimumSize(QSize(30, 30))
        self.btnPlay.setMaximumSize(QSize(30, 30))
        self.btnPlay.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: white;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icons/stop", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPlay.setIcon(icon6)

        self.horizontalLayout_10.addWidget(self.btnPlay)


        self.verticalLayout_9.addWidget(self.frameControlBtns)

        self.hSliderVideo = QSlider(self.frameMediaControls)
        self.hSliderVideo.setObjectName(u"hSliderVideo")
        self.hSliderVideo.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: rgb(35, 40, 49);\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.5, stop:0 rgba(199, 129, 18, 255), stop:1 rgba(151, 88, 0, 255));\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background-color: white;\n"
"border: 1px solid rgb(40, 48, 65);\n"
"width: 12px;\n"
"margin-top: -2px;\n"
"margin-bottom: -2px;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 4px;\n"
"}")
        self.hSliderVideo.setValue(10)
        self.hSliderVideo.setOrientation(Qt.Horizontal)

        self.verticalLayout_9.addWidget(self.hSliderVideo)


        self.verticalLayout_8.addWidget(self.frameMediaControls)


        self.verticalLayout_7.addWidget(self.frameMediaInfo)

        self.tabWidget.addTab(self.tabVideo, "")
        self.tabLogs = QWidget()
        self.tabLogs.setObjectName(u"tabLogs")
        self.verticalLayout_4 = QVBoxLayout(self.tabLogs)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.textBrowser = QTextBrowser(self.tabLogs)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setFont(font2)
        self.textBrowser.setStyleSheet(u"background-color: white; \n"
"border-radius: 3px;")

        self.verticalLayout_4.addWidget(self.textBrowser)

        self.tabWidget.addTab(self.tabLogs, "")
        self.tabStats = QWidget()
        self.tabStats.setObjectName(u"tabStats")
        self.verticalLayout_5 = QVBoxLayout(self.tabStats)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 50, 10, 50)
        self.statLabel = QLabel(self.tabStats)
        self.statLabel.setObjectName(u"statLabel")
        self.statLabel.setMaximumSize(QSize(16777215, 20))
        self.statLabel.setFont(font6)
        self.statLabel.setStyleSheet(u"color: white;")
        self.statLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.statLabel)

        self.statBox = QFrame(self.tabStats)
        self.statBox.setObjectName(u"statBox")
        self.statBox.setFrameShape(QFrame.StyledPanel)
        self.statBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.statBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frameTotalCount = QFrame(self.statBox)
        self.frameTotalCount.setObjectName(u"frameTotalCount")
        self.frameTotalCount.setFrameShape(QFrame.StyledPanel)
        self.frameTotalCount.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frameTotalCount)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelTotalCountFix = QLabel(self.frameTotalCount)
        self.labelTotalCountFix.setObjectName(u"labelTotalCountFix")
        self.labelTotalCountFix.setFont(font2)
        self.labelTotalCountFix.setStyleSheet(u"color: white;")
        self.labelTotalCountFix.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.labelTotalCountFix)

        self.labelTotalCountVar = QLabel(self.frameTotalCount)
        self.labelTotalCountVar.setObjectName(u"labelTotalCountVar")
        self.labelTotalCountVar.setFont(font5)
        self.labelTotalCountVar.setStyleSheet(u"color: white;")
        self.labelTotalCountVar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.labelTotalCountVar)


        self.verticalLayout_6.addWidget(self.frameTotalCount)

        self.frameNoPassenger = QFrame(self.statBox)
        self.frameNoPassenger.setObjectName(u"frameNoPassenger")
        self.frameNoPassenger.setFrameShape(QFrame.StyledPanel)
        self.frameNoPassenger.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frameNoPassenger)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelNoPassFix = QLabel(self.frameNoPassenger)
        self.labelNoPassFix.setObjectName(u"labelNoPassFix")
        self.labelNoPassFix.setFont(font2)
        self.labelNoPassFix.setStyleSheet(u"color: white;")
        self.labelNoPassFix.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.labelNoPassFix)

        self.labelNoPassVar = QLabel(self.frameNoPassenger)
        self.labelNoPassVar.setObjectName(u"labelNoPassVar")
        self.labelNoPassVar.setFont(font5)
        self.labelNoPassVar.setStyleSheet(u"color: white;")
        self.labelNoPassVar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.labelNoPassVar)


        self.verticalLayout_6.addWidget(self.frameNoPassenger)

        self.frameNoCargo = QFrame(self.statBox)
        self.frameNoCargo.setObjectName(u"frameNoCargo")
        self.frameNoCargo.setFrameShape(QFrame.StyledPanel)
        self.frameNoCargo.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frameNoCargo)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelNoCgoFix = QLabel(self.frameNoCargo)
        self.labelNoCgoFix.setObjectName(u"labelNoCgoFix")
        self.labelNoCgoFix.setFont(font2)
        self.labelNoCgoFix.setStyleSheet(u"color: white;")
        self.labelNoCgoFix.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.labelNoCgoFix)

        self.labelNoCgoVar = QLabel(self.frameNoCargo)
        self.labelNoCgoVar.setObjectName(u"labelNoCgoVar")
        self.labelNoCgoVar.setFont(font5)
        self.labelNoCgoVar.setStyleSheet(u"color: white;")
        self.labelNoCgoVar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.labelNoCgoVar)


        self.verticalLayout_6.addWidget(self.frameNoCargo)

        self.frameNoMotor = QFrame(self.statBox)
        self.frameNoMotor.setObjectName(u"frameNoMotor")
        self.frameNoMotor.setFrameShape(QFrame.StyledPanel)
        self.frameNoMotor.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frameNoMotor)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelNoMotorFix = QLabel(self.frameNoMotor)
        self.labelNoMotorFix.setObjectName(u"labelNoMotorFix")
        self.labelNoMotorFix.setFont(font2)
        self.labelNoMotorFix.setStyleSheet(u"color: white;")
        self.labelNoMotorFix.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.labelNoMotorFix)

        self.labelNoMotorVar = QLabel(self.frameNoMotor)
        self.labelNoMotorVar.setObjectName(u"labelNoMotorVar")
        self.labelNoMotorVar.setFont(font5)
        self.labelNoMotorVar.setStyleSheet(u"color: white;")
        self.labelNoMotorVar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.labelNoMotorVar)


        self.verticalLayout_6.addWidget(self.frameNoMotor)

        self.frameNoUnknown = QFrame(self.statBox)
        self.frameNoUnknown.setObjectName(u"frameNoUnknown")
        self.frameNoUnknown.setFrameShape(QFrame.StyledPanel)
        self.frameNoUnknown.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frameNoUnknown)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.labelNoUnkFix = QLabel(self.frameNoUnknown)
        self.labelNoUnkFix.setObjectName(u"labelNoUnkFix")
        self.labelNoUnkFix.setFont(font2)
        self.labelNoUnkFix.setStyleSheet(u"color: white;")
        self.labelNoUnkFix.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.labelNoUnkFix)

        self.labelNoUnkVar = QLabel(self.frameNoUnknown)
        self.labelNoUnkVar.setObjectName(u"labelNoUnkVar")
        self.labelNoUnkVar.setFont(font5)
        self.labelNoUnkVar.setStyleSheet(u"color: white;")
        self.labelNoUnkVar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.labelNoUnkVar)


        self.verticalLayout_6.addWidget(self.frameNoUnknown)


        self.verticalLayout_5.addWidget(self.statBox)

        self.tabWidget.addTab(self.tabStats, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.drop_shadow_layout.addWidget(self.dropShadowFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleIcon.setText("")
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"IO Vehicle Detection", None))
        self.btnMinimize.setText("")
        self.btnMaximize.setText("")
        self.btnClose.setText("")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type the path to file, drag it onto the bar or choose file from the dialog..", None))
        self.btnChooseFolder.setText(QCoreApplication.translate("MainWindow", u"   Choose File", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Some Intro Text", None))
        self.btnProcess.setText(QCoreApplication.translate("MainWindow", u" Process!", None))
        self.labelProgress.setText(QCoreApplication.translate("MainWindow", u"Complete process in: ", None))
        self.labelTimeLeft.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInput), QCoreApplication.translate("MainWindow", u"File", None))
        self.labelVideoName.setText(QCoreApplication.translate("MainWindow", u"Video_name_rendered.mp4", None))
        self.btnStop.setText("")
        self.btnPlay.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVideo), QCoreApplication.translate("MainWindow", u"Video", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLogs), QCoreApplication.translate("MainWindow", u"Logs", None))
        self.statLabel.setText(QCoreApplication.translate("MainWindow", u"Statistics of detected vehicles", None))
        self.labelTotalCountFix.setText(QCoreApplication.translate("MainWindow", u"Total Vehicle Count: ", None))
        self.labelTotalCountVar.setText(QCoreApplication.translate("MainWindow", u"Total Vehicle Count Num", None))
        self.labelNoPassFix.setText(QCoreApplication.translate("MainWindow", u"No. of Passenger Vehicles: ", None))
        self.labelNoPassVar.setText(QCoreApplication.translate("MainWindow", u"PassengerCar Num", None))
        self.labelNoCgoFix.setText(QCoreApplication.translate("MainWindow", u"No. of Cargo/Bus Vehicles:", None))
        self.labelNoCgoVar.setText(QCoreApplication.translate("MainWindow", u"Cargo/BusCar Num", None))
        self.labelNoMotorFix.setText(QCoreApplication.translate("MainWindow", u"No. of Motorcycles/Bicycles:", None))
        self.labelNoMotorVar.setText(QCoreApplication.translate("MainWindow", u"Motor/Bike Num", None))
        self.labelNoUnkFix.setText(QCoreApplication.translate("MainWindow", u"No. of Unknown Vehicles", None))
        self.labelNoUnkVar.setText(QCoreApplication.translate("MainWindow", u"UnknownCar Num", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStats), QCoreApplication.translate("MainWindow", u"Statistics", None))
    # retranslateUi

