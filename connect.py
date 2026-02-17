import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="survey_db"
)
cursor = conn.cursor()

def chek():
    cursor.execute("select * from users")
    users_data = cursor.fetchall()
    return users_data


def save_to_database(age):
    """Функция для сохранения возраста в БД"""
    try:
        # Получаем или создаем вопрос
        cursor.execute(
            "SELECT id_q FROM Question WHERE text_q = %s",
            ("Ваш возраст",)
        )
        result = cursor.fetchone()

        if result:
            q_id = result[0]
        else:
            cursor.execute("""
                INSERT INTO Question (text_q, type_q) 
                VALUES (%s, %s)
            """, ("Ваш возраст", "radio"))
            q_id = cursor.lastrowid
            conn.commit()

        # Сохраняем ответ
        cursor.execute("""
            INSERT INTO Answer (q_id, text_ans) 
            VALUES (%s, %s)
        """, (q_id, age))

        ans_id = cursor.lastrowid
        conn.commit()

        print(f"✅ Возраст '{age}' сохранен в БД! ID ответа: {ans_id}")
        return True

    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        conn.rollback()
        return False

def close_connection():
    """Закрыть соединение"""
    conn.close()
    print("🔌 Соединение закрыто")

print("✅ Подключение к survey_db готово!")