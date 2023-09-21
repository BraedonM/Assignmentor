from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QSize
from PyQt6 import QtGui
import sys


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        old_size = event.oldSize()
        new_size = QSize(self.geometry().width(), self.geometry().height())
        print(f"Old size: {old_size}\nNew size: {new_size}")
        QMainWindow.resizeEvent(self, event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
