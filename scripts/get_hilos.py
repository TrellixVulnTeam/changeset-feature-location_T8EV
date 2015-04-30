
from __future__ import print_function

import csv
from src import main, utils
import sys


projects = main.load_projects()

with open('snapshot_hilos.csv', 'wt') as f:
    pass

with open('changeset_hilos.csv', 'wt') as f:
    pass

for project in projects:
    goldsets = main.load_goldsets(project)
    snapshot_ranks = main.read_ranks(project, "release")
    changeset_ranks = main.read_ranks(project, "changeset")


    snapshot_frms =dict( (y,(x,z)) for x,y,z in main.get_frms(goldsets, snapshot_ranks))
    changeset_frms =dict( (y,(x,z)) for x,y,z in  main.get_frms(goldsets, changeset_ranks))


    snapshot_low = min(rank[0] for gid,rank in snapshot_frms.items())
    changeset_low = min(rank[0] for gid,rank in changeset_frms.items())

    snapshot_high = max(rank[0] for gid,rank in snapshot_frms.items())
    changeset_high = max(rank[0] for gid,rank in changeset_frms.items())

    print("Lo:", project.printable_name, project.version, snapshot_low, changeset_low, sep="\t")
    print("Hi:", project.printable_name, project.version, snapshot_high, changeset_high, sep="\t")

    snapshot_best = dict(filter(lambda x: x[1][0] == snapshot_low, snapshot_frms.items()))
    changeset_best = dict(filter(lambda x: x[1][0] == changeset_low, changeset_frms.items()))

#    snapshot_worst = dict(filter(lambda x: x[1][0] == snapshot_high, snapshot_frms.items()))
#    changeset_worst = dict(filter(lambda x: x[1][0] == changeset_high, changeset_frms.items()))


    worst = (-1, )
    for gid, val in snapshot_best.items():
        rank, item = val
        if gid in changeset_frms:
            cs_rank, cs_item = changeset_frms[gid]
            if cs_rank > worst[0] and cs_rank != rank:
                worst = (gid, rank, item, cs_rank, cs_item)

    if worst != (-1,):
        with open('snapshot_hilos.csv', 'at') as f:
            w = csv.writer(f)
            w.writerow((project.name, project.version, project.level) + worst)

    worst = (-1, )
    for gid, rank in changeset_best.items():
        rank, item = val
        if gid in snapshot_frms:
            ss_rank, ss_item = snapshot_frms[gid]
            if ss_rank > worst[0] and ss_rank != rank:
                worst = (gid, rank, item, ss_rank, ss_item)

    if worst != (-1,):
        with open('changeset_hilos.csv', 'at') as f:
            w = csv.writer(f)
            w.writerow((project.name, project.version, project.level) + worst)

