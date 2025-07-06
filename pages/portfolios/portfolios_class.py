import numpy as np
from cvxopt import matrix
from cvxopt.solvers import qp as Solver, options as SolverOptions
from scipy.optimize import minimize_scalar

SolverOptions["show_progress"] = False

class portfolio:

    def __init__(self, means, cov, Shorts):
        self.means = np.array(means)
        self.cov = np.array(cov)
        self.Shorts = Shorts
        self.n = len(means)
        if Shorts:
            w = np.linalg.solve(cov, np.ones(self.n))
            self.GMV = w / np.sum(w)
            w = np.linalg.solve(cov, means)
            self.piMu = w / np.sum(w)
        else:
            n = self.n
            Q = matrix(cov, tc="d")
            p = matrix(np.zeros(n), (n, 1), tc="d")
            G = matrix(-np.identity(n), tc="d")
            h = matrix(np.zeros(n), (n, 1), tc="d")
            A = matrix(np.ones(n), (1, n), tc="d")
            b = matrix([1], (1, 1), tc="d")
            sol = Solver(Q, p, G, h, A, b)
            self.GMV = np.array(sol["x"]).flatten() if sol["status"] == "optimal" else np.array(n * [np.nan])

    def frontier(self, m):
        if self.Shorts:
            gmv = self.GMV
            piMu = self.piMu
            m1 = gmv @ self.means
            m2 = piMu @ self.means
            a = (m - m2) / (m1 - m2)
            return a * gmv + (1 - a) * piMu
        else:
            n = self.n
            Q = matrix(self.cov, tc="d")
            p = matrix(np.zeros(n), (n, 1), tc="d")
            G = matrix(-np.identity(n), tc="d")
            h = matrix(np.zeros(n), (n, 1), tc="d")
            A = matrix(np.vstack((np.ones(n), self.means)), (2, n), tc="d")
            b = matrix([1, m], (2, 1), tc="d")
            sol = Solver(Q, p, G, h, A, b)
            return np.array(sol["x"]).flatten() if sol["status"] == "optimal" else np.array(n * [np.nan])

    def tangency(self, r):
        if self.Shorts:
            w = np.linalg.solve(self.cov, self.means - r)
            return w / np.sum(w)
        else:
            def f(m):
                w = self.frontier(m)
                mn = w @ self.means
                sd = np.sqrt(w.T @ self.cov @ w)
                return - (mn - r) / sd
            m = minimize_scalar(f, bounds=[max(r, np.min(self.means)), max(r, np.max(self.means))], method="bounded").x
            return self.frontier(m)

    def optimal(self, raver, rs=None, rb=None):
        n = self.n
        if self.Shorts:
            if (rs or rs==0) and (rb or rb==0):
                Q = np.zeros((n + 2, n + 2))
                Q[2:, 2:] = raver * self.cov
                Q = matrix(Q, tc="d")
                p = np.array([-rs, rb] + list(-self.means))
                p = matrix(p, (n + 2, 1), tc="d")
                G = np.zeros((2, n + 2))
                G[0, 0] = G[1, 1] = -1
                G = matrix(G, (2, n+2), tc="d")
                h = matrix([0, 0], (2, 1), tc="d")
                A = matrix([1, -1] + n*[1], (1, n+2), tc="d")
                b = matrix([1], (1, 1), tc="d")
                sol = Solver(Q, p, G, h, A, b)
                return np.array(sol["x"]).flatten()[2:] if sol["status"] == "optimal" else None
            else:
                w = np.linalg.solve(self.cov, self.means)
                a = np.sum(w)
                return (a/raver)*self.piMu + (1-a/raver)*self.GMV
        else:
           if (rs or rs==0) and (rb or rb==0):
                Q = np.zeros((n + 2, n + 2))
                Q[2:, 2:] = raver * self.cov
                Q = matrix(Q, tc="d")
                p = np.array([-rs, rb] + list(-self.means))
                p = matrix(p, (n+2, 1), tc="d")
                G = matrix(-np.identity(n + 2), tc="d")
                h = matrix(np.zeros(n+2), (n+2, 1), tc="d")
                A = matrix([1, -1] + n * [1], (1, n+2), tc="d")
                b = matrix([1], (1, 1), tc="d")
                sol = Solver(Q, p, G, h, A, b)
                return np.array(sol["x"]).flatten()[2:] if sol["status"] == "optimal" else None
           else:
                Q = matrix(raver * self.cov, tc="d")
                p = matrix(-self.means, (n, 1), tc="d")
                G = matrix(-np.identity(n), tc="d")
                h = matrix(np.zeros(n), (n, 1), tc="d")
                A = matrix(np.ones(n), (1, n), tc="d")
                b = matrix([1], (1, 1), tc="d")
                sol = Solver(Q, p, G, h, A, b)
                return np.array(sol["x"]).flatten() if sol["status"] == "optimal" else None
