from PyQt5 import QtWidgets
from layout import Ui_IoTTestbed


class IoTTestbed(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Ui_IoTTestbed()
        ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
