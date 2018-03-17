from algo.algo_container import AlgoContainer
from algo.graph_walker import GraphWalker
from brain.brain import Brain
from onto.onto_container import OntoContainer


def main():
    onto_container = OntoContainer()
    algo_container = AlgoContainer(onto_container=onto_container)
    brain = Brain(onto_container=onto_container, algo_container=algo_container)
    onto_container.brain = brain
    algo_container.brain = brain

    onto_container.load("data/sample1.json")
    algo_container.load("algo/patterns/sample1.json")

    input = ['cross street', 'check side' ]
    graph_walker = GraphWalker(brain=brain)
    result = graph_walker.resolve(input)
    print(result)


if __name__ == '__main__':
    main()