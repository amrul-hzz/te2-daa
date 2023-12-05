# implemented from: https://www.tandfonline.com/doi/pdf/10.1057/palgrave.jors.2601698?casa_token=odT6d_I_Y6QAAAAA:8haj3wpHuu9MslLTXssWMwJgwMJG0Umuy1M8havmbbUYfmT_3TM00yq0vMEmCn6IdIOyKFpoXTjIKih6

import numpy as np
import math

class BnBUnboundedKnapsack:

    def __init__(self, cap, weights, values):
        self.cap = cap
        self.weights = weights
        self.values = values
        self.n = len(values)
        self.N = []

    def solve(self):
        
        try:
            self.initialize()
            return self.develop() 
        except Exception as e:
            return self.finish()

    def eliminate_dominated(self):
        '''
        Eliminate items that have non-dominating value to weight ratio.
        '''

        self.N = [i for i in range (self.n)]

        for j in range (0, len(self.N)-1):
            for k in range (j+1, len(self.N)):
                if math.floor(self.weights[k]/self.weights[j]) * self.values[j] >= self.values[k] and k in self.N:
                    self.N.remove(k) 
                elif math.floor(self.weights[j]/self.weights[k]) * self.values[k] >= self.values[j] and j in self.N:
                    self.N.remove(j)
                    break       

    def upperbound(self, i, cap):
        idx = self.N[i] 
        w1 = self.weights[idx]
        v1 = self.values[idx]

        U = math.floor(cap/w1) * v1 
        
        cap_1 = cap - math.floor(cap/w1) * w1
       
        if i+1 < len(self.N):
            idx2 = self.N[i+1]
            w2 = self.weights[idx2]
            v2 = self.values[idx2]

            z_1 = math.floor(cap/w1) * v1 + math.floor(cap_1/w2) * v2
            cap_2 = cap_1 - math.floor(cap_1/w2) * w2

            U_1 = None
            U_2 = z_1 + math.floor(
                        (cap_2 + math.ceil((w2-cap_2)/w1)*w1) * (v2/w2) -
                        math.ceil((w2-cap_2)/w1)*v1
                    )
    
            if i+2 <  len(self.N):
                idx3 = self.N[i+2]
                w3 = self.weights[idx3]
                v3 = self.values[idx3]

                U_1 = z_1 + math.floor(cap_2*(v3/w3))

            if U_1 == None: 
                U = U_2
            elif U_2 == None:
                U = U_1
            else:
             U = max(U_1, U_2)

        return U

    def initialize (self): 
        self.eliminate_dominated()

        self.N = sorted(self.N, key=lambda x: self.values[x]/self.weights[x], reverse=True)

        self.x_hat = np.zeros(self.n) # current best solution
        self.x = np.zeros(self.n) # current feasible solution
        self.i = 0 
        self.z_hat = 0 # current best solution value

        self.M = np.zeros(shape=(len(self.N), self.cap)) 
        
        idx = self.N[self.i] 
        self.x[idx] = math.floor(self.cap/self.weights[idx])
        self.V = self.values[idx] * self.x[idx]
        self.cap_r = self.cap - self.weights[idx] * self.x[idx]
        self.U = self.upperbound(self.i, self.cap)

        self.m = []
        for i in range (len(self.N)):
            mi = float('inf')
            idx = i
            for j in range (i+1, len(self.N)):
                cur_w = self.weights[self.N[j]]
                mi = min(mi, cur_w)
            
            self.m.append(mi)

    def develop(self):
        if self.cap_r < self.m[self.i]:
            if self.z_hat < self.V:
                self.z_hat = self.V
                self.x_hat = self.x
                
                if self.z_hat == self.U:
                    return self.finish()

            self.backtrack()
            return
        
        else:
            
            for j in self.N[self.i+1:]:
                if self.weights[j] <= self.cap_r:
                    break
            else:
                if self.z_hat < self.V:
                    self.z_hat = self.V
                    self.x_hat = self.x
                    
                    if self.z_hat == self.U:
                        return self.finish()

                self.backtrack()
                return

            U = self.upperbound(j, self.cap_r) 
            
            if self.V + U <= self.z_hat:
                self.backtrack()
            
            if self.M[self.i, self.cap_r] >= self.V:
                self.backtrack()
            
            idx = self.N[j]
            self.x[idx] = math.floor(self.cap_r/self.weights[idx])
            self.V  += self.values[idx] * self.x[idx]
            self.cap_r -= self.weights[idx] * self.x[idx]
            self.M[self.i, self.cap_r] = self.V
            self.i = j
            self.develop()

    def backtrack(self):
        for j in reversed(self.N[:self.i+1]):
            if self.x[j] > 0:
                break
        else:
            return self.finish()
        
        if j < 0:
            return self.finish()

        self.i = j
        idx = self.N[self.i]
        self.x[idx] -= 1
        self.V -= self.values[idx]
        self.cap_r += self.weights[idx]

        if self.cap_r < self.m[self.i]:
            self.backtrack()
        
        if self.i + 1 < len(self.N):
            idx2 = self.N[self.i + 1]
            if self.V + math.floor(self.cap_r * (self.values[idx2]/self.weights[idx2])) <= self.z_hat:
                self.V -= self.values[idx] * self.x[idx]
                self.cap_r += self.weights[idx] * self.x[idx]
                self.x[idx] = 0
                self.backtrack()

        if self.cap_r - self.weights[idx] >= self.m[idx]:
            self.develop()

        self.replace(self.i, self.i + 1)

    def replace(self, j, h):
        if h >= len(self.N):
            return self.finish()

        idx_j = self.N[j]
        idx_h = self.N[h]

        if self.z_hat >= self.V + math.floor(self.cap_r * (self.values[idx_h]/self.weights[idx_h])):
            self.backtrack()
        
        if self.weights[idx_h] >= self.weights[idx_j]:
            if  (self.weights[idx_h] == self.weights[idx_j]) or \
                (self.weights[idx_h] > self.cap_r) or \
                (self.z_hat >= self.V + self.values[idx_h]):

                h += 1
                self.replace(j, h)

            self.z_hat = self.V + self.values[idx_h]
            self.x_hat = self.x
            self.x[idx_h] = 1

            if self.z_hat == self.U:
                return self.finish()

            j = h
            h += 1
            self.replace(j, h)

        else:
            idx_hmin1 = self.N[h-1]
            if self.cap_r - self.weights[idx_h] < self.m[idx_hmin1]:
                h += 1
                self.replace(j, h)

        self.i = h
        idx_i = self.N[self.i]
        self.x[idx_i] = math.floor(self.cap_r/self.weights[idx_i])
        self.V += self.values[idx_i] * self.weights[idx_i]
        self.cap_r -= self.weights[idx_i] * self.x[idx_i]
        self.develop()

    def finish(self):
        return int(self.z_hat), self.x_hat
