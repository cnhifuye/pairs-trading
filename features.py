import numpy as np
import pandas as pd



class FeatureEngine:


    def __init__(
        self,
        spread
    ):

        self.spread = spread



    # ==========================
    # Rolling Z-score
    # ==========================

    def zscore(
        self,
        window=60
    ):


        mean = (
            self.spread
            .rolling(window)
            .mean()
        )


        std = (
            self.spread
            .rolling(window)
            .std()
        )


        z = (

            self.spread
            -
            mean

        ) / std


        return z



    # ==========================
    # Rolling volatility
    # ==========================

    def volatility(
        self,
        window=20
    ):


        vol = (

            self.spread
            .rolling(window)
            .std()

        )


        return vol




    # ==========================
    # Momentum
    # ==========================

    def momentum(
        self,
        window=20
    ):


        mom = (

            self.spread
            -
            self.spread.shift(window)

        )


        return mom




    # ==========================
    # Spread return
    # ==========================

    def returns(self):


        return (
            self.spread
            .pct_change()
        )




    # ==========================
    # Moving average
    # ==========================

    def moving_average(
        self,
        window=60
    ):


        return (

            self.spread
            .rolling(window)
            .mean()

        )




    # ==========================
    # Generate all features
    # ==========================

    def generate(
        self,
        z_window=60,
        vol_window=20,
        momentum_window=20
    ):


        df = pd.DataFrame(
            index=self.spread.index
        )



        df["spread"] = self.spread



        df["zscore"] = (

            self.zscore(
                z_window
            )

        )



        df["volatility"] = (

            self.volatility(
                vol_window
            )

        )



        df["momentum"] = (

            self.momentum(
                momentum_window
            )

        )



        df["return"] = (

            self.returns()

        )



        df["ma"] = (

            self.moving_average(
                z_window
            )

        )



        # remove invalid rows

        df = df.replace(
            [np.inf,-np.inf],
            np.nan
        )


        df = df.dropna()



        return df