import pytest
from main import ReportMaker as RM

paths = ['tests/test_logs/test_app1.log', 'tests/test_logs/test_app2.log', 'tests/test_logs/test_app3.log']


class TestReportMakerAttr:
    @pytest.mark.parametrize('test_paths, result',
                             [
                                 (RM(paths).paths,
                                  ['tests/test_logs/test_app1.log', 'tests/test_logs/test_app2.log', 'tests/test_logs/test_app3.log']),
                                 (RM([paths[1]]).paths, ['tests/test_logs/test_app2.log']),
                             ])
    def test_paths(self, test_paths, result):
        assert test_paths == result

    @pytest.mark.parametrize('expected_exception, value',
                             [
                                 (TypeError, 'tests/test_logs/test_app1.log'),
                                 (TypeError, ['tests/test_logs/test.txt']),
                                 (FileNotFoundError, ['some_path.log']),
                             ])
    def test_paths_exceptions(self, expected_exception, value):
        with pytest.raises(expected_exception):
            RM(value)

    @pytest.mark.parametrize('log_levels, result',
                             [
                                 (RM(paths).log_levels, ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
                                 (RM(paths, log_levels=('ErrOr', 'debug')).log_levels, ('DEBUG', 'ERROR')),
                                 (RM(paths, log_levels=('ErROR', 'CRITICAL', 'CRiTICAL', 'ERROR')).log_levels,
                                  ('ERROR', 'CRITICAL')),
                             ])
    def test_log_levels(self, log_levels, result):
        assert log_levels == result

    @pytest.mark.parametrize('expected_exception, value',
                             [
                                 (ValueError, ''),
                                 (ValueError, ('something', 'info')),
                                 (TypeError, (1, 'CRITICAL'))
                             ])
    def test_log_levels_exceptions(self, expected_exception, value):
        with pytest.raises(expected_exception):
            RM(paths, log_levels=value)

    @pytest.mark.parametrize('name, result',
                             [
                                 (RM(paths).report_name, ' '),
                                 (RM(paths, report_name='handlers').report_name, 'handlers'),
                                 (RM(paths, report_name=1).report_name, '1'),
                             ])
    def test_report_name(self, name, result):
        assert name == result

    @pytest.mark.parametrize('name, result',
                             [
                                 (RM(paths).module_name, 'django.request'),
                                 (RM(paths, module_name='fiction').module_name, 'fiction'),
                                 (RM(paths, module_name=1).module_name, '1'),
                             ])
    def test_module_name(self, name, result):
        assert name == result
