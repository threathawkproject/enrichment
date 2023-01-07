from abc import ABC, abstractmethod

class WebAnalyzer(ABC):
        @property
        def ioc(self):
            return self._ioc

        @property
        def type(self):
            return self._type

        @property
        def key(self):
            return self._key

        @abstractmethod
        def run(self):
            pass
class DockerAnalyzer(ABC):
        @property
        def ioc(self):
            return self._ioc

        @property
        def type(self):
            return self._type

        @property
        def command(self):
            return self._command

        @abstractmethod
        # for any configurations need when we run the docker contianer
        def container_configuration():
            pass
        
        # this is to build the image for the tool
        @abstractmethod
        def build_image(self):
            pass

        @abstractmethod
        # to run tool!
        # optional_args is a list for the flags and their inputs and such!
        def run(self, optional_args: list):
            pass