#!/usr/bin/env python

import sys

post_tup = [(1, -1, 120),
            (2, 1, 60),
            (3, 1, 30),
            (4, 2, 90),
            (5, 3, 40),
            (6, 4, 10),
            (7, -1, 240),
            (8, 7, 190),
            (9, 7, 50)]

# Not sure if postID is an auto incrementing id so
# building a 2 pass tree to be safe. Incase the ids are
# replaced with uuids in the future
def count_followers(pt):
    tree = {} #build back ref tree
    for (post_id, repost_id, followers) in pt:
        tree[post_id] = repost_id
    org_counters = {}
    #now iterate through the back reference for an O(n log n) search on all 
    for(post_id, repost_id, followers) in pt:
        if repost_id == -1:
            org_counters[post_id] = followers
            continue
        while tree[repost_id] != -1:
            repost_id = tree[repost_id] # Keep going till you find the root
        org_counters[repost_id] += followers
    return org_counters

counts = count_followers(post_tup)

for org_post_id in sorted(counts.keys()):
    print("{0}: {1}".format(org_post_id, counts[org_post_id]))
