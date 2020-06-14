from src.constants import BUY, SELL


class Analyser:
    @staticmethod
    def analyse(frame, strategy, broker, statistic=None, attempt=None, latest_date_dict=None):
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                ticker = frame.columns[j]
                date = frame.index.values[i]
                if latest_date_dict is not None and latest_date_dict[ticker] != date:
                    continue
                price = frame.iloc[i][j]
                action, number = strategy(frame, i, j, attempt)
                buy = False
                sell = False
                if action == BUY:
                    buy = broker.buy(ticker, price, number)
                elif action == SELL:
                    sell = broker.sell(ticker, price, number)
                else:
                    broker.update(ticker, price)
                if statistic is not None:
                    statistic.plot(date, ticker, price, buy, sell)
                    statistic.test(action, number, ticker, broker)
                    statistic.log(action, date, ticker, price, buy, sell)
        return statistic
