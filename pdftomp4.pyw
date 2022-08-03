#!/usr/bin/env python3
"""
Turns
"""
import argparse

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon

from subprocess import Popen, PIPE

_CURR = os.path.abspath(os.path.dirname(__file__))
UI_PDFTOMP4 = uic.loadUiType(os.path.join(_CURR, "pdftomp4.ui"))[0]

class PfdToMp4(QtWidgets.QMainWindow, UI_PDFTOMP4):
    """Main window"""
    def __init__(self, parent=None):
        # Initialize UI
        super().__init__(parent)
        self.setupUi(self)

    def Update(self):
        self.pbExecute.setEnabled(True if self.edSource.text != "" and self.edDestination.text != "" else False)

    def OnOpen(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open source PDF", "","PDF (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.edSource.setText(fileName)
        self.Update()

    def OnSave(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Select destination MP4","untitled.mp4","Video (*.mp4);;All Files (*)", options=options)
        if fileName:
            if os.path.splitext(fileName)[-1] != ".mp4":
                fileName += ".mp4"
            self.edDestination.setText(fileName)
        self.Update()

    def OnExecute(self):
        self.Command("mkdir", frames)
        self.command("pdftoppm", "self.edSource -png frames/frame")
        if not self.chKeep.isChecked():
            self.Command("rm", frames)
        

    def Command(self, *command):
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        return (process.stdout.read().decode(), process.stderr.read().decode())

def Main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.parse_args()

    QtCore.QCoreApplication.setOrganizationName("MS Studio");
    QtCore.QCoreApplication.setOrganizationDomain("msstudio.nl");
    QtCore.QCoreApplication.setApplicationName("Pdf to Mp4");
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QtWidgets.QApplication([])
    #app.setWindowIcon(QtGui.QIcon('mccommand.png'))

    window = PfdToMp4()
    window.show()

    if (sys.flags.interactive != -1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()

    del app

if __name__ == '__main__':
    Main()
