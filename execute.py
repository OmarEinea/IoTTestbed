from PyQt5.QtCore import QThread, pyqtSignal


class Execute(QThread):
    progressed = pyqtSignal(str)

    def __init__(self, script):
        super(QThread, self).__init__()
        self.script = script

    def run(self):
        exec(open("tests/" + self.script).read(), {"print": self.print})

    def print(self, *args, **kwargs):
        progress = " ".join(map(str, args))
        self.progressed.emit(progress)
