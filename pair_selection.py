import numpy as np
import pandas as pd

import statsmodels.api as sm

from itertools import combinations

from statsmodels.tsa.stattools import coint



def hedge_ratio(y,x):

    model=sm.OLS(
        y,
        sm.add_constant(x)
    ).fit()

    return model.params.iloc[1]



def half_life(spread):

    lag=spread.shift(1)

    diff=spread.diff()


    df=pd.concat(
        [diff,lag],
        axis=1
    ).dropna()


    model=sm.OLS(
        df.iloc[:,0],
        sm.add_constant(df.iloc[:,1])
    ).fit()


    lam=model.params.iloc[1]


    if lam>=0:
        return np.inf


    return -np.log(2)/lam





def evaluate_pair(prices,a,b):


    x=prices[b]

    y=prices[a]


    corr=y.corr(x)



    beta=hedge_ratio(
        y,
        x
    )


    spread=y-beta*x


    coint_stat,pvalue,_=coint(
        y,
        x
    )


    hl=half_life(
        spread
    )


    if hl==np.inf:
        return None



    volatility=spread.std()



    score=(

        0.3*corr

        +

        0.4*(-np.log10(pvalue))

        +

        0.2*(1/hl)

        +

        0.1*(1/volatility)

    )


    return {


        "pair":f"{a}-{b}",

        "correlation":corr,

        "beta":beta,

        "coint_pvalue":pvalue,

        "half_life":hl,

        "score":score

    }






def find_pairs(prices):


    results=[]


    pairs=combinations(
        prices.columns,
        2
    )


    for a,b in pairs:


        result=evaluate_pair(
            prices,
            a,
            b
        )


        if result:

            results.append(
                result
            )


    df=pd.DataFrame(
        results
    )


    return df.sort_values(
        "score",
        ascending=False
    )