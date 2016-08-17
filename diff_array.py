#!/usr/bin/env python

import sys

cur = [1,3,5,6,8,9]
tar = [1,2,5,7,9]

# The inputs appear to be ordered as does the output with nothing
# to suggest when additions or deletions should be applied so
# I went ahead and used set logic. With input and output converted two and
# from arrays
def diff_array(cur,tar):
    return {'additions': sorted(set(tar) - set(cur)),
            'deletions': sorted(set(cur) - set(tar))}

diff = diff_array(cur,tar)

fmt = "additions: {additions}\ndeletions: {deletions}\n"
print(fmt.format(**diff))

