import numpy as np

from networks.dssm_network import DssmNetwork


def main():

    dssm = DssmNetwork(5, 10, (20, 20))
    dataset = [
        (np.array([1,0,1,1,0]), np.array([1,0,1,1,0,0,0,1,1,0])),
        (np.array([1,0,0,1,0]), np.array([1,0,0,1,0,0,0,1,1,0]))
    ]
    dssm.fit(dataset)



if __name__ == '__main__':
    main()