# pip install -r requirements
import sys
from cryptography.fernet import Fernet
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyperclip

class main_window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'enc-dec'
        self.left = 10
        self.top = 10
        self.width = 600    
        self.height = 400
        self.init_ui()


    def init_ui(self):
        """ Initialize UI """

        # Set window attributes
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox for key file
        self.lblGenKey = QLabel('Key file', self)
        self.key_file = QLineEdit(self)
        self.key_file.setText('secret.key')

        # Create textbox for text
        self.lblText = QLabel('Text', self)
        self.text = QTextEdit(self)

        # Optional styling on textbox
        # self.text.setFontFamily('Courier New')
        # self.text.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255,255,255)")
        
        # Create buttons
        self.btnGenKey = QPushButton('Gen key', self)
        self.btnEncrypt = QPushButton('Encrypt', self)
        self.btnDecrypt = QPushButton('Decrypt', self)
        self.btnCopyToClipboard = QPushButton('Copy to clipboard', self)       
        self.btnBrowseForKeyFile = QPushButton('Browse', self)
        self.btnBrowseForOpenFile = QPushButton('Open', self)
        self.btnBrowseForSaveFile = QPushButton('Save', self)

        # Connect buttons to functions
        self.btnGenKey.clicked.connect(self.gen)
        self.btnEncrypt.clicked.connect(self.enc)
        self.btnDecrypt.clicked.connect(self.dec)
        self.btnCopyToClipboard.clicked.connect(self.copyToClipboard) 
        self.btnBrowseForKeyFile.clicked.connect(self.browseForKeyFile) 
        self.btnBrowseForOpenFile.clicked.connect(self.browseForOpenFile) 
        self.btnBrowseForSaveFile.clicked.connect(self.browseForSaveFile) 

        """ Start of grid """

        # Create a grid layout
        self.grid = QGridLayout()

        # .addWidget(widget, row, column [,rowSpan], [columnSpan])    

        # Put fields on grid
        self.grid.addWidget(self.lblGenKey, 1, 1)
        self.grid.addWidget(self.key_file, 1, 2)
        self.grid.addWidget(self.lblText, 2, 1)
        self.grid.addWidget(self.text, 2, 2, 1, 2)
        
        # Put buttons on grid        
        self.grid.addWidget(self.btnGenKey, 3, 1, 1, 3)
        self.grid.addWidget(self.btnEncrypt, 4, 1, 1, 3)
        self.grid.addWidget(self.btnDecrypt, 5, 1, 1, 3)
        self.grid.addWidget(self.btnCopyToClipboard, 6, 1, 1, 3)
        self.grid.addWidget(self.btnBrowseForKeyFile, 1, 3, 1, 1)
        self.grid.addWidget(self.btnBrowseForOpenFile, 7, 1, 1, 3)
        self.grid.addWidget(self.btnBrowseForSaveFile, 8, 1, 1, 3)

        # Set the grid as layout
        self.setLayout(self.grid)

        """ End of grid """

        # Show window
        self.show()

    
    def browseForKeyFile(self):
        """ Browse for key file """
        fileName = QFileDialog.getOpenFileName(self,"Browse for key file", "","Key Files (*.key);;All Files (*)")
        self.key_file.setText(fileName[0])


    def browseForOpenFile(self):
        """ Browse for open file """
        fileName = QFileDialog.getOpenFileName(self,"Open file", "","Enc Files (*.enc);;All Files (*)")
        try:
            with open(fileName[0]) as inFile:
                self.text.setText(inFile.readlines()[0])
                self.text.repaint()
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)    


    def browseForSaveFile(self):
        """ Browse for save file """
        fileName = QFileDialog.getSaveFileName(self,"Save text to...",".","Enc file (*.enc)")
        try:
            with open(fileName[0], "w") as outFile:
                outFile.write(self.text.toPlainText())
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)


    def gen(self):
        """ Generate a key file """
        try:
            with open(self.key_file.text(), "xb") as outFile:
                key = Fernet.generate_key()
                outFile.write(key)
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)


    def enc(self):
        """ Encode text """
        text = self.text.toPlainText().encode('utf-8')
        try:
            key = open(self.key_file.text(), "rb").read()
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)
        try:
            f = Fernet(key)
            encrypted = f.encrypt(text)
            self.text.setText(encrypted.decode('utf-8'))
            self.text.repaint()
        except:
            QMessageBox.information(self, 'Error', 'Unable to encode message, check key file.', 
                                    QMessageBox.Ok)


    def dec(self):
        """ Decode text """
        text = self.text.toPlainText().encode('utf-8')
        try:
            key = open(self.key_file.text(), "rb").read()
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)        
        try:
            f = Fernet(key)
            decrypted = f.decrypt(text)
            self.text.setText(decrypted.decode('utf-8'))  
            self.text.repaint()               
        except:
            QMessageBox.information(self, 'Error', 'Unable to decode message, check key file.', 
                                    QMessageBox.Ok)


    
    def copyToClipboard(self):
        """ Copy text to clipboard """
        pyperclip.copy(self.text.toPlainText())


    def closeEvent(self, event):
        """ Close application """
        reply = QMessageBox.question(self, 'Question',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = main_window()
    sys.exit(app.exec_())
