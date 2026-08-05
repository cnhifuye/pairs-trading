import matplotlib.pyplot as plt


def plot_equity(
    equity,
    filename="equity_curve.png"
):

    plt.figure(
        figsize=(10,5)
    )

    plt.plot(
        equity.index,
        equity.values
    )

    plt.title(
        "Strategy Equity Curve"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Equity"
    )

    plt.grid(
        True
    )

    plt.tight_layout()


    plt.savefig(
        filename,
        dpi=300
    )


    plt.close()