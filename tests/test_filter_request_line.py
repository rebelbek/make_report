import pytest
from main import ReportMaker as RM

paths = ['tests/test_logs/test_app1.log',
         'tests/test_logs/test_app2.log',
         'tests/test_logs/test_app3.log']
lines = ["2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
         "2025-03-28 12:49:37,000 ERROR django.request: Internal Server Error: /api/v1/auth/login/ [192.168.1.70] - ConnectionError: Failed to connect to payment gateway",
         "2025-03-28 12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;"]


class TestRMFilterLine:
    """Класс тестирует метод filter_request_line класса ReportMaker"""
    @pytest.mark.parametrize('expected_value, result',
                             [
                                 (all([isinstance(item, str) for item in RM(paths).filter_request_line(lines[0])]), True),
                                 (len(RM(paths).filter_request_line(lines[0])), 2),
                                 (RM(paths).filter_request_line(lines[0])[0], 'INFO'),
                                 (RM(paths).filter_request_line(lines[1])[0], 'ERROR'),
                                 (RM(paths).filter_request_line(lines[0])[1], '/admin/dashboard/'),
                             ])
    def test_filter_request_line(self, expected_value, result):
        """Тестирует метод класса filter_request_line ReportMaker"""
        assert expected_value == result
