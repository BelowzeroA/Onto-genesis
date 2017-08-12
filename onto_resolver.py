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
                return "no predicate found"
            if "leaves" not in clause.root_node:
                return "the predicate has no leaves"
            nps = [node for node in clause.root_node["leaves"] if node["type"] == "NP"]
            onto_nodes = [self.container.find_node(node["text"]) for node in nps]
            onto_nodes.append(predicate_node)
            search_result = self.get_target_nodes(onto_nodes)
            node_attrs = max(search_result, key=lambda p: p["weight"])
            if node_attrs:
                node = self.container.find_node_by_id(node_attrs["node"])
                if node["type"] == "clarification":
                    return node
                if node["type"] == "action":
                    return node

    def get_target_nodes(self, source_nodes):

        actions = self.container.find_common_targets_of_type(source_nodes, "action")
        clarifications = self.container.find_common_targets_of_type(source_nodes, "clarification")
        if not actions and not clarifications:
            return []
        else:
            actions += clarifications
        return actions
