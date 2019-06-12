# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 Round C - Problem D. Napkin Folding
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051707/0000000000159170
#
# Time:  O(N^2 * K^4), pass in PyPy2 but Python2 for set 2
# Space: O(N * K^2)
#

def gcd(a, b):  # Time: O((logn)^2)
    while b:
        a, b = b, a % b
    return a

def advance_polygon_area(p1, p2):
    return p1[0]*p2[1]-p1[1]*p2[0]

def polygon_area(polygon):
    area = 0
    for i in xrange(len(polygon)):
        area += advance_polygon_area(polygon[i-1], polygon[i])
    return abs(area)  # in this problem, we don't divide the area by 2 to keep it an integer

# Return Q which is the reflection of P over line (A, B)
def reflect(P, A, B):
    a, b, c = A[1]-B[1], -(A[0]-B[0]), (A[1]-B[1])*(-A[0])-(A[0]-B[0])*(-A[1])
    if -2 * a * (a * P[0] + b * P[1] + c) % (a * a + b * b) or \
       -2 * b * (a * P[0] + b * P[1] + c) % (a * a + b * b):
       return None  # in this problem, Q should be integers too
    return (-2 * a * (a * P[0] + b * P[1] + c) // (a * a + b * b) + P[0],
            -2 * b * (a * P[0] + b * P[1] + c) // (a * a + b * b) + P[1])

def find_candidates(K):
    fractions_set = set()
    for y in xrange(2, K+1):
        for x in xrange(1, y):
            common = gcd(x, y)
            fractions_set.add((x//common, y//common))
    candidates = list(fractions_set)
    candidates.sort()
    return candidates

def split(A, B, candidates):
    endpoints = []
    for c in candidates:
        endpoints.append((A[0]+(B[0]-A[0])*c[0]//c[1],
                          A[1]+(B[1]-A[1])*c[0]//c[1]))
    return endpoints

def find_possible_endpoints(polygon, candidates):
    endpoints = []
    endpoints.append(polygon[0])
    for i in xrange(1, len(polygon)):
        endpoints.extend(split(polygon[i-1], polygon[i], candidates))
        endpoints.append(polygon[i])
    endpoints.extend(split(polygon[-1], polygon[0], candidates))
    return endpoints

def find_possible_pairs(polygon, K, endpoints):
    total_area = polygon_area(polygon)
    for i in xrange(len(endpoints)-1):
        area = 0
        for j in xrange(i+1, len(endpoints)):
            area += advance_polygon_area(endpoints[(j-1)%len(endpoints)], endpoints[j]) + \
                    advance_polygon_area(endpoints[j], endpoints[i]) - \
                    advance_polygon_area(endpoints[(j-1)%len(endpoints)], endpoints[i])
            if abs(area) * K == total_area:
                yield (i, j)
            elif abs(area) * K == total_area * (K-1):
                yield (j, i)

def find_pattern(begin, end, length, C):
    pattern = [begin]
    if end < begin:
        end += length
    curr = begin//C*C + C
    while end-curr > 0:
        pattern.append(curr%length)
        curr += C
    pattern.append(end%length)
    return pattern

def normalize(a, b):
    return (a, b) if a <= b else (b, a)

def is_on_polygon_edge(a, b, length, C):
    if a%C == b%C == 0:
        return abs(a-b) in (C, length-C)
    if a%C == 0:
        return a in (b//C*C, (b//C+1)*C%length)
    if b%C == 0:
        return b in (a//C*C, (a//C+1)*C%length)
    return a//C == b//C

def find_valid_pairs(polygon, K, endpoints, endpoints_idx, pair):
    C = len(endpoints)//len(polygon)  # count of polygon and non-polygon vertex on an edge

    pattern = find_pattern(pair[0], pair[1], len(endpoints), C)
    pairs = set()
    stk = [(pair, pattern)]  # using queue is also fine (BFS), here we use stack (DFS)
    while len(pairs) != K-1 and stk:
        (pair, pattern) = stk.pop()
        pairs.add(normalize(pair[0], pair[1]))

        new_pairs, new_pattern = [], []
        for i in xrange(-1, len(pattern)):
            p = reflect(endpoints[pattern[i]], endpoints[pair[0]], endpoints[pair[1]])
            if not p or p not in endpoints_idx:  # not on polygon
                return None
            p_idx = endpoints_idx[p]  
            if new_pattern:
                if not is_on_polygon_edge(new_pattern[-1], p_idx, len(endpoints), C):  # not on polygon edge
                    new_pair = normalize(new_pattern[-1], p_idx)
                    if new_pair not in pairs:
                        new_pairs.append(new_pair)
            if len(new_pattern) != len(pattern):
                new_pattern.append(p_idx)

        for new_pair in new_pairs:
            stk.append((new_pair, new_pattern))

    return pairs if len(pairs) == K-1 and not stk else None

def output1(p, lcm):
    common = gcd(p, lcm)
    return "{}/{}".format(p//common, lcm//common)

def output2(p, lcm):
    return "{} {}".format(output1(p[0], lcm), output1(p[1], lcm))

def napkin_folding():
    N, K = map(int, raw_input().strip().split())
    lcm = 1
    for i in xrange(2, K+1):
        lcm = lcm * i // gcd(lcm, i)
    polygon = []
    for _ in xrange(N):
        polygon.append(tuple(map(lambda x: int(x)*lcm, raw_input().strip().split())))
    candidates = find_candidates(K)  # Time: O(K^2)
    endpoints = find_possible_endpoints(polygon, candidates)  # Time: O(N*K^2)

    endpoints_idx = {}
    for k, v in enumerate(endpoints):
        endpoints_idx[v] = k
    for pair in find_possible_pairs(polygon, K, endpoints):  # Time: O(N^2*K^4)
        # possible pairs should be much less than O(N^2*K^4)
        pairs = find_valid_pairs(polygon, K, endpoints, endpoints_idx, pair)  # Time: O(N*K)
        if not pairs:
            continue
        result = ["POSSIBLE"]
        for a, b in pairs:
            result.append("{} {}".format(output2(endpoints[a], lcm), output2(endpoints[b], lcm)))
        return "\n".join(result)
    return "IMPOSSIBLE"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, napkin_folding())
