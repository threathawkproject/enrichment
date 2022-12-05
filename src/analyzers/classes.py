from abc import ABC, abstractmethod

class WebAnalyzer(ABC):
        @property
        def ioc(self):
            return self._ioc

        @property
        def key(self):
            return self._key

        @abstractmethod
        def run(self):
            pass