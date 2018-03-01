from PyQt5 import QtWidgets
from layout import Ui_IoTTestbed


class IoTTestbed(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_IoTTestbed()
        self.ui.setupUi(self)
        self.ui.startTestingButton.clicked.connect(self.testDevice)
        self.ui.exitButton.triggered.connect(self.close)

    def testDevice(self):
        results = "Testing the security of "
        results += self.ui.categoriesCombo.currentText() + " "
        results += self.ui.productsCombo.currentText() + "..."
        self.ui.resultsTextArea.setText(results)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
