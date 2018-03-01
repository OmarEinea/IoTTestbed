from PyQt5 import QtWidgets
from layout import Ui_IoTTestbed
from data import categories


class IoTTestbed(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_IoTTestbed()
        self.ui.setupUi(self)
        self.ui.categoriesCombo.addItems(categories)
        self.ui.categoriesCombo.currentTextChanged.connect(self.setProducts)
        self.ui.startTestingButton.clicked.connect(self.testDevice)
        self.ui.exitButton.triggered.connect(self.close)

    def setProducts(self, category):
        self.ui.productsCombo.clear()
        self.ui.productsCombo.addItems(categories[category])

    def testDevice(self):
        product = self.ui.productsCombo.currentText()
        if product:
            self.ui.resultsTextArea.setText("Testing the security of " + product)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
