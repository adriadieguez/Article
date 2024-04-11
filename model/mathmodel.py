# Required packages
from Bio import Phylo
from io import StringIO
from scipy.linalg import expm
from sympy import symbols, Eq, solve
import numpy as np
import sympy as sp

class Edge:
    def __init__(self, edge, transition_matrix=None):
        self.edge = edge
        self.transition_matrix = transition_matrix

class MM:
    def __init__(self, source, target, matrix):
        self.source = source
        self.target = target
        self.matrix = matrix

def get_matrix_from_dict(d):
    """
    Returns a 4x4 matrix given a dictionary with 16 values
    """
    Q2 = np.zeros((4,4))
    coefficients = list(d.values())
    for i in range(4):
        for j in range(4):
            Q2[i,j] = coefficients[i*4+j]
    return Q2

def generate_alignment(length, distribution):
    """
    Generates an alignment of length `length` using a given `distribution`.
    """
    seq = ''
    for i in range(length):
        # Generate a random sample from the multinomial distribution
        nucleotide = np.random.choice(['A', 'G', 'C', 'T'], p=distribution)
        seq += nucleotide
    return seq

def alpha(new_distribution, Q, i, k):
    """
    Returns the parameter alpha of the Metropolis - Hastings algorithm
    """
    return min(1, (new_distribution[k]*Q[k,i])/(new_distribution[i]*Q[i,k]))

def get_M2(new_distribution,d2, l):
    """
    Metropolis - Hastings implementation to get M2
    """
    P = np.zeros((4,4))
    iter = True
    while iter:
        # Random Markov matrix generation
        Q = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = (12.5*np.exp(-l/4))/(np.sqrt(l/4))
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                Q[i,:] = R
                i = i + 1
        # Time reversible matrix generation
        for i in range(4):
            for j in range(4):
                if i == j:
                    sum = 0
                    for k in range(4):
                        if k != i:
                            sum += (Q[i,k] * (1 - alpha(new_distribution,Q,i,k)))
                    P[i,j] = Q[i,i] + sum
                else:
                    P[i,j] = Q[i,j]*alpha(new_distribution,Q,i,j)
        assert (np.abs(np.sum(new_distribution - np.matmul(
                new_distribution,P)))) < 10**-6
        # Adjust the matrix diagonalising (ensure matrix with determinant d2)
        vaps, _ = np.linalg.eig(P)
        vaps = sorted(vaps, reverse=True)
        A = symbols('A')
        eq = Eq(-d2+(((1-A)*vaps[1]+A)*((1-A)*vaps[2]+A)*((1-A)*vaps[3]+A)),0)
        sol = solve(eq, A)
        # We only want the real solution between 0 and 1
        res = 0
        for s in sol:
            if s.is_real and s > 0 and s < 1:
                res = s
                res = np.float64(res)
                P = (1-res)*P + res*np.identity(4)
                iter = False
                break
            elif s.is_complex:
                b = np.imag(s)
                a = sp.re(s)
                if np.abs(b) < 10**-20 and a > 0 and a < 1:
                    res = sp.re(s)
                    res = np.float64(res)
                    P = (1-res)*P + res*np.identity(4)
                    iter = False
                    break
    return P

def generate_random_matrix(distribution, l):
    """
    Returns the transition matrix M=M1M2 given a branch length
    and the distribution at the ancestor node.
    """
    res = 1
    # Compute M1
    while res >= 1:
        M1 = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = (12.5*np.exp(-l/4))/(np.sqrt(l/4))
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                M1[i,:] = R
                i = i + 1

        new_distribution = np.matmul(distribution,M1)
        D = np.diag(distribution)
        D_ = np.diag(new_distribution)
        res = np.exp(-l)*np.sqrt(np.linalg.det(D_))/np.sqrt(np.linalg.det(D))
        detM1 = np.linalg.det(M1)
        #Checking conditions
        if detM1 > np.exp(-l)*np.sqrt(np.linalg.det(D_))/np.sqrt(np.linalg.det(D)):
            pass
        else:
            res = 1

    d2 = np.exp(-l)*np.sqrt(np.linalg.det(D_))/(detM1*np.sqrt(np.linalg.det(D)))
    # Obtain M2
    M2 = get_M2(new_distribution,d2,l)

    detM2 = np.linalg.det(M2)
    assert(np.abs(detM2 - d2) < 10**-6)
    M = np.matmul(M1,M2)
    return M

def generate_sequences(M, seq):
    """
    Given the sequence seq of the ancestor node and the transition matrix M,
    returns the sequence of the descendant node
    """
    new_seq = ""
    for s in seq:
        if s == "A":
            new_seq += np.random.choice(['A', 'G', 'C', 'T'], p=M[0,:])
        elif s == "G":
            new_seq += np.random.choice(['A', 'G', 'C', 'T'], p=M[1,:])
        elif s == "C":
            new_seq += np.random.choice(['A', 'G', 'C', 'T'], p=M[2,:])
        else:
            new_seq += np.random.choice(['A', 'G', 'C', 'T'], p=M[3,:])
    return new_seq
