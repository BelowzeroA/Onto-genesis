from onto_container import OntoContainer
from clause import Clause
from onto_resolver import OntoResolver

container = OntoContainer()
container.load("onto/moneycare.json")

clause = Clause()
clause.load("test/sample_query2.json")

resolver = OntoResolver(container)
reply = resolver.get_reply(clause)
print(reply)