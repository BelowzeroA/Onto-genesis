from algo.algo_container import AlgoContainer
from algo.algorithm import Algorithm
from algo.graph_walker import GraphWalker
from algo.op_container import OperationContainer
from brain.brain import Brain
from onto.onto_container import OntoContainer


def main():

    onto_container = OntoContainer()
    onto_container.load("data/sample1.json")

    algo1 = Algorithm(onto_container=onto_container, filename='algo/patterns/because_i_know.json')
    algo2 = Algorithm(onto_container=onto_container, filename='algo/patterns/resolve_ambiguity.json')

    algo_container = AlgoContainer()
    algo_container.add_algorithm(algo1)
    algo_container.add_algorithm(algo2)

    brain = Brain(onto_container=onto_container, algo_container=algo_container)

    input = ['cross street', 'check side', 'US' ]
    graph_walker = GraphWalker(brain=brain)
    result = graph_walker.resolve(input)
    print(result)


if __name__ == '__main__':
    main()