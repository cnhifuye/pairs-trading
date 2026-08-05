Regime-Aware Pairs Trading Strategy

A quantitative trading framework implementing statistical arbitrage through pairs trading, dynamic hedge ratio estimation, market regime detection, and risk-controlled backtesting.

Overview

Pairs trading is a market-neutral strategy based on the assumption that historically related assets tend to maintain a long-term equilibrium relationship.

This project develops a complete research and backtesting pipeline:

Pair selection
Feature engineering
Dynamic hedge ratio estimation
Signal generation
Position sizing
Risk management
Regime detection
Performance analysis

The goal is to investigate statistical arbitrage opportunities using quantitative methods.

Strategy Framework

1. Pair Selection

Candidate asset pairs are identified based on historical relationships between assets.

The framework evaluates potential pairs using statistical features to identify assets with suitable mean-reverting behaviour.

2. Dynamic Hedge Ratio

Instead of assuming a fixed relationship between two assets, the strategy estimates a time-varying hedge ratio.

The rolling beta approach adapts to changing market conditions:

[
Spread_t = P_{A,t} - \beta_t P_{B,t}
]

3. Feature Engineering

The strategy generates quantitative features used for trading decisions, including spread-related statistics and market indicators.

4. Regime Detection

A Hidden Markov Model (HMM) is used to identify different market regimes.

The strategy adjusts behaviour depending on detected market conditions.

5. Signal Generation

Trading signals are generated based on statistical deviations of the spread.

Typical logic:

Enter long spread positions when the spread is significantly below its mean
Enter short spread positions when the spread is significantly above its mean
Exit when the spread converges

6. Position Sizing and Risk Management

The framework includes position sizing and risk controls to manage exposure.

Components include:

Position allocation
Risk limits
Exposure control

Backtesting Framework

The strategy is evaluated using historical market data.

The backtesting engine supports:

Portfolio simulation
Trade execution logic
Performance tracking

Performance Evaluation

Performance metrics include:

Total return
Annualized return
Sharpe ratio
Maximum drawdown
Volatility
Trade statistics

Project Structure

pairs_trading/
│
├── main.py
│
├── fmp_loader.py
│
├── pair_selection.py
├── rolling_beta.py
├── features.py
│
├── signal_generator.py
├── position_sizer.py
├── risk_manager.py
│
├── hmm_regime.py
│
├── backtester.py
├── performance_analyzer.py
├── visualization.py
│
└── README.md

Data Source

Market data is loaded through:

fmp_loader.py

The framework is designed to work with historical price data for quantitative research and strategy evaluation.

Future Improvements

Potential extensions:

Add transaction cost modelling
Implement walk-forward validation
Improve pair selection using cointegration tests
Expand to multi-pair portfolio optimization
Add machine learning based signal generation
Compare performance against benchmark strategies


Disclaimer

This project is developed for educational and research purposes only.

It does not represent financial advice or a recommendation to trade.

