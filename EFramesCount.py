import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import os

eFramesCount_window = None

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def get_key_count():
    selection = cmds.ls(selection=True)
    total_keys = 0
    for obj in selection:
        keys = cmds.keyframe(obj, query=True, keyframeCount=True)
        if keys is not None:
            total_keys += keys
    return total_keys

class EFramesCountWindow(QtWidgets.QDialog):
    def __init__(self):
        super(EFramesCountWindow, self).__init__()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        icon_folder = os.path.join(cmds.internalVar(userPrefDir=True), "icons", "EFramesCount")

        self.frame = QtWidgets.QWidget(self)
        self.frame.setStyleSheet("""
            QWidget {
                background-color: rgba(10, 10, 10, 240);
                border-radius: 10px;
                min-width: 200px;
                min-height: 40px;
            }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self.frame)
        self.setLayout(self.main_layout)

        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.title_bar_layout)

        self.key_count_label = QtWidgets.QLabel("Total Keys: 0")
        self.title_bar_layout.addWidget(self.key_count_label)

        self.title_bar_layout.addStretch()
        
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setIcon(QtGui.QIcon(os.path.join(icon_folder, "closeButton.png")))
        self.close_button.setIconSize(QtCore.QSize(20, 20))
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(10, 10, 10, 240);
                border-radius: 10px;
            }
            QPushButton::hover {
                background-color: rgba(20, 20, 20, 240);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);
            }
        """)
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button)

        self.update_key_info()
        
    def update_key_info(self):
        key_count = get_key_count()
        self.key_count_label.setText(f"Total Keys: {key_count}")
        QtCore.QTimer.singleShot(500, self.update_key_info)

    def mousePressEvent(self, event):
        self.mouseClickPosition = event.globalPos() - self.pos()
        super(EFramesCountWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mouseClickPosition:
            self.move(event.globalPos() - self.mouseClickPosition)
        super(EFramesCountWindow, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouseClickPosition = None
        super(EFramesCountWindow, self).mouseReleaseEvent(event)

def create_eFramesCount_window():
    global eFramesCount_window
    if eFramesCount_window is not None:
        eFramesCount_window.close()
        eFramesCount_window = None
    eFramesCount_window = EFramesCountWindow()
    eFramesCount_window.show()

create_eFramesCount_window()
