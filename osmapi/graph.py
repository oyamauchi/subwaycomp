
import xml.dom.minidom

class Node:
    def __init__(self, xmlnode):
        self.id = int(xmlnode.getAttribute('id'))
        self.lat = float(xmlnode.getAttribute('lat'))
        self.lon = float(xmlnode.getAttribute('lon'))


class Way:
    def __init__(self, xmlnode, nodecache):
        self.id = int(xmlnode.getAttribute('id'))
        self.nodes = \
            [nodecache[int(nd.getAttribute('ref'))]
             for nd in xmlnode.getElementsByTagName('nd')]


class Relation:
    def __init__(self, xmlnode, waycache):
        self.id = int(xmlnode.getAttribute('id'))
        self.ways = \
            [waycache[int(member.getAttribute('ref'))]
             for member in xmlnode.getElementsByTagName('member')
             if member.getAttribute('type') == 'way']

        # Grab the color if it's there
        tagnodes = xmlnode.getElementsByTagName('tag')
        color = None
        for tagnode in tagnodes:
            if tagnode.getAttribute('k') == 'color' or \
                    tagnode.getAttribute('k') == 'colour':
                color = tagnode.getAttribute('v')
                break

        self.color = color


    def jsonable_form(self):
        obj = {'color' : self.color}

        pieces = []
        for way in self.ways:
            piece = []
            for node in way.nodes:
                piece.append((node.lat, node.lon))
            pieces.append(piece)

        obj['pieces'] = pieces
        return obj


def get_one_relation(queryresult):
    queryresult = xml.dom.minidom.parseString(queryresult)

    nodecache = {}
    waycache = {}

    # yo dawg
    nodenodes = queryresult.getElementsByTagName('node')
    for nodenode in nodenodes:
        node = Node(nodenode)
        nodecache[node.id] = node

    waynodes = queryresult.getElementsByTagName('way')
    for waynode in waynodes:
        way = Way(waynode, nodecache)
        waycache[way.id] = way

    relationnodes = queryresult.getElementsByTagName('relation')
    assert len(relationnodes) == 1
    relation = Relation(relationnodes[0], waycache)

    return relation
