import numpy as np
import pandas as pd



class PairBacktesterV15:


    def __init__(
    self,
    prices,
    stock1,
    stock2,
    beta,
    regime=None,
    transaction_cost=0.0005
):


        self.prices = prices

        self.stock1 = stock1

        self.stock2 = stock2

        self.beta = beta

        self.regime = regime

        self.transaction_cost = transaction_cost

        self.position = None



    # ==========================
    # Spread return
    # ==========================

    def spread_returns(self):


        r1 = (

            self.prices[self.stock1]
            .pct_change()

        )


        r2 = (

            self.prices[self.stock2]
            .pct_change()

        )


        return (

            r1
            -
            self.beta*r2

        )




    # ==========================
    # Execute trades
    # ==========================

    def execution_cost(
        self,
        position
    ):


        turnover = (

            position
            .diff()
            .abs()

        )


        cost = (

            turnover
            *
            self.transaction_cost

        )


        return cost


    def calculate_spread(self):


        spread = (

        self.prices[self.stock1]

        -

        self.beta
        *
        self.prices[self.stock2]

    )


        return spread

    def calculate_zscore(
    self,
    spread,
    window=60
):


        mean = spread.rolling(
        window
    ).mean()


        std = spread.rolling(
        window
    ).std()


        zscore = (

        spread-mean

    )/std


        return zscore

    def generate_signal(
    self,
    zscore,
    entry=2,
    exit=0
):


        position = pd.Series(
        0,
        index=zscore.index
    )


        position[zscore > entry] = -1


        position[zscore < -entry] = 1


        position[
        abs(zscore)<exit+0.1
    ] = 0


        position = position.ffill()


        return position

    def calculate_returns(
    self,
    position
):


        r1 = (
        self.prices[self.stock1]
        .pct_change()
    )


        r2 = (
        self.prices[self.stock2]
        .pct_change()
    )


        spread_return = (

        r1

        -

        self.beta*r2

    )


        strategy_return = (

        position.shift(1)

        *

        spread_return

    )


        return strategy_return


    def apply_transaction_cost(
    self,
    returns,
    position
):


        turnover = (

        position.diff()
        .abs()

    )


        cost = (

        turnover
        *
        self.transaction_cost

    )


        return returns-cost
    # ==========================
    # PnL calculation
    # ==========================

    def run(self):


        spread = self.calculate_spread()


        zscore = self.calculate_zscore(
        spread
    )


        self.position = self.generate_signal(
        zscore
    )


        returns = self.calculate_returns(
        self.position
    )


        returns = self.apply_transaction_cost(
        returns,
        self.position
    )


        equity = (
        1+returns.fillna(0)
    ).cumprod()


        return pd.DataFrame({

        "spread":spread,

        "zscore":zscore,

        "position":self.position,

        "return":returns,

        "equity":equity

    })


        return result