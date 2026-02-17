from PyQt6 import QtWidgets,QtGui,QtCore
import sys
from connect import save_to_database,close_connection

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

        self.btn_save = QtWidgets.QPushButton("save",central_windget)
        self.btn_save.move(300,700)
        self.btn_save.clicked.connect(self.save_database)

        self.status_label = QtWidgets.QLabel("", central_windget)
        self.status_label.move(100, 650)
        self.status_label.resize(200, 30)


        self.selected_age = None

    def on_clicked(self, button):
        self.selected_age = button.text()
        print(f"Выбрано: {self.selected_age}")

    def save_database(self):
        """Сохраняем в БД"""
        if not self.selected_age:
            self.status_label.setText("❌ Сначала выберите возраст!")
            self.status_label.setStyleSheet("color: red;")
            return

        # Вызываем функцию из connect.py
        success = save_to_database(self.selected_age)

        if success:
            self.status_label.setText(f"✅ Сохранено: {self.selected_age}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("❌ Ошибка сохранения")
            self.status_label.setStyleSheet("color: red;")

    def closeEvent(self, event):
        close_connection()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())