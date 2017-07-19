from onto_container import OntoContainer
from clause import Clause
from onto_resolver import OntoResolver

container = OntoContainer()
container.load("vardex.json")

clause = Clause()
clause.load("sample_query.json")

resolver = OntoResolver(container)
reply = resolver.get_reply(clause)
print(reply)