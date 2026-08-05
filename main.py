import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore",
    message="urllib3 v2 only supports OpenSSL"
)

from fmp_loader import load_prices

from pair_selection import find_pairs

from rolling_beta import calculate_rolling_beta

from features import FeatureEngine

from signal_generator import PairSignal

from risk_manager import RiskManager

from backtester import PairBacktesterV15

from performance_analyzer import PerformanceAnalyzer

from hmm_regime import HMMRegimeDetector

from position_sizer import PositionSizer

from visualization import plot_equity


STOCKS = [
    "KO",
    "PEP",
    "SBUX"
]


INITIAL_CAPITAL = 100000



def load_data():

    print("Loading prices...")

    prices = load_prices(
        STOCKS
    )

    print(prices.head())

    return prices





def select_pair(train):


    print("\nSelecting pairs...")


    ranking = find_pairs(
        train
    )


    best = ranking.iloc[0]


    pair = best["pair"]


    a,b = pair.split("-")


    print(
        "Selected:",
        pair
    )


    return a,b





def run_window(
        train,
        test
):


    stock1,stock2 = select_pair(
        train
    )


    y=train[stock1]

    x=train[stock2]


    beta_series = calculate_rolling_beta(
        y,
        x
    )


    beta = beta_series.iloc[-1]


    print(
        "Latest beta:",
        beta
    )


    spread_train = (
        train[stock1]
        -
        beta*train[stock2]
    )


    hmm = HMMRegimeDetector()


    regime = hmm.fit_predict(
        spread_train
    )


    print(
        "\nRegime:"
    )

    print(
        regime["state"].value_counts()
    )


    # test spread

    spread_test = (
        test[stock1]
        -
        beta*test[stock2]
    )


    bt = PairBacktesterV15(

        prices=test,

        stock1=stock1,

        stock2=stock2,

        beta=beta,

        regime=regime,

        transaction_cost=0.0005

    )


    result = bt.run()


    return result





def walk_forward(
        prices
):


    window=756

    test_size=126


    results=[]



    total=len(prices)


    start=0


    count=1



    while start+window+test_size <= total:


        print(
            "\n======================"
        )

        print(
            f"Window {count}"
        )


        train=prices.iloc[
            start:start+window
        ]


        test=prices.iloc[
            start+window:
            start+window+test_size
        ]



        result=run_window(
            train,
            test
        )


        results.append(
            result
        )


        start += test_size


        count+=1



    return pd.concat(
        results
    )






def main():


    prices=load_data()


    result=walk_forward(
        prices
    )


    print(
        "\n FINAL PERFORMANCE "
    )


    performance= PerformanceAnalyzer(
        result
    )


    report = performance.summary()



    result.to_csv(
        "PC_V15_result.csv"
    )



    returns = result["return"]



    analyzer = PerformanceAnalyzer(
            returns
    )



    report = analyzer.summary()



    print(
        "\n========== PERFORMANCE =========="
    )



    for key,value in report.items():

        if value is not None:

            print(
            f"{key}: {value:.4f}"
        )



    equity = (
        1+returns
    ).cumprod()



    plot_equity(
        equity,
        "equity_curve.png"
    )


    print(
        "\nEquity curve saved."
    )


if __name__=="__main__":

    main()

