#!/usr/bin/env python
import unittest
import operator
import random
import sys

old_tup = [(1, -1, 120),
           (2, 1, 60),
           (3, 1, 30),
           (4, 2, 90),
           (5, 3, 40),
           (6, 4, 10),
           (7, -1, 240),
           (8, 7, 190),
           (9, 7, 50)]

big_tup = [(1, -1, 1), (2, 1, 2), (3, 1, 3), (4, -1, 4), (5, 2, 5), (6, 3, 6),
           (7, 4, 7), (8, 4, 8), (9, 8, 9), (10, 8, 10), (11, 7, 11),
           (12, 7, 12), (13, 12, 13), (14, 12, 14), (15, 11, 15), (16, 15, 16),
           (17, 15, 17), (18, 3, 18),(19, 18, 19), (20, 18, 20), (21, 5, 21),
           (22,21,22), (23, 21, 23)]

# Not sure if postID is an auto incrementing id so
# building a 2 pass tree to be safe. Incase the ids are
# replaced with uuids in the future
def count_followers(pt):
    op_counter = 0
    all = set([])
    srcs = set([])
    dsts = set([])
    roots = set([])
    leafs = set([])
    root_followers = {}
    pid2followers = {}
    pid2rid = {}
    for(pid, rid, f) in pt:
        all.add(pid)
        op_counter += 1
        if rid == -1: # We got a root
            roots.add(pid)
        else: #other wise its elseware in the tree
            pid2rid[pid] = rid
            dsts.add(rid)
            srcs.add(pid)
        pid2followers[pid] = f
        srcs.add(pid)

    op_counter += len(all)*2
    leafs = all - dsts
    root_followers = {}
    #now start from the bottom the tree and tricle the followers towards their
    #root nodes pruning the tree on the way up in an attempt to get n log n time
    for pid in leafs:
        op_counter += 1
        trail = set([]) # After we reach the top where going to flatten the all
                        # nodes below to save time by avoiding revisiting a
                        # parent node that has multiple children
        cpid = pid
        while cpid not in roots:
            op_counter += 1
            # Get this nodes followers
            followers = pid2followers[cpid]

            #find the parent
            rid = pid2rid[cpid]

            #now move all the followers up the tree
            pid2followers[cpid] = 0
            crid = pid2rid[cpid]
            pid2followers[crid] += followers
            trail.add(cpid) # so we can flatten the tree later

            # no travers to the parent
            cpid = crid

        #The loop exiterd so this must be a root
        root = cpid
        root_followers[root] = pid2followers[root]

        for cpid in trail: #flatten the tree
            op_counter += 1
            # repoint all nodes in the trail to root
            # Sense we no each point in the trail ends going to root we
            # repoint all the nodes to the root saving time for future trees
            pid2rid[cpid] = root
        # now move on to the next leaf and hope we shaved the path
    return (root_followers, op_counter)

class TestCounter(unittest.TestCase):
    def test_counter(self):
        n = 4096
        (counts, op_counter) = count_followers(old_tup)
        print counts
        self.assertEqual(counts[1], 350)
        self.assertEqual(counts[7], 480)
        loop_count = 0
        pt = big_tup[:]
        random.shuffle(pt)
        op_counter_sum = 0
        for i in xrange(0, n):
            random.shuffle(pt)
            (counts, op_counter) = count_followers(pt)
            op_counter_sum += op_counter
            self.assertEqual(counts[1], 140)
            self.assertEqual(counts[4], 136)
        avg_call_count = op_counter_sum/float(n)
        print avg_call_count

if __name__ == "__main__":
    unittest.main()