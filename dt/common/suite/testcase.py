import time
import random
import logging
import concurrent.futures

from dt.common.mixin.model import Model

logger = logging.getLogger(__name__)

MAX_WORKERS = 5
JOBS_PER_TICK = 100
SECS_PER_TICK = 10
JOB_CHUNKSIZE = 10

CHAOSS_PER_TICK = 1

# main daemon
# spawn subprocess(worker)
class TestCase(Model):
    def __init__(self, dt_api, model_cls):
        self.api = dt_api
        self.model = model_cls(dt_api)

    def run(self, timeout=0):
        self.setUp()

        try:
            self.main_loop(timeout)
        except Exception:
            raise
        finally:
            self.tearDown()

    def main_loop(self, timeout):
        if timeout:
            total_ticks = max(timeout // SECS_PER_TICK, 1)
        else:
            total_ticks = float('inf')

        ticks = 0
        # do work
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while True:
                self.init_model()

                futures = [executor.submit(self.work) for _ in range(JOBS_PER_TICK)]
                futures += [executor.submit(self.chaos) for _ in range(CHAOSS_PER_TICK)]
                records = []
                try:
                    for future in concurrent.futures.as_completed(futures, timeout=SECS_PER_TICK):
                        record = future.result()
                        if record:
                            records.append(record)
                except Exception:
                    logger.exception('Main loop exception on tick %s:', ticks)

                logger.info('TestCase %s of %s produce records: %s', self.__class__.__name__, self.api.chart.name,
                            records)

                # record records for analyze
                # operation records: input, output, call_time, return_time
                self.api.run_checker(self.api.record(records))

                ticks += 1
                if ticks >= total_ticks:
                    break
                time.sleep(SECS_PER_TICK)

    def get_test_funcs(self):
        for attr in dir(self):
            if attr.startswith('test_') and callable(getattr(self, attr)):
                yield getattr(self, attr)

    def random_test_func(self):
        return random.choices(list(self.get_test_funcs()))[0]

    def work(self):
        '''
        random pick test_ func
        return record dict
        '''
        func = self.random_test_func()
        return func().to_dict()

    def chaos(self):
        # TODO: chaos functions, like delete pods, inject iptables rules on k8s nodes
        pass

    def setUp(self):
        # run chart
        # FIXME: testing
        return
        res = self.api.chart.install(self.api.namespace, name=self.api.release_name,
                                     values=self.api.values, wait=True)
        logger.info('installed chart: %s', self.api.chart.name)

    def init_model(self):
        pass

    def tearDown(self):
        # purge chart
        res = self.api.chart.uninstall(self.api.release_name)
        logger.info('uninstalled chart: %s', self.api.chart.name)

        # TODO: clean PVCs, kubectl -ndttt get pvc
