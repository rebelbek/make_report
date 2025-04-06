import pytest
from main import ReportMaker

paths = ['test_logs/test_app1.log', 'test_logs/test_app2.log', 'test_logs/test_app3.log']

class TestLogLevels:
    @pytest.mark.parametrize('log_levels, result',
                             [(ReportMaker(paths).log_levels, ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
                              (ReportMaker(paths, log_levels=('ErrOr', 'debug')).log_levels, ('DEBUG', 'ERROR')),
                              (ReportMaker(paths, log_levels=('ErROR', 'CRITICAL', 'CRiTICAL', 'ERROR')).log_levels, ('ERROR', 'CRITICAL')),
                              ])
    def test_log_levels(self, log_levels, result):
        assert log_levels == result

    def test_paths(self):
        pass