import sys
from PyQt6 import QtWidgets
import modifyGUI as gui

# start the Qt GUI application
app = QtWidgets.QApplication(sys.argv)

# Fusion style
app.setStyle("Fusion")

# create an instance of the GUI
ui = gui.MainWindow()
ui.show()

# exit the GUI
sys.exit(app.exec())
