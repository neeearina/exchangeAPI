import requests
import datetime

import flask

import settings
import database

app = flask.Flask(__name__)


# главная ручка
@app.route('/')
def index():
    return flask.render_template('index.html')


# ручка для обновления данных о валютах
@app.route('/update_rates', methods=['GET'])
def update_rates():
    # запрос к апи
    response = requests.get(f'{settings.API_URL}{settings.API_KEY}')

    # проверка, xто все получено успешно
    if response.status_code == 200:
        # получение данных из запроса о валютах
        data = response.json()
        rates = data['rates']

        # подключение к базе данных
        connection = database.connect_db()
        cursor = connection.cursor()
        # удаление старых данных
        cursor.execute("DELETE FROM exchange_rates")

        # перебираем данные и создаем для каждого новую запись в бд
        for curr, rate in rates.items():
            cursor.execute("INSERT INTO exchange_rates (currency, rate, last_updated) VALUES (?, ?, ?)",
                           (curr, rate, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # сохраняем изменения
        connection.commit()
        connection.close()
        return "currency rates updated successfully"

    # если произошла ошибка с получением данных
    return f"error while receiving currencies"


# Дата и время последнего обнавления
@app.route('/last_updated', methods=['GET'])
def last_updated():
    # подключение к бд и выбор данных о последних обновлениях
    connection = database.connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT last_updated FROM exchange_rates LIMIT 1")
    result = cursor.fetchone()
    connection.close()

    # проверка на то, найдены ли какие-лиюо обновления
    if result:
        return f"last updated: {result[0]}"

    return "no data"


# Конвертация валюты
@app.route('/convert', methods=['POST'])
def convert():
    # из какой валюты будем конвертировать
    from_curr = flask.request.json.get('from_currency')
    # в какую валюту будем конвертировать
    to_curr = flask.request.json.get('to_currency')
    # кол-во валюты
    amount = float(flask.request.json.get('amount'))

    # подключаемся к бд
    connection = database.connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT rate FROM exchange_rates WHERE currency = ?",
                   (from_curr,))
    from_rate = cursor.fetchone()
    cursor.execute("SELECT rate FROM exchange_rates WHERE currency = ?",
                   (to_curr,))
    to_rate = cursor.fetchone()
    connection.close()

    if from_rate is not None and to_rate is not None:
        return flask.jsonify({
            'converted_amount': round((amount / from_rate[0]) * to_rate[0], 2)
        }, 200)

    return flask.jsonify({'error': 'check the correct currencies'}), 400


if __name__ == '__main__':
    database.create_table()
    app.run(debug=True)
