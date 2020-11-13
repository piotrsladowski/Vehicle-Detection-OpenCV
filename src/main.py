#######################################
# Project: IO_Vehicle_Detection Project
# Authors: Mateusz Smendowski, Piotr Sladowski, Adam Twardosz
# Copyright (C) Mateusz Smendowski, Piotr Sladowski, Adam Twardosz 2020
#######################################

import sys
import platform
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QSize, Qt, QCoreApplication
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtWidgets import *

from gui.ui_main import Ui_MainWindow
import gui.all_icons_rc

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
TITLE = "IO Vehicle Detection"

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"IO_VD Application", None))
        self.setWindowIcon(QtGui.QIcon(u":/icons/car_logo"))

        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        UIFunctions.remove_title_bar(self, True)

        startSize = QSize(800, 600)
        self.resize(startSize)
        self.setMinimumSize(startSize)


        # SET TABS DISABLED UNTIL FILE IS PRCESSED
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.tabWidget.setTabEnabled(3, False)

        # ALLOW WINDOW TO MOVE ON THE SCREEN
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.return_status(self) == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.titleBar.mouseMoveEvent = moveWindow

        UIFunctions.ui_definitions(self)

        self.show()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

class UIFunctions(MainWindow):

    # GLOBALS
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

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

    # SET STATUS
    def set_status(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def remove_title_bar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def ui_definitions(self):
        def doubleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

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
        self.ui.btnMaximize.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION
        self.ui.btnClose.clicked.connect(lambda: self.close())


# ----------- MAIN_FUNC ----------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
