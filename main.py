import argparse
import os.path


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
        Обязательные: paths.
        Не обязательные: report_name, log_levels, module_name.
    """

    def __init__(self,
                 paths: list[str],
                 report_name: str = None,
                 log_levels: tuple[str, ...] = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
                 module_name: str = 'django.request'
                 ):
        self.paths: list[str] = paths
        self.report_name: str = report_name
        self.log_levels: tuple[str, ...] = log_levels
        self.module_name: str = module_name
        self.key_width: int = 25
        self.value_width: int = 8

    def __str__(self):
        return (f'Report for logs in {self.module_name}, paths to file: '
                f'{', '.join([path for path in self.paths])}.')

    @property
    def paths(self) -> list[str, ...]:
        return self._paths

    @paths.setter
    def paths(self, value: list[str, ...]) -> None:
        for path in value:
            if not os.path.exists(path):
                raise FileNotFoundError(f'Неверно указан путь к файлу - {path}.')
            if not path.endswith('.log'):
                raise TypeError(f'Неверный формат файла - {path}, должен быть ".log".')
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
                    raise TypeError(f'Неверное значение уровня логирования - {level}, '
                                    f'должно быть строкой.')
                if level.upper() not in levels_sample:
                    raise ValueError(f'Неверное значения уровня логирования - {level}, '
                                     f'должно быть в [{", ".join(levels_sample)}].')
            self._log_levels = tuple((l for l in levels_sample if l in [i.upper() for i in value]))

    def filter_line(self, line: str) -> list[str]:
        """Получает необходимые значения из одной записи."""
        result: list[str] = []
        for item in line.split():
            if self.module_name == 'django.request':
                if item in self.log_levels:
                    result.append(item)
                if item.startswith('/'):
                    result.append(item)
            else:
                # в случае доработки для других модулей
                pass
        return result

    def filter_logs(self) -> list[list[str]]:
        """Получает все записи логов из переданных файлов и фильтрует необходимые данные."""
        result: list[list[str]] = []
        for path in self.paths:
            with open(f'{path}', 'r') as f:
                for line in f.readlines():
                    if self.module_name in line:
                        result.append(self.filter_line(line))
        return result

    def make_dict(self) -> tuple[dict[str, dict[str, int]], dict[str, int], int]:
        """Создает словарь из отфильтрованных логов и подсчитывает количество запросов."""
        log_dict: dict[str, dict[str, int]] = {}
        level_count: dict[str, int] = {level: 0 for level in self.log_levels}
        request_count: int = 0
        for item in self.filter_logs():
            key = item[1]
            level = item[0]
            level_count[level] += 1
            request_count += 1
            if key not in log_dict:
                log_dict[key] = {level: 1}
            else:
                if level not in log_dict[key]:
                    log_dict[key][level] = 1
                else:
                    log_dict[key][level] += 1
        return log_dict, level_count, request_count

    def print_report(self):
        """Печатает отчет."""
        log_dict, level_count, request_count = self.make_dict()
        report_name: str = f'{self.report_name.upper():<{self.key_width}s}' \
            if self.report_name else f'{" ":<{self.key_width}s}'
        title: str = (f'{level.upper():<{self.value_width}s}' for level in self.log_levels)
        head: str = f'Total requests: {str(request_count)}\n\n{report_name} {' '.join(title)}'
        print(head)

        for key, value in sorted(log_dict.items(), key=lambda x: x[0]):
            print(f'{key:<{self.key_width}s}', end=' ')
            for level in self.log_levels:
                if level in value.keys():
                    print(f'{str(value[level]):<{self.value_width}s}', end=' ')
                else:
                    print(f'{'0':<{self.value_width}s}', end=' ')
            print()

        print(f'{" ":<{self.key_width}s}', end=' ')
        for value in level_count.values():
            print(f'{str(value):<{self.value_width}s}', end=' ')
        else:
            print()


if __name__ == '__main__':
    arguments = get_args()
    ReportMaker(arguments.paths, arguments.report).print_report()
