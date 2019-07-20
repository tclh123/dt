import logging

from dt.common.mixin.model import Model
from dt.common.mixin.yaml import YamlMixin
from dt.common.chart import Chart
from dt.common.api import DtApi
from dt.common.util import import_class
from dt.config import SUITE_PATHS

logger = logging.getLogger(__name__)


# main entry point
class Suite(Model, YamlMixin):
    __fields__ = [
        'name',                 # suite name
        'chart',                # chart name
        'values',               # helm values
        'timeout',              # default is 0, means forever
        'testcase_cls',         # python class path for the testcase class
        'testcase_model_cls',   # python class path for the testcase model class
    ]

    # TODO: use dir pattern
    __yaml_dirs__ = SUITE_PATHS

    def __init__(self, **kw):
        super().__init__(**kw)

    def get_testcase(self):
        chart = Chart.from_yaml(Chart.load_yaml(self.chart))
        logger.debug('get chart: %s', chart)
        dt_api = DtApi(chart=chart, values=self.values)

        testcase_cls = import_class(self.testcase_cls)
        testcase_model_cls = import_class(self.testcase_model_cls)
        testcase = testcase_cls(dt_api, testcase_model_cls)
        return testcase

    def run(self, timeout=None):
        testcase = self.get_testcase()
        self.timeout = timeout if timeout is not None else self.timeout
        return testcase.run(self.timeout)
