import pytest
from main import ReportMaker as RP

paths = ['tests/test_logs/test_app1.log', 'tests/test_logs/test_app2.log', 'tests/test_logs/test_app3.log']


class TestReportMakerAttr:
    @pytest.mark.parametrize('test_paths, result',
                             [
                                 (RP(paths).paths,
                                  ['tests/test_logs/test_app1.log', 'tests/test_logs/test_app2.log', 'tests/test_logs/test_app3.log']),
                                 (RP([paths[1]]).paths, ['tests/test_logs/test_app2.log']),
                             ])
    def test_paths(self, test_paths, result):
        assert test_paths == result

    @pytest.mark.parametrize('expected_exception, value',
                             [
                                 (FileNotFoundError, ['some_path']),
                                 (TypeError, ['tests/test_logs/test.txt'])
                             ])
    def test_paths_errors(self, expected_exception, value):
        with pytest.raises(expected_exception):
            RP(value)

    @pytest.mark.parametrize('log_levels, result',
                             [
                                 (RP(paths).log_levels, ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
                                 (RP(paths, log_levels=('ErrOr', 'debug')).log_levels, ('DEBUG', 'ERROR')),
                                 (RP(paths, log_levels=('ErROR', 'CRITICAL', 'CRiTICAL', 'ERROR')).log_levels,
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
    def test_log_levels_errors(self, expected_exception, value):
        with pytest.raises(expected_exception):
            RP(paths, log_levels=value)

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
