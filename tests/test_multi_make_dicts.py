import pytest
from main import ReportMaker as RM

paths = ['tests/test_logs/test_app1.log',
         'tests/test_logs/test_app2.log',
         'tests/test_logs/test_app3.log']
log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


class TestRMMultiMakeDicts:
    """Класс тестирует метод multi_make_dicts класса ReportMaker"""
    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (len(RM(paths).multi_make_dicts()), 3),
                                 (isinstance(RM(paths).multi_make_dicts(), tuple), True),
                             ])
    def test_multi_make_dicts(self, expected_value, result):
        """Тестирует метод multi_make_dicts класса ReportMaker"""
        assert expected_value == result

    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (isinstance(RM(paths).multi_make_dicts()[0], dict), True),
                                 (all([isinstance(key, str) for key in RM(paths).multi_make_dicts()[0]]), True),
                                 (all([isinstance(value, dict) for value in
                                       RM(paths).multi_make_dicts()[0].values()]), True),
                                 ([value for value in
                                   RM(paths).multi_make_dicts()[0]['/api/v1/reviews/'].values()], [0, 20, 0, 4, 0]),
                                 ([value for value in
                                   RM([paths[0]]).multi_make_dicts()[0]['/admin/dashboard/'].values()], [0, 6, 0, 2, 0]),
                                 (len(RM(paths).multi_make_dicts()[0]), 12)
                             ])
    def test_multi_make_dicts_log_dict(self, expected_value, result):
        """Тестирует переменную log_dict метода multi_make_dicts класса ReportMaker"""
        assert expected_value == result

    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (isinstance(RM(paths).multi_make_dicts()[1], dict), True),
                                 (all([isinstance(key, str) for key in RM(paths).multi_make_dicts()[1]]), True),
                                 (all([isinstance(value, int) for value in
                                       RM(paths).multi_make_dicts()[1].values()]), True),
                                 (all([level in log_levels for level in RM(paths).multi_make_dicts()[1]]), True),
                                 ([value for value in RM(paths).multi_make_dicts()[1].values()], [0, 148, 0, 40, 0]),
                                 ([value for value in RM([paths[0]]).multi_make_dicts()[1].values()], [0, 48, 0, 12, 0]),
                             ])
    def test_multi_make_dicts_level_count(self, expected_value, result):
        """Тестирует переменную level_count метода multi_make_dicts класса ReportMaker"""
        assert expected_value == result

    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (isinstance(RM(paths).multi_make_dicts()[2], int), True),
                                 (RM(paths).multi_make_dicts()[2], 188),
                                 (RM([paths[0]]).multi_make_dicts()[2], 60)
                             ])
    def test_multi_make_dicts_request_count(self, expected_value, result):
        """Тестирует переменную request_count метода multi_make_dicts класса ReportMaker"""
        assert expected_value == result
