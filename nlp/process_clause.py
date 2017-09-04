from nlp.models.clause import *
from nlp.cleverise_api import *

clause = Clause("[чтобы] [отменить] [авторизованную заявку], нужно [следовать инструкции 1]")
api = CleveriseApi()
result = api.get_nlp_analysys(clause.source)