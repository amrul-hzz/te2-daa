# taken from: https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/ 
# Time Complexity: O(N*W)
# Auxiliary Space: O(W) 

def dp_unbounded_knapsack(W, n, val, wt): 
	'''
	Find maximum achievable value with a knapsack of weight W and multiple instances allowed. 
	Returns the maximum value with knapsack of W capacity 
	'''

	# dp[i] is going to store maximum 
	# value with knapsack capacity i. 
	dp = [0 for i in range(W + 1)] 

	ans = 0

	# Fill dp[] using above recursive formula 
	for i in range(W + 1): 
		for j in range(n): 
			if (wt[j] <= i): 
				dp[i] = max(dp[i], dp[i - wt[j]] + val[j]) 

	return dp[W] 