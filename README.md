# cli-приложение

Анализирует логи django-приложения и формирует отчет. Отчет выводится в консоль.

Пример формирование отчёта:
```
python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```
Принимает мининмум 1 позиционный аргумент и опционально название отчета после флага **--report**
