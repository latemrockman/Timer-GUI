import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from form import *
import time


class MyWin(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # var
        self.min = 0
        self.sec = 0
        self.msec = 0

        self.speed = 1
        self.n = 0
        self.n_round = 1
        self.slideDirection = True
        self.run = True
        self.round = False
        self.last_time = 0

        # buttons
        self.ui.btn_Start.clicked.connect(self.start_and_stop)
        self.ui.btn_Round.clicked.connect(self.round_and_reset)

        # timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerFunction)



    def timerFunction(self):
        self.changeTimer()

    def changeTimer(self):
        self.msec += 1

        if self.msec == 1000:
            self.sec += 1
            self.msec = 0
        if self.sec == 60:
            self.min += 1
            self.sec = 0
        if self.min == 60:
            self.min = 0
            self.sec = 0
            self.msec = 0
            self.last_time = 0

        self.setup_lTime()

    def start_and_stop(self):
        if self.run:
            self.timer.start(self.speed)
            self.ui.btn_Start.setText("Стоп")
            self.ui.btn_Round.setText("Круг")
            self.ui.btn_Round.setDisabled(False)
        else:
            self.timer.stop()
            self.ui.btn_Start.setText("Старт")
            self.ui.btn_Round.setText("Сброс")

        self.run = not self.run

    def round_and_reset(self):
        if self.ui.btn_Round.text() == "Круг":
            self.fix_time()
        else:
            self.reset()

    def setup_lTime(self):
        self.ui.l_timer.setText(f"{str(self.min):0>2}:{str(self.sec):0>2}:{str(self.msec):0>3}")

    def reset(self):
        self.min = 0
        self.sec = 0
        self.msec = 0
        self.n_round = 1
        self.last_time = 0

        self.setup_lTime()
        self.ui.listWidget.clear()
        self.ui.btn_Round.setDisabled(True)
        self.ui.btn_Round.setText("Круг")

    def fix_time(self):
        self.time = self.ui.l_timer.text()

        self.round_time = self.str_to_ms(self.time) - self.last_time
        self.round_time = self.ms_to_str(self.round_time)

        self.ui.listWidget.addItem(f"{self.n_round:0>3} - {self.round_time} - {self.time}")
        self.n_round += 1

        self.last_time = self.str_to_ms(self.time)
        self.get_bets_round()

        self.scroll()

    def ms_to_str(self,msec) -> str:
        l = [0, 0, 0]
        l[0] = msec // 60000
        l[1] = (msec % 60000) // 1000
        l[2] = (msec % 60000) % 1000

        return f"{l[0]:0>2}:{l[1]:0>2}:{l[2]:0>3}"

    def str_to_ms(self,s) -> int:
        l = [int(i) for i in s.split(":")]
        return (l[0]*60000 + l[1]*1000 + l[2])

    def get_bets_round(self):
        list_round = []
        for i in range(self.ui.listWidget.count()):
            self.ui.listWidget.item(i).setForeground(QtGui.QColor('grey'))
            t = self.ui.listWidget.item(i).text()[6:15]
            list_round.append(self.str_to_ms(t))

        best = list_round.index(min(list_round))
        worse = list_round.index(max(list_round))

        self.ui.listWidget.item(worse).setForeground(QtGui.QColor('red'))
        self.ui.listWidget.item(best).setForeground(QtGui.QColor('green'))

    def scroll(self):
        if self.n_round > 14:
            self.ui.listWidget.verticalScrollBar().setValue(self.n_round)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())