import pytest
from main import ReportMaker as RP

paths = ['test_logs/test_app1.log', 'test_logs/test_app2.log', 'test_logs/test_app3.log']


class TestLogLevels:
    @pytest.mark.parametrize('log_levels, result',
                             [
                                 (RP(paths).log_levels, ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
                                 (RP(paths, log_levels=('ErrOr', 'debug')).log_levels, ('DEBUG', 'ERROR')),
                                 (RP(paths, log_levels=('ErROR', 'CRITICAL', 'CRiTICAL', 'ERROR')).log_levels,
                                  ('ERROR', 'CRITICAL')),
                             ])
    def test_log_levels(self, log_levels, result):
        assert log_levels == result

    @pytest.mark.parametrize('test_paths, result',
                             [
                                 (RP(paths).paths,
                                  ['test_logs/test_app1.log', 'test_logs/test_app2.log', 'test_logs/test_app3.log']),
                                 (RP([paths[1]]).paths, ['test_logs/test_app2.log']),
                             ])
    def test_paths(self, test_paths, result):
        assert test_paths == result

    @pytest.mark.parametrize('name, result',
                             [
                                 (RP(paths).report_name, ' '),
                                 (RP(paths, report_name='handlers').report_name, 'handlers'),
                                 (RP(paths, report_name=1).report_name, '1'),
                             ])
    def test_report_name(self, name, result):
        assert name == result

    @pytest.mark.parametrize('name, result',
                             [
                                 (RP(paths).module_name, 'django.request'),
                                 (RP(paths, module_name='fiction').module_name, 'fiction'),
                                 (RP(paths, module_name=1).module_name, '1'),
                             ])
    def test_module_name(self, name, result):
        assert name == result
