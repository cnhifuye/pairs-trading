import numpy as np
import pandas as pd



class RiskManager:


    def __init__(

        self,

        target_vol=0.10,

        max_position=1.0,

        drawdown_limit=0.10

    ):


        self.target_vol = target_vol

        self.max_position = max_position

        self.drawdown_limit = drawdown_limit



    def volatility_scaling(

        self,

        returns,

        position

    ):


        """

        volatility targeting

        """


        annual_vol = (

            returns
            .rolling(60)
            .std()

            *

            np.sqrt(252)

        )


        scale = (

            self.target_vol

            /

            annual_vol

        )


        scale = scale.clip(

            0,

            2

        )


        adjusted_position = (

            position

            *

            scale

        )


        return adjusted_position





    def drawdown_control(

        self,

        equity,

        position

    ):


        peak = (

            equity
            .cummax()

        )


        drawdown = (

            equity
            /
            peak

            -

            1

        )


        adjusted = position.copy()



        adjusted[

            drawdown < -self.drawdown_limit

        ] *= 0.5



        return adjusted




    def apply(

        self,

        returns,

        position

    ):


        equity = (

            1+returns.fillna(0)

        ).cumprod()



        position = self.volatility_scaling(

            returns,

            position

        )


        position = self.drawdown_control(

            equity,

            position

        )


        position = position.clip(

            -self.max_position,

            self.max_position

        )


        return position