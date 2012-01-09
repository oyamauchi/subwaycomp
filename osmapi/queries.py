
# This will help you figure out operator names. Find a station on the subway
# system that you can pretty accurately guess the node name of, then this will
# search for relations that go there.
def relations_by_node(node_name):
    return """
<query type="node">
  <has-kv k="name" v="%s" />
</query>
<recurse type="node-way" into="ways" />
<union>
  <recurse type="node-relation" />
  <recurse type="way-relation" from="ways" />
</union>
<print />
""" % node_name


# This will collect all (ideally) subway lines run by a given operator. This
# just gets relations. Use the next query to find all the data for a given
# relation (subway line) individually.
def relations_by_operator(operator_name, route_type="subway"):
    return """
<query type="relation">
  <has-kv k="type" v="route" />
  <has-kv k="route" v="%s" />
  <has-kv k="network" v="%s" />
</query>
<print />""" % (route_type, operator_name)


# This will get all the data for a given relation (by relation id).
def nodes_and_ways_by_relation(relation):
    return """
<union>
  <id-query type="relation" ref="%s" />
  <recurse type="relation-node" into="nodes" />
  <recurse type="relation-way" />
  <recurse type="way-node" />
</union>
<print />""" % str(relation)
