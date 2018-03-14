from algo.algo_container import AlgoContainer
from algo.graph_walker import GraphWalker
from onto.onto_container import OntoContainer


def main():
    onto_container = OntoContainer()
    onto_container.load("data/sample1.json")

    algo_container = AlgoContainer(onto_container=onto_container)
    algo_container.load("algo/patterns/sample1.json")

    brain = Brain(onto_container=onto_container, algo_container=algo_container)

    input = ['cross street', 'check side' ]
    graph_walker = GraphWalker(brain=brain)
    result = graph_walker.resolve(input)
    print(result)


if __name__ == '__main__':
    main()