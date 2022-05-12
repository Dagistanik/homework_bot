## Бот-ассистент для Telegramm.

### Описание
Бот обращается к API сервиса Практикум.Домашка и узнаёт статус домашней работы. Бот написан на Python 3 с использованием элементов функционального программирования. Для работы используется анализ JSON формата. Реализовано ведение лога программы.

#### Инструкция по развёртыванию
* Клонировать репозиторий и перейти в него в командной строке:

```python
git clone https://github.com/Dagistanik/homework_bot.git
```

```python
cd homework_bot
```


* Cоздать и активировать виртуальное окружение:

```python
python -m venv env
```

```python
source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt
```python
python -m pip install --upgrade pip
```
```python
pip install -r requirements.txt
```
* Запустить сервер

```Python
python manage.py runserver
```
#### Язык

* Python 3.7

#### Стек технологий

* Python 3
* ООП
* REST API