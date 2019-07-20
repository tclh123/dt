import redis

from dt.common.suite.impl.bank import Bank as BankModel, BankOutput

# for test
from dt.config import REDIS_HOST, REDIS_PASSWORD


class Bank(BankModel):
    '''
    use a redis hash to simulate bank accounts
    '''
    def __init__(self, *a, **kw):
        super().__init__(self, *a, **kw)

        host = '{release_name}-master.{namespace}.svc.{cluster_domain}'.format(
                release_name=self.api.release_name,
                namespace=self.api.namespace,
                cluster_domain=self.api.cluster_domain)

        # now for testing. we will get those connection infos from k8s api
        self.host = REDIS_HOST
        self.password = REDIS_PASSWORD
        self.red = None

        self.bank_name = 'bank1'
        self.n = 0

    def get_client(self):
        client = redis.Redis(host=self.host, port=6379, password=self.password, db=0)
        client.set_response_callback('HGET', int)
        client.set_response_callback('HMGET', lambda l: [int(i) for i in l])
        return client

    def init(self, balances):
        self.n = len(balances)
        self.keys = [str(i) for i in range(self.n)]

        client = self.get_client()
        for i, balance in zip(self.keys, balances):
            client.hset(self.bank_name, i, balance)

    def read(self):
        client = self.get_client()
        # hmget is atomic
        balances = client.hmget(self.bank_name, self.keys)
        return BankOutput(balances=balances, ok=True)

    def transfer(self, from_account, to_account, amount):
        client = self.get_client()
        from_account = str(from_account)
        to_account = str(to_account)

        def func(pipe):
            from_value = pipe.hget(self.bank_name, from_account)
            if from_value < amount:
                return BankOutput(ok=False)
            pipe.multi()
            pipe.hincrby(self.bank_name, from_account, -amount)
            pipe.hincrby(self.bank_name, to_account, amount)
            return BankOutput(ok=True)

        return client.transaction(func, from_account, to_account, value_from_callable=True)
