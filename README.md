Описание проекта по моделированию системы Леннарда-Джонса
Обзор
Данный проект представляет собой моделирование системы Леннарда-Джонса с использованием метода Стермера-Верле. Система состоит из частиц, взаимодействия между которыми моделируются с использованием потенциала Леннарда-Джонса. В рамках моделирования учитываются периодические граничные условия, а также изучается поведение системы при переходе из упорядоченного состояния в детерминированный хаос.

Структура проекта
Проект состоит из следующих компонентов:

Particle Class: Определяет поведение и свойства отдельных частиц.
main.py: Оркестрирует моделирование, обеспечивает инициализацию, эволюцию во времени и сбор данных.
particleclass.py: Содержит определение класса Particle.
maxwell.py: Визуализирует распределение скоростей частиц.
energy.py: Строит графики эволюции различных энергетических характеристик во времени.
way.py: Генерирует график перемещения частиц во времени.
Particle Class (particleclass.py)
Атрибуты
c: Координаты частиц.
v: Скорости частиц.
a: Ускорения частиц.
lc: Последняя позиция координат.
way: Перемещение частиц от начальной точки.
Методы
init(self, c, v, a, lc, way): Инициализирует новую частицу с заданными атрибутами.
to_border(self): Обеспечивает нахождение частицы в пределах границы моделирования путем корректировки ее координат.
vec_to_virtual_copy(self, partc, part1c): Рассчитывает вектор до виртуальной копии другой частицы.
first_move(self): Перемещает частицу в первый раз.
move(self): Перемещает частицу с использованием схемы Верле.
Выполнение моделирования (main.py)
Шаги
Инициализация частиц с заданными положениями, скоростями и ускорениями.
Создание модельной области и установка периодических граничных условий.
Эволюция системы на протяжении определенного числа временных шагов.
Сбор и анализ данных в регулярные интервалы.
Сценарии визуализации
maxwell.py: Отображает распределение скоростей частиц по закону Максвелла.
energy.py: Строит графики эволюции механической, кинетической и потенциальной энергии.
way.py: Генерирует график, иллюстрирующий среднее перемещение частиц во времени.
Использование
Для запуска моделирования:

Убедитесь, что установлены все необходимые пакеты Python.
Запустите скрипт main.py для запуска моделирования.
Ознакомьтесь с полученными графиками и файлами данных для анализа поведения системы.
