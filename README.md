![logo](https://raw.githubusercontent.com/Asconius/media/master/trading-bot/logo.png)

![Python application](https://github.com/Asconius/trading-bot/workflows/Python%20application/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Asconius_trading-bot&metric=alert_status)](https://sonarcloud.io/dashboard?id=Asconius_trading-bot)
[![codecov](https://codecov.io/gh/Asconius/trading-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/Asconius/trading-bot)

# Trading Bot
Trading Bot is a software in which trading strategies can be tested for- and backwards, optimized and executed
## Installation
### Database
The database can be created with the following command. The database must then be added to the database subdirectory in the project directory
```python
import sqlite3
sqlite3.connect('tradingbot.db')
```
### Enviroment Variables
The following command must be used to insert the [Alpha Vantage API key][cb956311] into the environment variables in Windows
```batch
setx ALPHA_VANTAGE "API key" /m
```
### Start Batch
The following command can be used to run the application and start the scheduler
```batch
start cmd.exe /k "cd path to project dir\trading-bot & py -m venv env & env\Scripts\activate & pip install -r requirements.txt & set FLASK_APP=src\main.py & flask run"
timeout /t 10
powershell.exe -noprofile -command "Invoke-WebRequest -Uri http://127.0.0.1:5000/process/start/schedule"
```
### Web GUI
Open your web browser and type http:// 127.0.0.1:5000/ in the address bar.

  [cb956311]: https://www.alphavantage.co/support/#api-key "Alpha Vantage API key"
