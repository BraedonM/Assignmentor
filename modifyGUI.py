from PyQt6.QtWidgets import (QMainWindow, QApplication, QMessageBox,
                             QWidget, QFileDialog, QStyledItemDelegate, QComboBox, QCalendarWidget, QTableWidgetItem,
                             QAbstractItemView, QHeaderView, QTableWidget, QScrollArea, QSizePolicy, QLabel)
from PyQt6.QtCore import QSize, Qt, QPoint, QModelIndex
from PyQt6.QtGui import QPixmap, QColor, QResizeEvent, QFont

from windowGUI import Ui_AssignmentTracker


class MyQComboBox(QComboBox):
    """
    This class is used to make the QComboBoxes in the table not scrollable
    """

    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(MyQComboBox, self).__init__(*args, **kwargs)
        self.scrollWidget = scrollWidget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            return self.scrollWidget.wheelEvent(*args, **kwargs)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_AssignmentTracker()
        self.ui.setupUi(self)

        self.initializeUI()

    def initializeUI(self):
        # Initialize variables
        self.courseButtonHeight = 0

        # Make 'COURSE' and 'STATUS' columns drop-down menus
        for r in range(self.ui.tableWidget.rowCount()):

            # Make 'COURSE' column drop-down menus
            courseBox = MyQComboBox(self.ui.tableWidget)

            # Set placeholder text & add items
            courseBox.setPlaceholderText("Course")
            courseBox.addItems(["Course 1", "Course 2", "Course 3"])

            # Set font to Montserrat Medium
            courseBox.setFont(QFont("Montserrat Medium", 10))
            courseBox.currentIndexChanged.connect(self.tableUpdate)
            self.ui.tableWidget.setCellWidget(r, 1, courseBox)

            # Make 'STATUS' column drop-down menus
            statusBox = MyQComboBox(self.ui.tableWidget)

            # Set placeholder text & add items
            statusBox.setPlaceholderText("Status")
            statusBox.addItems(["Not Started", "In Progress", "Completed"])

            # Set font to Montserrat Medium
            statusBox.setFont(QFont("Montserrat Medium", 10))
            statusBox.currentIndexChanged.connect(self.tableUpdate)
            self.ui.tableWidget.setCellWidget(r, 4, statusBox)

        # '+' button connects to addCourse
        self.ui.addCourse.clicked.connect(self.addCourse)

        # Change tab widget style
        self.ui.tabWidget.setStyleSheet("QTabBar::tab { height: 40px; width: 150px}"
                                        "QTabBar::tab:selected { font: 10pt \"Montserrat Semibold\"; }"
                                        "QTabBar::tab:!selected { font: 10pt \"Montserrat Medium\"; }"
                                        "QTabWidget::tab-bar { left: 27px; }")

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.windowHeight = self.geometry().height()
        self.windowWidth = self.geometry().width()

        QMainWindow.resizeEvent(self, event)

    def tableUpdate(self):
        # Get the row and column of the cell that was changed
        row = self.ui.tableWidget.currentRow()
        column = self.ui.tableWidget.currentColumn()

        if column == 1:
            color = QColor(150, 130, 130)  # Row highlight color based on the course

            color1 = int(str(color.getRgb()).split(', ')[0].split('(')[-1])
            color2 = int(str(color.getRgb()).split(', ')[1])
            color3 = int(str(color.getRgb()).split(', ')[2])

            bColor = f"rgb({color1-5}, {color2-5}, {color3-5})"

            # Color the row
            for j in range(self.ui.tableWidget.columnCount()):
                if j == 1 or j == 4:
                    # Color the combo box

                    if color1 + color2 + color3 > 400:
                        self.ui.tableWidget.cellWidget(row, j).setStyleSheet(f"background-color: {bColor}; "
                                                                             f"color: rgb(0, 0, 0);")
                    else:
                        self.ui.tableWidget.cellWidget(row, j).setStyleSheet(f"background-color: {bColor};")

                else:
                    # Get the current text of the cell
                    cellText = self.ui.tableWidget.model().data(self.ui.tableWidget.model().index(row, j))
                    # Change the background color while keeping the text
                    self.ui.tableWidget.setItem(row, j, QTableWidgetItem(cellText))
                    self.ui.tableWidget.item(row, j).setBackground(color)

                    if color1 + color2 + color3 > 400:
                        self.ui.tableWidget.item(row, j).setForeground(QColor(0, 0, 0))

        elif column == 4:
            if self.ui.tableWidget.cellWidget(row, column).currentText() == "Completed":
                # Remove the row
                self.ui.tableWidget.removeRow(row)
                # Move the 'Add Course' button up
                self.courseButtonHeight -= 33
                if self.courseButtonHeight >= 0:
                    self.ui.addCourse.move(self.ui.addCourse.x(), self.ui.addCourse.y() - 33)

            # Check if table is empty
            if self.ui.tableWidget.rowCount() == 0:
                self.ui.noAssignmentText.setText("No Assignments!")
                self.ui.newAssignmentText.setText("Press + to create one")
                # Format the text
                self.ui.noAssignmentText.setStyleSheet("color: rgb(255, 255, 255); font: 36pt \"Montserrat Medium\";")
                self.ui.newAssignmentText.setStyleSheet("color: rgb(255, 255, 255); font: 18pt \"Montserrat Light\";")

    def addCourse(self):
        # Program moves the 'Add Course' button down if it is clicked and there is enough space
        if (self.courseButtonHeight + 33) <= (self.windowHeight - 200):
            # Move the 'Add Course' button down
            self.courseButtonHeight += 33
            self.ui.addCourse.move(self.ui.addCourse.x(), self.ui.addCourse.y() + 33)

        # Add a new row to the table
        numRows = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(numRows)

        # Add course combo box
        courseBox = MyQComboBox(self.ui.tableWidget)
        courseBox.setPlaceholderText("Course")
        courseBox.addItems(["Course 1", "Course 2", "Course 3"])
        # Set font
        courseBox.setFont(QFont("Montserrat Medium", 10))

        # Set flat to true
        courseBox.setStyleSheet("QComboBox { flat: true; }"
                                "")


        courseBox.currentIndexChanged.connect(self.tableUpdate)
        self.ui.tableWidget.setCellWidget(numRows, 1, courseBox)

        # Add status combo box
        statusBox = MyQComboBox(self.ui.tableWidget)
        statusBox.setPlaceholderText("Status")
        statusBox.addItems(["Not Started", "In Progress", "Completed"])
        # Set font
        statusBox.setFont(QFont("Montserrat Medium", 10))
        statusBox.currentIndexChanged.connect(self.tableUpdate)
        self.ui.tableWidget.setCellWidget(numRows, 4, statusBox)

        # Clear the text
        self.ui.noAssignmentText.setText("")
        self.ui.newAssignmentText.setText("")

        # Make the text able to click through
        self.ui.noAssignmentText.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.newAssignmentText.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
