import pytest
from main import ReportMaker as RM

paths = ['tests/test_logs/test_app1.log',
         'tests/test_logs/test_app2.log',
         'tests/test_logs/test_app3.log']
log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


class TestRMFilterLogs:
    """Класс тестирует метод filter_logs класса ReportMaker"""
    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (all([isinstance(item, list) for item in RM(paths).filter_logs()]), True),
                                 (all([isinstance(item, str) for item in RM(paths).filter_logs()[0]]), True),
                                 (all([len(item) == 2 for item in RM(paths).filter_logs()]), True),
                                 (len(RM(paths).filter_logs()), 188),
                                 (len(RM(paths[:2]).filter_logs()), 122),
                                 (len(RM([paths[0]]).filter_logs()), 60),
                                 (len(RM([paths[1]]).filter_logs()), 62),
                                 (len(RM([paths[2]]).filter_logs()), 66),
                                 (all([level in log_levels for level in [item[0] for item in RM(paths).filter_logs()]]), True),
                                 (all([uri.startswith('/') for uri in [item[1] for item in RM(paths).filter_logs()]]), True),
                             ])
    def test_filter_logs(self, expected_value, result):
        """Тестирует метод filter_logs класса ReportMaker"""
        assert expected_value == result

    def test_filter_logs_exceptions(self):
        """Тестирует метод filter_logs класса ReportMaker на исключения"""
        with pytest.raises(ValueError):
            RM(paths, module_name='django.security').filter_logs()