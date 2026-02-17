from PyQt6 import QtWidgets,QtGui,QtCore
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400,800)

        central_windget = QtWidgets.QWidget()
        self.setCentralWidget(central_windget)

        self.label = QtWidgets.QLabel("Анонимный вопрос", central_windget)
        self.label.move(150,10)

        self.label_age = QtWidgets.QLabel("ваш возраст",central_windget)
        self.label_age.move(10,50)

        ages = ["18-25 лет", "26-35 лет", "36-45 лет", "46-60 лет", "60+ лет"]
        self.group = QtWidgets.QButtonGroup()
        y_pozotion = 80
        for i, ages in enumerate(ages):
            r1 = QtWidgets.QRadioButton(ages, central_windget)
            r1.move(30,y_pozotion + i * 30)
            r1.setStyleSheet("font-size: 12px;")
            self.group.addButton(r1,i)

        self.group.buttonClicked.connect(self.on_clicked)
    def on_clicked(self, button):
        print(f"{button.text()}")






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())