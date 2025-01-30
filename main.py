import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

def load_patients(file_path):
    # Load the spreadsheet TODO: check if it works with multiple sheets, or one sheet required
    df = pd.read_excel(file_path, sheet_name='Лист1', na_filter=True)
    # first_col is required since this is the column we group by. Other columns will get their own name like supposed to
    first_col = df.columns[0]
    # Remove the whitespaces from EVERY CELL, this doesn't have to be reworked, although if someone decides to parse something with a space that is actually needed a problem may arise
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # WARNING: UNCOMMENT THIS ONLY IF YOU WANT TO HAVE NaNs IN THE PATIENT LIST. WILL BREAK EVERYTHING.
    # df['Unnamed: 0'].fillna(method='ffill', inplace=True)

    # Group the data by patient name
    grouped = df.groupby(first_col)

class FileManipulator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Window settings
        self.setWindowTitle('File Manipulator')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # Labels and buttons, as well as event listeners tied to the buttons
        url = "https://github.com/EvgeniiIsaenko/covid-lethality"
        def on_linkActivated(url):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        self.link_label = QLabel('<a href={}>User Manual</a>'.format(url))
        self.link_label.linkActivated.connect(on_linkActivated)
        layout.addWidget(self.link_label)

        self.label = QLabel('Select a file to process', self)
        layout.addWidget(self.label)

        self.btn_open = QPushButton('Open CSV/XLSX', self)
        self.btn_open.clicked.connect(self.openFile)
        layout.addWidget(self.btn_open)

        self.btn_process = QPushButton('Process File', self)
        self.btn_process.clicked.connect(self.processFile)
        layout.addWidget(self.btn_process)

        self.btn_save = QPushButton('Save File', self)
        self.btn_save.clicked.connect(self.saveFile)
        layout.addWidget(self.btn_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Opens the spreadsheet
    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.xlsx);;Excel Files (*.csv);;All Files (*)", options=options)
        # If an actual file, saves the file name
        if fileName:
            self.filePath = fileName
            self.label.setText(f'Selected File: {self.filePath}')

    # Processes the spreadsheet (breaks it down into an array of patients with ALL of their characteristics)
    def processFile(self):
        if hasattr(self, 'filePath'):
            self.patients = load_patients(self.filePath)

    # Saves the file
    def saveFile(self):
        if hasattr(self, 'data'):
            options = QFileDialog.Options()
            saveFileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)", options=options)
            if saveFileName:
                if saveFileName.endswith('.csv'):
                    self.data.to_csv(saveFileName, index=False)
                elif saveFileName.endswith('.xlsx'):
                    self.data.to_excel(saveFileName, index=False)
                self.label.setText(f'File saved as: {saveFileName}')

# Launches the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManipulator()
    ex.show()
    sys.exit(app.exec_())
