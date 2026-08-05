import requests
import pandas as pd
import time


API_KEY = "j37pHde9bFahF9DUBkrzIUeGWNbIcY38"


START_DATE = "2015-01-01"
END_DATE = "2025-01-01"



def get_price(symbol):

    url = (
        "https://financialmodelingprep.com/stable/"
        "historical-price-eod/full"
    )


    params = {

        "symbol": symbol,

        "from": START_DATE,

        "to": END_DATE,

        "apikey": API_KEY

    }


    print("Downloading", symbol)

    time.sleep(1)


    response = requests.get(
        url,
        params=params
    )


    print(response.status_code)


    try:

        data=response.json()

    except Exception:

        print(response.text[:500])

        raise Exception(
            f"Invalid JSON for {symbol}"
        )


    if not isinstance(data,list):

        print(data)

        raise Exception(
            f"FMP failed for {symbol}"
        )


    df = pd.DataFrame(
    data
    )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    df = df.sort_values(
        "date"
    )



    price = df.set_index(
        "date"
    )["close"]



    price.name = symbol


    return price

def load_prices(tickers):


    data=[]


    for ticker in tickers:


        try:

            price = get_price(
                ticker
            )


            data.append(
                price
            )


        except Exception as e:


            print(
                f"Skip {ticker}: {e}"
            )


            continue



    prices = pd.concat(
        data,
        axis=1
    )


    prices = prices.dropna()


    return prices
