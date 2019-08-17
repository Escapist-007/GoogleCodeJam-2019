# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 World Finals - Problem B. Sort Permutation Unit
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051708/000000000016c77d
#
# Time:  O(K*N^2)
# Space: O(N)
#

def normalize(nums):
    A = [(num, i) for i, num in enumerate(nums)]
    A.sort()
    lookup = {i:rank for rank, (num, i) in enumerate(A)}
    return map(lambda x: lookup[x], range(len(nums)))

def rotate(nums, k, n):
    def reverse(nums, start, end):
        while start < end:
            nums[start], nums[end-1] = nums[end-1], nums[start]
            start += 1
            end -= 1

    k %= n
    reverse(nums, 0, n)
    reverse(nums, 0, k)
    reverse(nums, k, n)

def rotate_and_add_seq(nums, k, seq, shift):
    assert(k >= 0)  # it should be non-negative rotation count to avoid wrong small rotations
    shift[0] = (shift[0]+k)%(len(nums)-1)
    rotate(nums, k, len(nums)-1)
    for i in reversed(xrange(len(ROTATES))):
        q, k = divmod(k, ROTATES[i])
        seq.extend([i+2]*q)

def swap_and_add_seq(nums, seq):
    nums[-1], nums[-2] = nums[-2], nums[-1]
    seq.append(1)

def sorting_permutation_unit():
    P, S, K, N = map(int, raw_input().strip().split())
    As = []
    for _ in xrange(K):
        As.append(normalize(map(int, raw_input().strip().split())))

    perms = []
    perms.append(range(1, N+1))
    perms[-1][-1], perms[-1][-2] = perms[-1][-2], perms[-1][-1]
    for r in ROTATES:
        if r > N:
            break
        perms.append(range(1, N+1))
        rotate(perms[-1], r, len(perms[-1])-1)

    result = [""]
    result.append(str(len(perms)))
    for perm in perms:
        result.append(" ".join(map(str, perm)))

    for A in As:
        B = list(A)
        seq = [0]
        shift = [0]
        if A[-1] != len(A)-1:  # make the last one the largest one
            rotate_and_add_seq(A, (len(A)-2) - A.index(len(A)-1), seq, shift)
            swap_and_add_seq(A, seq) 
        while True:
            for curr in reversed(xrange(len(A)-1)):  # find any incorrect relative position
                if curr != (shift[0]+A[curr])%(len(A)-1):
                    break
            else:
                break
            rotate_and_add_seq(A, (len(A)-2) - curr, seq, shift)  # rotate and swap incorrect one to the last one
            swap_and_add_seq(A, seq)
            while A[-1] != len(A)-1:  # rotate and swap the last one into the correct position until it becomes the largest one
                rotate_and_add_seq(A, (len(A)-2) - (shift[0]+A[-1])%(len(A)-1), seq, shift)
                swap_and_add_seq(A, seq)
        rotate_and_add_seq(A, (len(A)-2) - A.index(len(A)-2), seq, shift)  # do the final rotations to put them in the correct absolute positions
        seq[0] = len(seq)-1
        result.append(" ".join(map(str, seq)))
    return "\n".join(result)

ROTATES = [1, 3, 9, 27]
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, sorting_permutation_unit())
