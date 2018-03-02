from PyQt5.QtWidgets import QApplication, QMainWindow
from layout import Ui_IoTTestbed
from execute import Execute
from data import categories


class IoTTestbed(QMainWindow, Ui_IoTTestbed):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.categoriesCombo.addItems(categories)
        self.categoriesCombo.currentTextChanged.connect(self.setProducts)
        self.startTestingButton.clicked.connect(self.testDevice)
        self.exitButton.triggered.connect(self.close)

    def setProducts(self, category):
        self.productsCombo.clear()
        self.productsCombo.addItems(categories[category])

    def testDevice(self):
        product = self.productsCombo.currentText()
        if not product: return
        self.resultsTextArea.clear()
        self.resultsTextArea.append("Testing the security of " + product + "...\n")
        self.test = Execute("test.py")
        self.test.progressed.connect(self.resultsTextArea.append)
        self.test.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
