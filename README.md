# Quanbub
Игра стенка на стенку
В будущем будет реализованы уровни, графика, усложнённая логика битвы и много чего нового!

!!!
Внимание вышли огромные обновления!
Добавлено:
- Уровни
- Игровая колода
- Улучшения
- Доработана механика боя (появилась дальность атаки)
- Возможность сохранять прогрес(база данных)
- Обновленно музыкальное сопровождение и звуки
- Появилось окошко победы/поражения
- Переделано срабатывание кнопок
- Добавлена настройка громкости
- Появилась отрисовка некоторых элементов во время боя
- Оптимизация

### Авторы: Ranigal, 	Iliushenka, Fordrenis ###

Идея проекта:
- Создать полноценную игру, где основная цель уничтожить вражескую базу, которую защищают враги
- Основной язык программирования: Python
- Библиотеки: PyGame, SQLite3, random

Запуск приложения:
- Скопировать репозиторий
- Скачать все необходимые библиотеки (PyGame)
- Выбрать интерпритатор Python
- Запусить main.py (находится в src)

Разработчикам(если они додумались почитать "прочитай меня"
- Обновите проект в PyCharm до последней версии, сделайте новую ветку и работайте там
Приоритеты в задачах:
- Организовать src, там уже слишком много файлов
- Рефакторинг кода, привести к читабельно у более менее виду
- Графика адекватная, анимации
- Понаделать уровней и персонажей
- Способ получения персонажей
(
Например после прохождения уровня
или гача, типо выпадает с шансом
)
- Протестировать на баги
- Протестировать прохождение игры
- Любые ваши идеи
!!!
Новые особенности:
- Кнопки создаются теперь через ButtonManager, а не обновляются каждую итерацию
(
Логика такова, что кнопки не пересоздаются, а создаются один раз и ты ими пользуешься, естественно можно обновлять их, изменять, но суть с ними теперь сложнее работать
)
- Обратите внимание на структуру меню, если собираетесь что-то добавлять, для каждой новой менюшки вроде levels, создаются отдельные файлы и классы и потом импортируются в main
- Если хотите сделать какую-то глобальную переменную, то делайте её в Settings
