import numpy as np
import pandas as pd



class PairSignal:



    def __init__(
        self,
        features,
        entry=2,
        exit=0.5
    ):

        self.features = features

        self.entry = entry

        self.exit = exit




    # ==========================
    # Basic zscore signal
    # ==========================

    def zscore_signal(self):


        z = self.features["zscore"]


        position = pd.Series(
            0,
            index=z.index
        )


        # short spread

        position[
            z > self.entry
        ] = -1



        # long spread

        position[
            z < -self.entry
        ] = 1



        # exit

        position[
            abs(z) < self.exit
        ] = 0



        position = (
            position
            .replace(
                0,
                np.nan
            )
            .ffill()
            .fillna(0)
        )


        return position





    # ==========================
    # Regime filter
    # ==========================

    def regime_filter(
        self,
        position,
        regime
    ):


        filtered = position.copy()



        # high volatility regime
        # state=2 in our HMM

        filtered[
            regime["state"]==2
        ] = 0



        return filtered





    # ==========================
    # Confidence score
    # ==========================

    def confidence(self):


        z = (
            self.features["zscore"]
            .abs()
        )


        vol = (
            self.features["volatility"]
        )


        confidence = (

            z /
            (1+vol)

        )


        return confidence




    # ==========================
    # Final signal
    # ==========================

    def generate(
        self,
        regime=None
    ):


        position = self.zscore_signal()



        if regime is not None:

            position = self.regime_filter(
                position,
                regime
            )



        confidence = self.confidence()



        result = pd.DataFrame({

            "position":position,

            "confidence":confidence

        })


        return result