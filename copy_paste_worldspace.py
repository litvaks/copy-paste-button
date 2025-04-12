from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance

# Store copied position globally
copiedPosition = []

def get_mayaWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

class CopyPasteWorldPos_UI(QtWidgets.QDialog):
    def __init__(self, parent=get_mayaWindow()):
        super(CopyPasteWorldPos_UI, self).__init__(parent)
        
        # Build Window
        self.setWindowTitle("Copy + Paste World Position")
        self.setMinimumWidth(150)
        self.setMinimumHeight(100)

        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Instruction for Copy Button
        self.copy_label = QtWidgets.QLabel("1. Select one object and click 'Copy' to store its world position.")
        self.copy_label.setWordWrap(True)
        self.copy_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.copy_label)

        # Create Copy Button
        self.copyButton = QtWidgets.QPushButton("Copy Position")
        self.copyButton.setStyleSheet("background-color: #677875;")
        self.copyButton.clicked.connect(self.copy_position)
        layout.addWidget(self.copyButton)

        # Instruction for Paste Button
        self.paste_label = QtWidgets.QLabel("2. Select another object and click 'Paste' to transfer saved position.")
        self.paste_label.setWordWrap(True)
        self.paste_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.paste_label)

        # Create Paste Button (disabled by default)
        self.pasteButton = QtWidgets.QPushButton("Paste Position")
        self.pasteButton.setEnabled(False)
        self.pasteButton.setStyleSheet("background-color: #566361;") 
        self.pasteButton.clicked.connect(self.paste_position)
        layout.addWidget(self.pasteButton)

        self.setLayout(layout)

    def copy_position(self):
        global copiedPosition
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("Select an object to copy position.")
            return
        copiedPosition = cmds.xform(sel[0], query=True, worldSpace=True, translation=True)
        print(f"[Copied] {sel[0]} world position: {copiedPosition}")
        self.pasteButton.setEnabled(True)  # Enable paste button after copying!

    def paste_position(self):
        global copiedPosition
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("Select an object to paste position to.")
            return
        if not copiedPosition:
            cmds.warning("No position copied.")
            return
        cmds.xform(sel[0], worldSpace=True, translation=copiedPosition)
        print(f"[Pasted] {copiedPosition} to {sel[0]}")

# Kill old window if it exists
def show_WorldCopyPaste_ui():
    for widget in QtWidgets.QApplication.allWidgets():
        if isinstance(widget, CopyPasteWorldPos_UI):
            widget.close()
            widget.deleteLater()
    ui = CopyPasteWorldPos_UI()
    ui.show()

show_WorldCopyPaste_ui()
