from algo.algo_container import AlgoContainer
from algo.graph_walker import GraphWalker
from onto_container import OntoContainer


def main():
    onto_container = OntoContainer()
    onto_container.load("onto/sample1.json")

    algo_container = AlgoContainer(onto_container=onto_container)
    algo_container.load("algo/patterns/sample1.json")

    input = ['cross street']
    graph_walker = GraphWalker(onto_container=onto_container, algo_container=algo_container)
    result = graph_walker.resolve(input)
    print(result)


if __name__ == '__main__':
    main()