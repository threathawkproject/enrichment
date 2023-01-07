from src.analyzers.classes import WebAnalyzer
from emailrep import EmailRep


class EmailRepClass(WebAnalyzer):
    ioc = ""
    key = ""

    def run(self, ioc, type):
        self.ioc = ioc
        self.key = "wvhc9xxi9ts7u1j6z494udv334grknewrythtcssvc5rjaqb"
        emailrep = EmailRep(self.key)

        try:
            results = emailrep.query(self.ioc)
            return results
        except Exception as e:
            return None
