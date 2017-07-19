from onto_container import OntoContainer
from clause import Clause


class OntoResolver:
    def __init__(self, container):
        self.container = container
        self.items = {}

    def get_reply(self, clause):
        if clause.intent == "whether":
            return self.resolve_yes_no_reply(clause)
        if clause.intent == "howto":
            return self.resolve_howto_reply(clause)

    def resolve_yes_no_reply(self, clause):
        if clause.predicate != "":
            predicate_node = self.container.find_node(clause.predicate)
            if predicate_node is None:
                return "no"

    def resolve_howto_reply(self, clause):
        if clause.predicate != "":
            predicate_node = self.container.find_node(clause.predicate)
            if predicate_node is None:
                return "no"


