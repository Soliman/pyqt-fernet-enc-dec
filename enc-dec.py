# pip install -r requirements
import sys
from cryptography.fernet import Fernet
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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

        # Connect buttons to functions
        self.btnGenKey.clicked.connect(self.gen)
        self.btnEncrypt.clicked.connect(self.enc)
        self.btnDecrypt.clicked.connect(self.dec)
        self.btnCopyToClipboard.clicked.connect(self.copyToClipboard) 

        # Create a grid layout
        self.grid = QGridLayout()        

        # Put fields on grid
        self.grid.addWidget(self.lblGenKey, 1, 1)
        self.grid.addWidget(self.key_file, 1, 2)
        self.grid.addWidget(self.lblText, 2, 1)
        self.grid.addWidget(self.text, 2, 2)
        
        # Put buttons on grid
        self.grid.addWidget(self.btnGenKey, 3, 1, 1, 2)
        self.grid.addWidget(self.btnEncrypt, 4, 1, 1, 2)
        self.grid.addWidget(self.btnDecrypt, 5, 1, 1, 2)
        self.grid.addWidget(self.btnCopyToClipboard, 6, 1, 1, 2)

        # Set the grid as layout
        self.setLayout(self.grid)

        # Show window
        self.show()

    
    def gen(self) -> None:        
        try:
            with open(self.key_file.text(), "xb") as outFile:
                key = Fernet.generate_key()
                outFile.write(key)
        except IOError as e:
            QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)


    def enc(self) -> None:
        text = self.text.toPlainText().encode('utf-8')
        key = open(self.key_file.text(), "rb").read()
        f = Fernet(key)
        encrypted = f.encrypt(text)
        self.text.setText(encrypted.decode('utf-8'))


    def dec(self) -> None:
        text = self.text.toPlainText().encode('utf-8')
        key = open(self.key_file.text(), "rb").read()
        f = Fernet(key)
        try:
            decrypted = f.decrypt(text)
            self.text.setText(decrypted.decode('utf-8'))
        except:
            QMessageBox.information(self, 'Error', 'Invalid key', QMessageBox.Ok)

    
    def copyToClipboard(self) -> None:
        QApplication.clipboard().setText(self.text.toPlainText())


    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Message',
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
