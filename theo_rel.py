from math import comb
from itertools import product
import numpy as np
import math

prob_r_dp = {}
successdp = {}

def generate_arrays(L):
    if not L:
        return [[]]
    
    results = []
    smaller_arrays = generate_arrays(L[1:])
    for i in range(L[0] + 1):
        for smaller_array in smaller_arrays:
            results.append([i] + smaller_array)
    return results


def f(num_strikes_till_now, param = 0.005, a = 999): # a = 999 -> t = 0 par 0.001 failure prob, param = 0.005
    return 1/(1+a*math.exp(-param*num_strikes_till_now))

def alt_f(num_strikes_till_now, a1 = 1.4, a2 = 1400): # a = 999 -> t = 0 par 0.001 failure prob, param = 0.005
    return (num_strikes_till_now + a1)/(num_strikes_till_now + a2)
    
def prob_l(l, l_prime, t, t0):
    n_s = len(l)
    
    product_term = 1
    for i in range(n_s):
        product_term *= comb(l[i], l_prime[i])
    
    sum_term1 = sum(l_prime)
    sum_term2 = sum([(l[i] - l_prime[i]) for i in range(n_s)])
    
    probability = product_term * (1 - f(t0-t+1)) ** sum_term1 * f(t0-t+1) ** sum_term2
    # probability = product_term * (0.99 ** sum_term1) * (0.01 ** sum_term2)
    
    return probability   



def prob_r(R, R_prime, L, m_f):
    n_d = len(R)
    
    key_tuple = (m_f, tuple(R), tuple(R_prime), tuple(sorted(L)))    
    if key_tuple in prob_r_dp:
        return prob_r_dp[key_tuple]     
    
    possible_assignments = product(range(1, n_d + 1), repeat=len(L))
    
    total_probability = 0

    all_K = []
    for assignment in possible_assignments:
        breakup = False
        for val in assignment:
            if R[val-1] == 0:
                breakup =True
                break
        if breakup:
            continue
        K = [0 for _ in range(1,n_d+1)]
        # print(K)
        for i in range(len(assignment)):
            K[assignment[i]-1] += L[i]
        # print(K)
        all_K.append(K)


    for K in all_K:
        product_term = 1
        for i in range(n_d):
            r_i = R[i]
            r_i_prime = R_prime[i]
            k_i = K[i]
            
            if k_i < r_i - r_i_prime:
                product_term = 0
                break
            
            sum_term =0
            if r_i_prime == 0:
                for x in range(0, k_i -r_i + 1 ):        
                    binomial_coefficient = comb(k_i, r_i + x)
                    probability_term = (1 - m_f) ** (r_i + x) * m_f ** (k_i- r_i - x)
                    sum_term += binomial_coefficient*probability_term
            else:
                binomial_coefficient = comb(k_i, r_i - r_i_prime)
                probability_term = (1 - m_f) ** (r_i - r_i_prime) * m_f ** (k_i - r_i + r_i_prime)
                sum_term = binomial_coefficient*probability_term
            
            product_term *= sum_term

        total_probability += product_term

    prob_r_dp[key_tuple] = total_probability/len(all_K)
    return prob_r_dp[key_tuple]


def prob(L, R, L_new, R_new, m_f, t, t0):
    return prob_r(R, R_new, L, m_f)*prob_l(L, L_new, t, t0)



def successProbability(t0, t, L, R, m_f): # t is the time step, L and R are the initial arrays
    # Base case: when t is 0
    if t == 0:
        for i in range(len(R)):
            if R[i] > 0:
                return 0
        return 1
    if sum(R) == 0:
        return 1
    if sum(L) == 0:
        return 0
    
    key_tuple = (t,tuple(sorted(L)),tuple(sorted(R)))
    if key_tuple in successdp:
        return successdp[key_tuple]
    
      
    # Iterate over all possible combinations of indices L and R
    L_ = generate_arrays(L)
    R_ = generate_arrays(R)
    res = 0
    for i in range(len(L_)):
        for j in range(len(R_)):
            res += successProbability(t0, t-1, L_[i], R_[j], m_f) * prob(L,R,L_[i],R_[j], m_f, t, t0)
    
    successdp[key_tuple] = res
    return res
