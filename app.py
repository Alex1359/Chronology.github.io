from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost", 
        database="test", 
        user="postgres", 
        password="1"
    )

# Основной маршрут
@app.route('/')
def timeline():
    # Получение данных из базы
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, date_end, event FROM events ORDER BY date ASC")
    events = cursor.fetchall()
    cursor.close()
    conn.close()

    # Конвертация из Windows-1251, если это необходимо
    def safe_convert(text):
        # Если это строка (str), просто возвращаем её
        if isinstance(text, str):
            return text
        # Если это байты (bytes), конвертируем их в строку
        return text.decode("windows-1251")
    
    # Применяем преобразование только к нужным полям (например, description)
    converted_events = [
        (event[0], event[1], safe_convert(event[2])) for event in events
    ]

    # Отправляем данные в шаблон
    return render_template('timeline.html', events=converted_events)

if __name__ == '__main__':
    app.run(debug=True)


