from PyQt5 import QtWidgets
from layout import Ui_IoTTestbed

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IoTTestbed = QtWidgets.QMainWindow()
    ui = Ui_IoTTestbed()
    ui.setupUi(IoTTestbed)
    IoTTestbed.show()
    sys.exit(app.exec_())
