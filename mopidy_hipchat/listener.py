from abc import abstractmethod

class CommandListener():

    @abstractmethod
    def command(self):
        pass

    @abstractmethod
    def action(self, msg):
        pass