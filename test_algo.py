from algo.graph_walker import GraphWalker
from onto_container import OntoContainer


def main():
    container = OntoContainer()
    container.load("onto/sample1.json")

    input = ['cross street', 'UK']
    graph_walker = GraphWalker(container)
    result = graph_walker.resolve(input)
    print(result)


if __name__ == '__main__':
    main()