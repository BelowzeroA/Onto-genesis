import json
from urllib.request import Request, urlopen
import nlp

class CleveriseApi:

    def __init__(self):
        self.server_addr = "http://api.itsgreat.ru/"

    def get_clause_parsed(self):
        self.server_addr = "http://api.itsgreat.ru/"

    def compose_url(self, method):
        return self.server_addr + method + "?token=" + nlp.config.cleverise_token

    def cleverise_command(self, method, text):
        try:
            url = self.compose_url(method)
            binary_data = text.encode('utf-8')
            request = Request(url, data=binary_data)
            raw_response = urlopen(request).read()
            return json.loads(raw_response.decode())
        except Exception as e:
            print(e)
            return None

    def get_nlp_analysys(self, source):
        return self.cleverise_command("nlp/analyse", source)
