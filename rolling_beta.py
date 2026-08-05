import numpy as np
import pandas as pd
import statsmodels.api as sm



def calculate_rolling_beta(
    y,
    x,
    window=120,
    min_periods=None
):
    """
    Calculate rolling hedge ratio (beta)
    
    Model:
        y = alpha + beta*x + error
        
    Parameters
    ----------
    y : pd.Series
        Price series of stock 1
    
    x : pd.Series
        Price series of stock 2
    
    window : int
        Rolling regression window
    
    min_periods : int
        Minimum observations required
        
    Returns
    -------
    beta : pd.Series
        Time-varying hedge ratio
    """



    if min_periods is None:
        min_periods = window



    beta = pd.Series(
        index=y.index,
        dtype=float
    )



    for i in range(
        window,
        len(y)
    ):


        y_window = (
            y.iloc[
                i-window:i
            ]
        )


        x_window = (
            x.iloc[
                i-window:i
            ]
        )



        # remove missing values

        data = pd.concat(
            [
                y_window,
                x_window
            ],
            axis=1
        ).dropna()



        if len(data) < min_periods:
            continue



        y_clean = data.iloc[:,0]

        x_clean = data.iloc[:,1]



        try:


            model = sm.OLS(

                y_clean,

                sm.add_constant(
                    x_clean
                )

            ).fit()



            beta.iloc[i] = (
                model.params.iloc[-1]
            )


        except Exception:


            beta.iloc[i] = np.nan




    # fill missing beta

    beta = beta.ffill()



    # if beginning values missing

    beta = beta.bfill()



    # avoid extreme hedge ratios

    beta = beta.clip(
        lower=0.05,
        upper=5
    )



    return beta