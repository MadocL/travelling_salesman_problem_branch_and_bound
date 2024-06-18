# Travelling Salesman Problem

Travelling Salesman Problem (TSP) solution with branch and bound (BAB) algorithm using ortools

Code annotated as "GOOGLE'S CODE" is unchanged and is from https://developers.google.com/optimization/assignment/assignment_example


# Short example of 'merge_solutions_tuple_into_chains' function :

solution_tuples = [(0, 5), (1, 8), (2, 9), (3, 4), (4, 1), (5, 3), (6, 2), (7, 6), (8, 7), (9, 0)]

## Chains creation - step by step

```chains = []```
- (0, 5): New chain added<br>```chains = [[(0, 5)]]```
- (1, 8): New chain added<br>```chains = [[(0, 5)], [(1, 8)]]```
- (2, 9): New chain added<br>```chains = [[(0, 5)], [(1, 8)], [2, 9]]```
- (3, 4): New chain added<br>```chains = [[(0, 5)], [(1, 8)], [(2, 9)], [(3, 4)]]```
- (4, 1): Added in front of 2nd chain<br>```chains = [[(0, 5)], [(4, 1), (1, 8)], [(2, 9)], [(3, 4)]]```
- (5, 3): Added in back of 1st chain<br>```chains = [[(0, 5), (5, 3)], [(4, 1), (1, 8)], [(2, 9)], [(3, 4)]]```
- (6, 2): Added in front of 3rd chain<br>```chains = [[(0, 5), (5, 3)], [(4, 1), (1, 8)], [(6, 2), (2, 9)], [(3, 4)]]```
- (7, 6): Added in front of 3rd chain<br>```chains = [[(0, 5), (5, 3)], [(4, 1), (1, 8)], [(7, 6), (6, 2), (2, 9)], [(3, 4)]]```
- (8, 7): Added in back of 2nd chain<br>```chains = [[(0, 5), (5, 3)], [(4, 1), (1, 8), (8, 7)], [(7, 6), (6, 2), (2, 9)], [(3, 4)]]```
- (9, 0): Added in front of 1st chain<br>```chains = [[(9, 0), (0, 5), (5, 3)], [(4, 1), (1, 8), (8, 7)], [(7, 6), (6, 2), (2, 9)], [(3, 4)]]```

## Chains merge - step by step

```chains = [[(9, 0), (0, 5), (5, 3)], [(4, 1), (1, 8), (8, 7)], [(7, 6), (6, 2), (2, 9)], [(3, 4)]]```
- 1st and 3rd chains merged together<br>```chains = [[(4, 1), (1, 8), (8, 7)], [(7, 6), (6, 2), (2, 9), (9, 0), (0, 5), (5, 3)], [(3, 4)]]```
- 1st and 2nd chains merged together<br>```chains = [[(4, 1), (1, 8), (8, 7), (7, 6), (6, 2), (2, 9), (9, 0), (0, 5), (5, 3)], [(3, 4)]]```
- 1st and 2nd chains merged together<br>```chains = [[(3, 4), (4, 1), (1, 8), (8, 7), (7, 6), (6, 2), (2, 9), (9, 0), (0, 5), (5, 3)]]```