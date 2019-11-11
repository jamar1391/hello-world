import numpy as np
import matplotlib.pyplot as plt

class Market:
    def __init__(self,wallet=10000,contracts=0,loss_cap=-2000,margin=500,
                 commission=2,ave_ret=2,stdev=4,point=12.5):

        self.wallet      = wallet
        self.contracts   = contracts
        self._loss_cap   = loss_cap
        self._margin     = margin
        self._commission = commission
        self._ave_ret    = ave_ret
        self._stdev      = stdev
        self._point      = point

    def margin_check(self):
        x = self.wallet/(self.contracts+1)
        if x > 502:
            return True
        else:
            return False


    def open_contract(self,x):
        for i in range(x):
            if self.margin_check():
                self.contracts += 1
                self.wallet -= self._commission
            else:
                print("You need more in your wallet to cover the margin for an additional contract.")
                break

    def tick(self):
        x = np.random.normal(self.ave_ret,self.stdev,self.contracts)
        return x

    def close_contract(self):
        if self.contracts >= 1:
            self.contracts -= 1
            self.wallet -= self.commission


joe = Market()

joe.open_contract(19)
lst = []

for i in range(joe.contracts):

# returns = np.random.normal(avg_return,std_dev,contracts)
# money = []

# for i in returns:
#     money.append((i*point)-commission)


