#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osmapi.client
import osmapi.graph
import osmapi.queries

import geo
import json
import random

import sys

if sys.argv[1] == "rbo":
    query = osmapi.queries.relations_by_operator(sys.argv[2])
elif sys.argv[1] == "rbn":
    query = osmapi.queries.relations_by_node(sys.argv[2])
elif sys.argv[1] == "nwbr":
    relations = []
    r = random.Random()
    for relid in sys.argv[2:]:
        query = osmapi.queries.nodes_and_ways_by_relation(relid)
        result = osmapi.client.send_query(query)
        relation = osmapi.graph.get_one_relation(result)
        if not relation.color:
            # If your system is lame and doesn't supply its own colors, you get
            # magical rainbow colors
            relation.color = "#%x" % r.randint(0x333333, 0xcccccc)
        relations.append(relation)

    structs = [rel.jsonable_form() for rel in relations]
    xmax, ymax = geo.rectangularize(structs)
    print "hereItIs(%s, %s, %s)" % (json.dumps(structs, separators=(',',':')),
                                    str(xmax), str(ymax))
    exit(0)

else:
    print "boop"
    exit(1)

result = osmapi.client.send_query(query)
print result

