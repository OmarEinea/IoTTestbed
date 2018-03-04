from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QProcess
from layout import Ui_IoTTestbed
from data import categories, scripts
import os, sys


def image_path(image):
    return os.path.join(getattr(sys, "_MEIPASS", "."), image)


class IoTTestbed(QMainWindow, Ui_IoTTestbed):
    def __init__(self):
        super().__init__()
        self.process = None
        self.setupUi(self)
        self.setWindowIcon(QIcon(image_path("iot.ico")))
        self.sponsors.setPixmap(QPixmap(image_path("sponsors.png")))
        self.categoriesCombo.addItems(categories)
        self.categoriesCombo.currentTextChanged.connect(self.setProducts)
        self.productsCombo.currentTextChanged.connect(self.setTests)
        self.testsListCombo.itemSelectionChanged.connect(self.toggleTestingButton)
        self.testingButton.clicked.connect(self.startTesting)

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
        if tests:
            self.testsListCombo.addItems(tests)
        elif tests is None:
            self.testsListCombo.addItem("No tests available")

    def startTesting(self):
        if self.process:
            return self.stopTesting()
        self.resultsTextArea.clear()
        test_name = self.testsListCombo.currentItem().text()
        script_name = scripts.get(test_name)
        if script_name:
            product = self.productsCombo.currentText()
            self.resultsTextArea.append(f'Running "{test_name}" script on {product}...\n')
            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.appendResults)
            self.process.finished.connect(self.stopTesting)
            self.process.start("python", ["-u", "tests/" + script_name])
            self.testingButton.setText("Stop Testing")
            self.testingButton.setStyleSheet("color: red")
        else:
            self.resultsTextArea.append(f'"{test_name}" script is not available yet!')

    def stopTesting(self):
        if self.process:
            self.process = self.process.kill()
        self.testingButton.setText("Start Testing")
        self.toggleTestingButton()

    def toggleTestingButton(self):
        if self.process: return
        enabled = len(self.testsListCombo.selectedItems()) > 0
        self.testingButton.setEnabled(enabled)
        self.testingButton.setStyleSheet("color:" + ["grey", "green"][enabled])

    def appendResults(self):
        self.resultsTextArea.append(
            str(self.process.readAllStandardOutput(), encoding="utf-8")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
