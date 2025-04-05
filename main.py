import argparse
import os.path


def get_args() -> argparse.Namespace:
    """Функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser('Формирует отчет из переданных логов '
                                     'и выводит в консоль')
    parser.add_argument('paths',
                        nargs='+',
                        type=str,
                        help='Пути к файлам')
    parser.add_argument('--report',
                        type=str,
                        required=False,
                        help='Название отчета')
    return parser.parse_args()


class ReportMaker:
    """
    Класс формирует и печатает отчет из лог-файлов.
    Принимает аргументы:
        Обязательные: paths
        Не обязательные: report_name, log_levels, module_name
    """

    def __init__(self,
                 paths: list[str],
                 report_name: str = None,
                 log_levels: tuple[str] = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
                 module_name: str = 'django.request'
                 ):
        self.paths: list[str] = paths
        self.report_name: str = report_name
        self.log_levels: tuple[str] = log_levels
        self.module_name: str = module_name

    def __str__(self):
        return f'Reports for logs in {self.module_name}, paths to file: {', '.join([path for path in self.paths])}'

    @property
    def paths(self) -> list[str]:
        return self._paths

    @paths.setter
    def paths(self, value: list[str]) -> None:
        for path in value:
            if not os.path.exists(path):
                raise FileNotFoundError(f'Неверно указан путь к файлу - {path}')
            if not path.endswith('.log'):
                raise TypeError(f'Неверный формат файла - {path}, должен быть ".log"')
        self._paths = value

    def filter_line(self, line: str) -> list[str]:
        """Получает необходимые значения из одной записи"""
        result: list[str] = []
        for item in line.split():
            if self.module_name == 'django.request':
                if item in self.log_levels:
                    result.append(item)
                if item.startswith('/'):
                    result.append(item)
                    continue
            else:
                #в случае доработки для других модулей
                pass
        return result

    def filter_logs(self) -> list[list[str]]:
        """Получает все записи логов из переданных файлов и фильтрует необходимые данные"""
        result: list[list[str]] = []
        for path in self.paths:
            with open(f'{path}', 'r') as f:
                for line in f.readlines():
                    if self.module_name in line:
                        result.append(self.filter_line(line))
        return result

    def make_dict(self) -> tuple[dict[str, dict[str, int]], dict[str, int], int]:
        """Создает словарь из отфильтрованных логов и подсчитывает количество запросов"""
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
        """Печатает отчет"""
        log_dict, level_count, request_count = self.make_dict()
        report_name = f'{self.report_name.upper():<25s}' if self.report_name else f'{" ":<25s}'
        title = (f'{level:<8s}' for level in self.log_levels)
        head = f'Total requests: {str(request_count)}\n\n{report_name} {' '.join(title)}'
        print(head)

        for key, value in sorted(log_dict.items(), key=lambda x: x[0]):
            print(f'{key:<25s}', end=' ')
            for level in self.log_levels:
                if level in value.keys():
                    print(f'{str(value[level]):<8s}', end=' ')
                else:
                    print(f'{'0':<8s}', end=' ')
            print()

        print(f'{" ":<25s}', end=' ')
        for value in level_count.values():
            print(f'{str(value):<8s}', end=' ')
        else:
            print()


if __name__ == '__main__':
    arguments = get_args()
    ReportMaker(arguments.paths, arguments.report).print_report()
