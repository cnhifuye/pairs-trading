import warnings

import numpy as np
import pandas as pd

from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler


# hide numerical warnings from hmmlearn
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning
)


class HMMRegimeDetector:


    def __init__(
        self,
        n_states=3
    ):

        self.n_states = n_states


        self.model = GaussianHMM(

            n_components=n_states,

            covariance_type="diag",

            n_iter=100,

            tol=0.01,

            min_covar=1e-3,

            random_state=42

        )


        self.scaler = StandardScaler()



    # =====================================
    # Feature Engineering
    # =====================================

    def create_features(
        self,
        spread
    ):


        df = pd.DataFrame(
            index=spread.index
        )


        # return

        df["return"] = (
            spread
            .pct_change()
        )


        # volatility

        df["volatility"] = (

            spread
            .rolling(20)
            .std()

        )


        # momentum

        df["momentum"] = (

            spread
            .diff(20)

        )



        # replace bad values

        df = df.replace(

            [
                np.inf,
                -np.inf
            ],

            np.nan

        )


        df = df.dropna()



        return df



    # =====================================
    # Fit HMM
    # =====================================

    def fit_predict(
        self,
        spread
    ):


        features = self.create_features(
            spread
        )


        if len(features) < 50:


            return self.empty_result(
                features
            )



        X = features.values



        # scaling

        X = self.scaler.fit_transform(
            X
        )



        # clip extreme values

        X = np.clip(

            X,

            -5,

            5

        )



        try:


            # train HMM

            self.model.fit(
                X
            )


            states = self.model.predict(
                X
            )


            probabilities = (
                self.model.predict_proba(
                    X
                )
            )



        except Exception:


            # fallback

            states = np.zeros(
                len(X),
                dtype=int
            )


            probabilities = np.zeros(

                (
                    len(X),
                    self.n_states
                )

            )


            probabilities[:,0] = 1



        # =================================
        # Result dataframe
        # =================================

        result = pd.DataFrame(

            index=features.index

        )



        result["state"] = states



        for i in range(
            self.n_states
        ):


            result[

                f"prob_{i}"

            ] = probabilities[:,i]



        # =================================
        # dominant regime
        # =================================


        best_state = (

            result["state"]

            .value_counts()

            .idxmax()

        )



        result["best_state"] = (

            best_state

        )


        result["regime_probability"] = (

            result[
                f"prob_{best_state}"
            ]

        )



        self.print_summary(
            result
        )



        return result




    # =====================================
    # Empty fallback
    # =====================================

    def empty_result(
        self,
        df
    ):


        result = pd.DataFrame(
            index=df.index
        )


        result["state"] = 0


        for i in range(
            self.n_states
        ):

            result[
                f"prob_{i}"
            ] = (
                1
                if i == 0
                else 0
            )


        result["best_state"] = 0


        result["regime_probability"] = 1



        return result




    # =====================================
    # Clean output
    # =====================================

    def print_summary(
        self,
        result
    ):


        counts = (

            result["state"]

            .value_counts(normalize=True)

            .sort_index()

            *100

        )



        print(
            "\nHMM Regime Summary"
        )

        print(
            "------------------"
        )


        for state, value in counts.items():

            print(

                f"Regime {state}: "
                f"{value:.1f}%"

            )


        print()
