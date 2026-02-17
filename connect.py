import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="survey_db",
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("✅ Подключение к survey_db успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения к БД: {e}")
    conn = None
    cursor = None


def save_to_database(question_text, answer_text):
    """Сохраняет ответ в твои таблицы Question и Answer"""
    try:
        if not cursor:
            print("❌ Нет подключения к БД!")
            return False

        print(f"БД: Сохраняем вопрос '{question_text}' = '{answer_text}'")

        # 1. Проверяем есть ли такой вопрос в таблице Question
        cursor.execute(
            "SELECT id_q FROM Question WHERE text_q = %s",
            (question_text,)
        )
        result = cursor.fetchone()

        if result:
            q_id = result[0]
            print(f"Найден вопрос с ID: {q_id}")
        else:
            # Создаем новый вопрос
            cursor.execute("""
                INSERT INTO Question (text_q, type_q) 
                VALUES (%s, %s)
            """, (question_text, "radio" if question_text == "Возраст" else "checkbox"))
            q_id = cursor.lastrowid
            conn.commit()
            print(f"Создан новый вопрос с ID: {q_id}")

        # 2. Сохраняем ответ в таблицу Answer
        cursor.execute("""
            INSERT INTO Answer (q_id, text_ans) 
            VALUES (%s, %s)
        """, (q_id, answer_text))

        ans_id = cursor.lastrowid
        conn.commit()

        print(f"✅ Ответ сохранен! ID ответа: {ans_id}")
        return True

    except pymysql.Error as e:
        print(f"❌ БД Ошибка MySQL: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"❌ БД Ошибка: {e}")
        return False


def close_connection():
    if conn:
        conn.close()
        print("🔌 Соединение закрыто")