from PyQt6 import QtWidgets, QtGui, QtCore
import sys
from connect import save_to_database, close_connection

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(450, 1000) #Увеличил высоту

        central_windget = QtWidgets.QWidget()
        self.setCentralWidget(central_windget)

        # Заголовок
        self.label = QtWidgets.QLabel("Анонимный опрос", central_windget)
        self.label.move(150, 10)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # === ВОЗРАСТ ===
        self.label_age = QtWidgets.QLabel("1. Ваш возраст:", central_windget)
        self.label_age.move(10, 50)
        self.label_age.setStyleSheet("font-weight: bold;")

        ages = ["18-25 лет", "26-35 лет", "36-45 лет", "46-60 лет", "60+ лет"]
        self.age_group = QtWidgets.QButtonGroup(central_windget)
        y_age = 80

        for i, age in enumerate(ages):
            rb = QtWidgets.QRadioButton(age, central_windget)
            rb.move(30, y_age + i * 30)
            self.age_group.addButton(rb, i)

        self.age_group.buttonClicked.connect(self.on_age_clicked)

        # === ХОББИ ===
        y_hobby = y_age + len(ages) * 30 + 30
        self.label_hobby = QtWidgets.QLabel("2. Ваши хобби:", central_windget)
        self.label_hobby.move(10, y_hobby)
        self.label_hobby.setStyleSheet("font-weight: bold;")

        hobbies = ["Спорт", "Чтение", "Музыка", "Путешествия", "Готовка", "Игры", "Рисование", "Фото"]
        self.hobby_checkboxes = []
        y_hobby_start = y_hobby + 30

        for i, hobby in enumerate(hobbies):
            cb = QtWidgets.QCheckBox(hobby, central_windget)
            cb.move(30, y_hobby_start + i * 30)
            cb.stateChanged.connect(self.on_hobby_changed)
            self.hobby_checkboxes.append(cb)

        # === ДОХОД ===
        y_income = y_hobby_start + len(hobbies) * 30 + 30
        self.label_income = QtWidgets.QLabel("3. Ваш ежемесячный доход:", central_windget)
        self.label_income.move(10, y_income)
        self.label_income.setStyleSheet("font-weight: bold;")

        incomes = [
            "До 30 000 руб.",
            "30 000 - 60 000 руб.",
            "60 000 - 100 000 руб.",
            "Более 100 000 руб.",
            "Предпочитаю не отвечать"
        ]
        self.income_group = QtWidgets.QButtonGroup(central_windget)
        y_income_start = y_income + 30

        for i, income in enumerate(incomes):
            rb = QtWidgets.QRadioButton(income, central_windget)
            rb.move(30, y_income_start + i * 30)
            self.income_group.addButton(rb, i)

        self.income_group.buttonClicked.connect(self.on_income_clicked)

        # === СОЦСЕТИ ===
        y_social = y_income_start + len(incomes) * 30 + 30
        self.label_social = QtWidgets.QLabel("4. Какими соцсетями пользуетесь?", central_windget)
        self.label_social.move(10, y_social)
        self.label_social.setStyleSheet("font-weight: bold;")

        socials = [
            "ВКонтакте",
            "Telegram",
            "Instagram",
            "Facebook",
            "TikTok",
            "YouTube",
            "Не пользуюсь соцсетями"
        ]
        self.social_checkboxes = []
        y_social_start = y_social + 30

        for i, social in enumerate(socials):
            cb = QtWidgets.QCheckBox(social, central_windget)
            cb.move(30, y_social_start + i * 30)
            cb.stateChanged.connect(self.on_social_changed)
            self.social_checkboxes.append(cb)

        # === КНОПКА СОХРАНЕНИЯ (ЗДЕСЬ ОНА!) ===
        button_y = y_social_start + len(socials) * 30 + 50
        self.btn_save = QtWidgets.QPushButton("💾 СОХРАНИТЬ В БД", central_windget)
        self.btn_save.move(200, 900)
        self.btn_save.resize(250, 30)
        self.btn_save.clicked.connect(self.save_database)

        # Статус
        self.status_label = QtWidgets.QLabel("", central_windget)
        self.status_label.move(100, button_y + 60)
        self.status_label.resize(250, 30)

        # Переменные
        self.selected_age = None
        self.selected_hobbies = []
        self.selected_income = None
        self.selected_socials = []

    def on_age_clicked(self, button):
        self.selected_age = button.text()
        print(f"Возраст: {self.selected_age}")

    def on_hobby_changed(self):
        self.selected_hobbies = [cb.text() for cb in self.hobby_checkboxes if cb.isChecked()]
        print(f"Хобби: {self.selected_hobbies}")

    def on_income_clicked(self, button):
        self.selected_income = button.text()
        print(f"Доход: {self.selected_income}")

    def on_social_changed(self):
        self.selected_socials = [cb.text() for cb in self.social_checkboxes if cb.isChecked()]
        print(f"Соцсети: {self.selected_socials}")

    def save_database(self):
        if not self.selected_age:
            self.status_label.setText("❌ Выберите возраст!")
            return
        if not self.selected_income:
            self.status_label.setText("❌ Выберите доход!")
            return

        # Сохраняем все
        if self.selected_age:
            save_to_database("Возраст", self.selected_age)
        for hobby in self.selected_hobbies:
            save_to_database("Хобби", hobby)
        if self.selected_income:
            save_to_database("Доход", self.selected_income)
        for social in self.selected_socials:
            save_to_database("Соцсети", social)

        self.status_label.setText("✅ Сохранено!")
        print("Готово")

    def closeEvent(self, event):
        close_connection()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())