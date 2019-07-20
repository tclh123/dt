from dt.common.suite.impl.bank import Bank as BankModel, BankOutput  # NOQA


class Bank(BankModel):
    def __init__(self, *a, **kw):
        super().__init__(self, *a, **kw)

    def init(self):
        pass

    def read(self):
        pass

    def transfer(self):
        pass

