![logo](https://raw.githubusercontent.com/Asconius/media/master/trading-bot/logo.png)

[![Python application](https://github.com/Asconius/trading-bot/workflows/Python%20application/badge.svg)](https://github.com/Asconius/trading-bot/actions?query=workflow%3A%22Python+application%22)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Asconius_trading-bot&metric=alert_status)](https://sonarcloud.io/dashboard?id=Asconius_trading-bot)
[![codecov](https://codecov.io/gh/Asconius/trading-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/Asconius/trading-bot)

# Trading Bot

Trading Bot is a software in which trading strategies can be tested for- and backwards, optimized and executed.

## Use Cases

### Optimization

Strategies are tested with different input parameters using historical data. Successful attempts are saved and used for
forward and realization.

### Forward

Strategies are applied to current data. Buy or sell orders are generated in a sample portfolio.

### Realization

Strategies are applied to current data. Buy or sell orders are generated in a depot.

## Installation

### Enviroment Variables

The following command must be used to insert the [Alpha Vantage API key][cb956311] into the environment variables in
Windows:

```batch
setx ALPHAVANTAGE_API_KEY "API key" /m
```

### Docker

The Docker image can be created with the following command:

```
docker build --build-arg alphavantage_api_key=${ALPHAVANTAGE_API_KEY} -t trading_bot_image .
```

The Docker container can be started with the following command:

```
docker run -d --name trading_bot_container --restart=always -p 80:5000 trading_bot_image
```

### Web GUI

The web gui can be opened by entering `http://localhost/` in the address bar of the browser.

[cb956311]: https://www.alphavantage.co/support/#api-key "Alpha Vantage API key"
