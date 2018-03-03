from PyQt5.QtWidgets import QApplication, QMainWindow
from data import categories, scripts
from layout import Ui_IoTTestbed
from execute import Execute


class IoTTestbed(QMainWindow, Ui_IoTTestbed):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.categoriesCombo.addItems(categories)
        self.categoriesCombo.currentTextChanged.connect(self.setProducts)
        self.productsCombo.currentTextChanged.connect(self.setTests)
        self.startTestingButton.clicked.connect(self.startTesting)
        self.exitButton.triggered.connect(self.close)
        self.testsListCombo.currentTextChanged.connect(
            lambda: self.startTestingButton.setEnabled(True)
        )

    def setProducts(self, category):
        self.productsCombo.clear()
        products = categories[category]
        if products:
            self.productsCombo.setEnabled(True)
            self.productsCombo.addItems(products)
        else:
            self.productsCombo.setEnabled(False)

    def setTests(self, product):
        self.testsListCombo.clear()
        tests = categories[self.categoriesCombo.currentText()].get(product, False)
        self.testsListCombo.setEnabled(tests is not None)
        self.startTestingButton.setEnabled(False)
        if tests:
            self.testsListCombo.addItems(tests)
        elif tests is None:
            self.testsListCombo.addItem("No tests available")

    def startTesting(self):
        self.resultsTextArea.clear()
        test_name = self.testsListCombo.currentItem().text()
        script_path = scripts.get(test_name)
        if script_path:
            product = self.productsCombo.currentText()
            self.resultsTextArea.append(f'Running "{test_name}" script on {product}...\n')
            self.test = Execute("test.py")
            self.test.progressed.connect(self.resultsTextArea.append)
            self.test.start()
        else:
            self.resultsTextArea.append(f'"{test_name}" script is not available yet!')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
