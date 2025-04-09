import argparse
import os.path
from time import time

def get_args() -> argparse.Namespace:
    """Функция получает аргументы из командной строки."""
    parser = argparse.ArgumentParser('Формирует отчет из переданных логов '
                                     'и выводит в консоль.')
    parser.add_argument('paths',
                        nargs='+',
                        type=str,
                        help='Пути к файлам.')
    parser.add_argument('--report',
                        type=str,
                        required=False,
                        help='Название отчета.')
    return parser.parse_args()


class ReportMaker:
    """
    Класс формирует и печатает отчет из лог-файлов.

    Принимает аргументы:
        Обязательные:
                    paths - список путей к файлам.
        Не обязательные:
                    report_name - название отчета,
                    log_levels - уровень логов,
                    module_name - название модуля для отчета,
                    show_execute_time - печать времени выполнения.
    """

    def __init__(self,
                 paths: list[str],
                 report_name: str = None,
                 log_levels: tuple[str, ...] = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
                 module_name: str = 'django.request',
                 show_execute_time = False
                 ):
        self.paths: list[str] = paths
        self.report_name: str = str(report_name) if report_name else ' '
        self.log_levels: tuple[str, ...] = log_levels
        self.module_name: str = str(module_name)
        self.show_execute_time: bool = show_execute_time
        self.key_width: int = 25  # Ширина печати 1 колонки для метода print_report.
        self.value_width: int = 8  # Ширина печати колонок уровня логирования для метода print_report.


    def __str__(self):
        return (f'Log-report for {self.module_name}, log-files: '
                f'{', '.join([file.split('/')[-1] for file in self.paths])}.')

    @property
    def paths(self) -> list[str, ...]:
        return self._paths

    @paths.setter
    def paths(self, value: list[str, ...]) -> None:
        if not isinstance(value, list):
            raise TypeError(f'Значение {value} должно быть списком из путей к файлам')
        for path in value:
            if not path.endswith('.log'):
                raise TypeError(f'Неверный формат файла - {path}, должен быть ".log".')
            if not os.path.exists(path):
                raise FileNotFoundError(f'Неверно указан путь к файлу - {path}.')
        self._paths = value

    @property
    def log_levels(self):
        return self._log_levels

    @log_levels.setter
    def log_levels(self, value: tuple[str, ...]) -> None:
        levels_sample = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        if not value:
            raise ValueError(f'В параметр log_levels нужно передать минимум 1 значение из '
                             f'[{", ".join(levels_sample)}]')
        if value == levels_sample:
            self._log_levels = value
        else:
            for level in value:
                if not isinstance(level, str):
                    raise TypeError(f'Неверный тип значения уровня логирования - {level}, '
                                    f'должно быть строкой.')
                if level.upper() not in levels_sample:
                    raise ValueError(f'Неверное значение уровня логирования - {level}, '
                                     f'должно быть в [{", ".join(levels_sample)}].')
            self._log_levels = tuple((l for l in levels_sample if l in [i.upper() for i in value]))

    def filter_request_line(self, line: str) -> list[str]:
        """Получает необходимые значения из одной записи для django.request."""
        result: list[str] = []
        for item in line.split():
            if item in self.log_levels:
                result.append(item)
            if item.startswith('/'):
                result.append(item)
        return result

    def make_dict(self) -> tuple[dict[str, dict[str, int]], dict[str, int], int]:
        """Получает все записи логов из переданных файлов и
        создает словарь из отфильтрованных логов, подсчитывает количество запросов."""
        log_dict: dict[str, dict[str, int]] = {}
        level_count: dict[str, int] = {level: 0 for level in self.log_levels}
        request_count: int = 0
        for path in self.paths:
            with open(f'{path}', 'r') as f:
                for line in f.readlines():
                    if 'django.request' in line:
                        level, key = self.filter_request_line(line)
                        level_count[level] += 1
                        if key not in log_dict:
                            log_dict[key] = {level: 0 for level in self.log_levels}
                            log_dict[key][level] += 1
                        else:
                            log_dict[key][level] += 1
                else:
                    request_count += 1
                    # в случае доработки для других модулей:
                    # else:
                    #     pass
        return log_dict, level_count, request_count


    def print_report(self):
        """Печатает отчет."""
        start_time = time()
        log_dict, level_count, request_count = self.make_dict()

        report_name: str = f'{self.report_name.upper():<{self.key_width}s}'
        title: tuple = tuple(f'{level.upper():<{self.value_width}s}' for level in self.log_levels)

        head: str = f'Total requests: {str(request_count)}\n\n{report_name}{' '.join(title)}'
        body: str = '\n'.join([f"{key:<{self.key_width}s}" +
                               ' '.join(f"{str(value[level]):<{self.value_width}s}" for level in self.log_levels)
                               for key, value in sorted(log_dict.items(), key=lambda x: x[0])])
        end: str = f'{" ":<{self.key_width}s}' + ' '.join(
            f"{str(value):<{self.value_width}s}" for value in level_count.values())

        print(head, body, end, sep='\n')
        end_time = time()
        if self.show_execute_time:
            print(end_time - start_time)


if __name__ == '__main__':
    arguments = get_args()
    ReportMaker(arguments.paths, arguments.report).print_report()
