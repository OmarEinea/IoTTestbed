from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        self.tests = []
        self.process = None
        self.setupUi(self)
        self.setWindowIcon(QIcon(image_path("iot.ico")))
        self.sponsors.setPixmap(QPixmap(image_path("sponsors.png")))
        self.categoriesCombo.addItems(categories)
        self.categoriesCombo.currentTextChanged.connect(self.setProducts)
        self.productsCombo.currentTextChanged.connect(self.setTests)
        self.testsListCombo.itemSelectionChanged.connect(self.toggleTestingButton)
        self.testingButton.clicked.connect(self.startTesting)
        self.reportButton.clicked.connect(self.exportReport)

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

    def startTesting(self, second=False):
        if self.process:
            return self.stopTesting(force=True)
        if not second:
            self.resultsTextArea.clear()
            self.reportButton.setEnabled(False)
            self.resultsLabel.setText(
                f"Test Results ({self.categoriesCombo.currentText()}: {self.productsCombo.currentText()})"
            )
            self.tests = [test.text() for test in self.testsListCombo.selectedItems()]
        for _ in range(len(self.tests)):
            test_name = self.tests.pop(0)
            script_name = scripts.get(test_name)
            if script_name:
                self.resultsTextArea.append(f'<b>Running "{test_name}" script</b><br>')
                self.process = QProcess()
                self.process.setProcessChannelMode(QProcess.MergedChannels)
                self.process.readyReadStandardOutput.connect(self.appendResults)
                self.process.finished.connect(self.stopTesting)
                self.process.start("python", ["-u"] + script_name.split())
                self.testingButton.setText("Stop Testing")
                self.testingButton.setStyleSheet("color: red")
                break
            else:
                self.resultsTextArea.append(f'"<b>{test_name}" script is not available yet!</b><br>')

    def stopTesting(self, force=False):
        if self.process:
            self.process = self.process.kill()
        if force or not self.tests:
            self.testingButton.setText("Start Testing")
            self.toggleTestingButton()
        else:
            self.startTesting(second=True)

    def toggleTestingButton(self):
        if self.process: return
        enabled = len(self.testsListCombo.selectedItems()) > 0
        self.testingButton.setEnabled(enabled)
        self.testingButton.setStyleSheet("color:" + ["grey", "green"][enabled])

    def appendResults(self):
        self.reportButton.setEnabled(True)
        self.resultsTextArea.append(
            str(self.process.readAllStandardOutput(), encoding="utf-8")
        )

    def exportReport(self):
        open("report.txt", "w+").write(self.resultsTextArea.toPlainText())
        QMessageBox(
            QMessageBox.Information,
            "Report Exported",
            "Test results report was exported to report.txt",
            parent=self
        ).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = IoTTestbed()
    main.show()
    sys.exit(app.exec_())
