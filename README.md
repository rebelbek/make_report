# cli-приложение

Анализирует логи django-приложения и формирует отчет. Отчет выводится в консоль.

Пример формирование отчёта:
```
python3 main.py example_logs/app1.log example_logs/app2.log example_logs/app3.log --report handlers
```

Принимает минимум 1 позиционный аргумент пути к файлу и опционально 
аргумент для названия отчета после флага **--report**.

Чтобы добавить новый отчет, нужно изменить аттрибут **module_name** и 
метод **filter_line** в классе **ReportMaker**.

Разработано на Python версии **3.12.3**.
В старых версиях python могут не поддерживаться "f-строки" для форматирования текста.

## Запуск pytest:
```
pip install -r requirements.txt
python -m pytest
```
