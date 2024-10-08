# exchangeAPI

> API для обновления и просмотра данных о курсах валют.

# Запуск проекта в dev режиме

### Создайте виртуальное окружение:

```commandline
python3 -m venv venv 
```

### Активируйте виртуальное окружение:

```commandline
source venv/bin/activate 
```

### Установите зависимости для проекта:

```commandline
pip install -r requirements.txt
```

### Перейдите в папку /converter:

```commandline
cd converter
```

### В файле settings.py установите значение переменной API_KEY для корректной работы с запросами

### Запустите приложение:

```commandline
python app.py
```

### После выполнения команды перейдите по ссылке в терминале, откроется главная страница, с которой можно работать:

![Image alt](https://github.com/neeearina/exchangeAPI/raw/main/converter/screenshots/img.png)

# Роуты в API

> /last_updated - данные о последнем обновлении курса валют
>
> /update_rates - обновление данных о курсах валют в базе данных
