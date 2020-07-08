![Logo](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABLpJREFUeNrsXe1x2zAMpX3+n3SCaIN4gygT1BvEnaDewPIEdSaIuoGzgb2BuoE8Qe0JUuIC3zmpRUr8kMD44Q6nO0uiQDyBACkCHr29vSmQHBpDBQAEBEAACAiAfA2apCz8aDSa6gNxxj/VmisdOVYApF8gCn2Ya75rOL/Xh1IDUyTXt5TmIWwRmyYgLhABM0vJYpIBhMHYar7peOtRc54KKEkAosEgH1E5gHEOylT3tUaUFYZKDzAU31si7A1jHbk+PARo6oHbAiCeNG/huFfMe8+24ENaWMjBMFy9avlnZ9fe8tD0vcmX6OtvAYgfICYBv2n5D5+uJ4X/bbpBXz/CkBWHdp/BYIXTb7tkVx8StpDG4cc0zMFC4tGNVvziAhgLzxB5UEphLWtnCHt/sc+gGTxZBTn4paUtDFmeQxaFqi+Bmvuh+1sCED9AyALqAMMQLZ9klwIB+JAOxAoMMaGbSwcjGaeuFUlL7s8eTTxzGwqAhAOFoqeVw60rvlcBkPCgFPrw2DJaomseU/tqOEp156J29mt9+GkYohYp9ivlieHB8RwAAQEQAAICIAAEJDzs5XUmWmE9benskzLVvGGOvq3XPctTMW+8lmgIkK7MyijpdvBFJt1kTrrtCARZxBoKb82kq9sogDAYFZTcmasuoAAMYaC0jbJo6foeMZAz3bMO/Z26pgXe8GC8sOnbGPZ2+Hz6m9+Ag25ve1Xzhvf9wqfw/8lyuf0zsqd1UMNTl/DuKzLPxWofK7FZSGXwHUlsGhjAYjJlzmXZa51lnZdOuGGTI18AjIsjTs0jSxPdsW47r2VlhnN76fubBgalVObUCCdAcksYDLJPFTrr1nUrqdNQJT2vPLB8Tjqa9NTRQtnzyte64+uBgBAj3zj2G6eZ3rKlMueW0znaOF3zW9qbRUiTbxzZ/LeqfZL/qePbPkCRKt84Umcz5Zbkr/ierSk0/MryxbKQUsnOKxcr3zjC20chndi8cunyxbCQudC2kpAvBiAzoW0lIV8MQG6EtpWEfEEBiRkZXYN8wQGRXv4I5ZlAIgDZCW0rCfliAFIKbSsJ+WIAQt8BjgHaOao4311EyxccEOl55dLli+LUpeeVS5ZvHLHTovPKpco3jtzpQgnOK5co36SHTm/1IeePOrT2k3+6hM5vhvquLk2+SY8dP2UYSZ3Fi5APM/UrmKmDAAgAAQGQ6yARVUm51NJ0YDEqCSWdpJSJJTAeYB9yhqwNZJAFSKnCLIm70lEJ+cMXEYDwMnYxoAhissHERFm81X81wKNXkrLBRIW9Z6uvrz08jp4hrmqpuGL8vPq6RZT1P5nG1AwBaqtQvolqF0BMS9EzrvIAujzRJd3kQQGxlMigPa0LqL45alOGfb8m3dqcusm5Lvm/PUAfrYN0snTUqRUQ2+z1hTJYMXy9D1Oczfvio1NrEUzOUrUlRh45MqquFI8p+wxbesIfre+pLcy0VbihB6HWVRjOvSvKsQNaKVCIFQH7/KpDLagSb7h72dhYZWILKLczF9Hq9p75lBqKtnLdxmd4A3IGzJxDOCj/I5NO5q56DfKXR5xAn13xGhdZQx2iAGiy/0F1jau9IAACAiAABARAEqJ/AgwALNJcYuOM9UMAAAAASUVORK5CYII=)

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
