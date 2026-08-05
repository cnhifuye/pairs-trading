import numpy as np
import pandas as pd


class PerformanceAnalyzer:


    def __init__(
        self,
        returns,
        benchmark=None
    ):

        self.returns = (
            returns
            .dropna()
        )

        self.benchmark = benchmark



    def calculate_alpha_beta(self):


        if self.benchmark is None:

            return np.nan, np.nan



        df = pd.concat(
            [
                self.returns,
                self.benchmark
            ],
            axis=1
        ).dropna()



        y = df.iloc[:,0]

        x = df.iloc[:,1]


        beta = (
            np.cov(
                y,
                x
            )[0,1]
            /
            np.var(x)
        )


        alpha = (
            y.mean()
            -
            beta*x.mean()
        )


        return alpha*252, beta



    def information_ratio(self):


        if self.benchmark is None:

            return np.nan


        active = (
            self.returns
            -
            self.benchmark
        )


        return (
            active.mean()
            /
            active.std()
            *
            np.sqrt(252)
        )



    def summary(self):


        total_return = (
            (1+self.returns)
            .prod()
            -1
        )


        cagr = (
            1+total_return
        )**(
            252/
            len(self.returns)
        )-1



        vol = (
            self.returns.std()
            *
            np.sqrt(252)
        )



        sharpe = (
            self.returns.mean()
            /
            self.returns.std()
            *
            np.sqrt(252)
        )



        equity = (
            1+self.returns
        ).cumprod()


        drawdown = (
            equity
            /
            equity.cummax()
            -1
        )


        max_dd = drawdown.min()



        alpha,beta = (
            self.calculate_alpha_beta()
        )


        ir = (
            self.information_ratio()
        )


        return {


            "Total Return":
            total_return,


            "CAGR":
            cagr,


            "Volatility":
            vol,


            "Sharpe":
            sharpe,


            "Max Drawdown":
            max_dd,


            "Alpha":
            alpha,


            "Beta":
            beta,


            "Information Ratio":
            ir

        }