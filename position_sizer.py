import numpy as np


class PositionSizer:


    def __init__(
        self,
        target_vol=0.15
    ):

        self.target_vol=target_vol



    def volatility_adjust(
        self,
        returns,
        window=60
    ):


        vol = (

            returns
            .rolling(window)
            .std()
            *
            np.sqrt(252)

        )


        scale = (

            self.target_vol
            /
            vol

        )


        scale = scale.clip(
            0,
            2
        )


        return scale



    def regime_position(
        self,
        probability,
        volatility_scale
    ):


        position=(

            probability

            *

            volatility_scale

        )


        return position.clip(
            0,
            1
        )