import json
from urllib.request import Request, urlopen
import config

class CleveriseApi:

    def get_clause_parsed(self):
        self.server_addr = "http://api.itsgreat.ru/"

    def compose_url(self, method):
        return self.server_addr + method + "?token=" + config.cleverise_token

    def cleverise_command(self, method, cmd, msg_text):
        try:
            url = self.compose_url(method, cmd)
            binary_data = msg_text.encode('utf-8')
            request = Request(url, data=binary_data)
            raw_response = urlopen(request).read()
            return json.loads(raw_response.decode())
        except Exception as e:
            print(e)
            return None