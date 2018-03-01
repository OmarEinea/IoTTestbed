from PyQt5 import QtWidgets
from layout import Ui_IoTTestbed


class IoTTestbed(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_IoTTestbed()
        self.ui.setupUi(self)
        self.ui.testButton.clicked.connect(self.test_device)
        self.ui.exitButton.triggered.connect(self.close)

    def test_device(self):
        results = "Testing the security of "
        results += self.ui.brandsList.currentText() + " "
        results += self.ui.productsList.currentText() + "..."
        self.ui.resultsOutput.setText(results)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
