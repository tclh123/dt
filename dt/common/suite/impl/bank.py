import time
import random
import logging

from dt.common.mixin.model import Model
from dt.common.suite.testcase import TestCase
from dt.common.suite.model import TestCaseModel
from dt.common.suite.record import Record

logger = logging.getLogger(__name__)

BANK_ACCOUNT_NUM = 5
INIT_BALANCE = 10000
MAX_TRANSFER_AMOUNT = 1000


class BankTestCase(TestCase):
    def __init__(self, dt_api, model_cls):
        self.api = dt_api
        self.bank = self.model = model_cls(api=dt_api)
        self.n = BANK_ACCOUNT_NUM
        self.time_ns = None

    def setUp(self):
        super().setUp()
        self.init_model()

    def init_model(self):
        balances = [INIT_BALANCE for _ in range(self.n)]
        self.bank.init(balances)
        self.time_ns = time.time_ns()

    def gen_timestamp(self):
        return time.time_ns() - self.time_ns

    def test_read(self):
        call_time = self.gen_timestamp()
        output = self.bank.read()
        return_time = self.gen_timestamp()
        return Record(input=BankInput(op=0), call_time=call_time, output=output, return_time=return_time)

    def test_transfer(self):
        from_account = random.randint(0, self.n-1)
        to_account = random.randint(0, self.n-1)
        amount = random.randint(1, MAX_TRANSFER_AMOUNT)

        input_ = BankInput(op=1, from_account=from_account, to_account=to_account, amount=amount)
        logger.info('test_transter %s', input_.to_dict())

        call_time = self.gen_timestamp()
        output = self.bank.transfer(from_account, to_account, amount)
        return_time = self.gen_timestamp()

        return Record(input=input_, call_time=call_time, output=output, return_time=return_time)

    def tearDown(self):
        # pass
        super().tearDown()


class BankInput(Model):
    __fields__ = [
        'op',  # 0 for read, 1 for transfer
        # args for transfer
        'from_account',
        'to_account',
        'amount',
    ]


class BankOutput(Model):
    __fields__ = [
        'balances',  # output state for read
        'ok',        # operation ok, boolean
        'unknown',   # timeout
    ]


class Bank(TestCaseModel):
    __fields__ = [
        'api',  # use api to get chart info, for example how to connect to the cluster
    ]

    def __init__(self, *a, **kw):
        super().__init__(self, *a, **kw)

        self.n = 0
        self.balances = []

    def init(self, balances):
        self.n = len(balances)
        self.balances = balances[:]

    def read(self):
        return BankOutput(balances=self.balances, ok=True)

    def transfer(self, from_account, to_account, amount):

        if self.balances[from_account] < amount:
            return BankOutput(ok=False)

        self.balances[from_account] -= amount
        self.balances[to_account] += amount

        return BankOutput(ok=True)
