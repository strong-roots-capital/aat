import os
import os.path
from aat import Strategy, Event
from pprint import pprint


class ReadOnlyStrategy(Strategy):
    def __init__(self, *args, **kwargs) -> None:
        super(ReadOnlyStrategy, self).__init__(*args, **kwargs)

    async def onStart(self, event: Event) -> None:
        pprint(self.instruments())
        pprint(self.positions())

        for i in self.instruments():
            await self.subscribe(i)

    async def onTrade(self, event: Event) -> None:
        pprint(event)

    async def onOrder(self, event):
        pprint(event)

    async def onExit(self, event: Event) -> None:
        print('Finishing...')


if __name__ == "__main__":
    from aat import TradingEngine, parseConfig
    cfg = parseConfig(['--trading_type', 'backtest',
                       '--load_accounts',
                       '--exchanges', 'aat.exchange.generic:CSV,{}'.format(os.path.join(os.path.dirname(__file__), 'data', 'aapl.csv')),
                       '--strategies', 'aat.strategy.sample.readonly:ReadOnlyStrategy'
                       ])
    print(cfg)
    t = TradingEngine(**cfg)
    t.start()
