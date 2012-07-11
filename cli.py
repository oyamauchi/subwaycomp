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
elif sys.argv[1] == "rbr":
    query = osmapi.queries.nodes_and_ways_by_relation(sys.argv[2])
elif sys.argv[1] == "nwbr":
    relations = []
    r = random.Random()
    for relid in sys.argv[2:]:
        if relid[0] == 'L':
            # Read it from local data
            result = open('localdata/' + relid[1:]).read()
        else:
            # Read it from the OSM API
            query = osmapi.queries.nodes_and_ways_by_relation(relid)
            result = osmapi.client.send_query(query)
        assert result
        relation = osmapi.graph.get_one_relation(result)

        if not relation.color:
            # If your system is lame and doesn't supply its own colors, you get
            # magical rainbow colors. Seed with relation id to ensure consistent
            # colors when regenerating data.
            r.seed(relid)
            relation.color = "#%x" % r.randint(0x333333, 0xcccccc)
        relations.append(relation)

    structs = [rel.jsonable_form() for rel in relations]
    xmin, ymin, xmax, ymax = geo.mercatorize(structs)
    jsondump = json.dumps(structs, separators=(',',':'))
    print """{
"obj" : %s,
"xmin" : %d, "ymin" : %d,
"xmax" : %d, "ymax" : %d
}
""" % (jsondump, xmin, ymin, xmax, ymax)
    exit(0)

else:
    print "boop"
    exit(1)

result = osmapi.client.send_query(query)
print result

