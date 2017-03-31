from util import Singleton
import logging
import abc


logger = logging.getLogger(__name__)

@Singleton
class MDFS:

    def __init__(self):
        self.adapter = None
        self.listeners = dict()
        logger.info("Initalized feed server")

    def setAdapter(self, adapter):
        logging.info("settng {adapter} in feed server".format(adapter=adapter))
        self.adapter = adapter

    def start(self):
        logging.info("starting feed server")
        self.adapter.start()

    def stop(self):
        logging.info("stopping feed server")
        self.adapter.stop()

    def subscribe(self, symbol, listner):
        logging.info("subscribing {symbol}".format(symbol=symbol))
        if not symbol in self.listeners:
            self.listeners = list()
            self.adapter.subscribe(symbol)
        self.listeners.append(listner)

    def unsubscribe(self, symbol, listner):
        logging.info("unsubscribing {symbol}".format(symbol=symbol))
        if symbol in self.listeners:
            l = self.listeners[symbol]
            l.remove(listner)
            if len(l) == 0:
                del self.listeners[symbol]
                self.adapter.unsubscribe(symbol)
        else:
            logging.info("{symbol} not found in feed".format(symbol=symbol))


class MarketDataLitener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def onTick(self, tick):
        return


class FeedAdapter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def stop(self):
        return

    @abc.abstractmethod
    def subscribe(self, symbol):
        return

    @abc.abstractmethod
    def unsubscribe(self, symbol):
        return

    @abc.abstractmethod
    def onTick(self, tick):
        return
