
import math

# The structs argument is a list. Each element is a dictionary, with a key
# 'pieces', whose value is a list of lists of tuples. Each 'piece' is a list of
# points, and each point is a tuple (a pair) of floats, representing lat and lon.
#
# This function converts this data structure, in-place, to express these points
# in terms of meters from the northernmost and westernmost extents of the whole
# set. It makes the simplifying assumption that the extents of the set are small
# enough that the surface of the earth can be approximated by a plane without
# anyone getting terribly upset. As such, it calculates constant lengths of
# degrees of latitude and longitude and uses them to map all of the points. This
# makes it an equirectangular projection.
def rectangularize(structs):
    # Find the extents of the set.
    lats = []
    lons = []
    for struct in structs:
        for piece in struct['pieces']:
            for lat, lon in piece:
                lats.append(lat)
                lons.append(lon)

    maxlat = max(lats)
    minlat = min(lats)
    minlon = min(lons)
    # maxlon not needed

    # Find the arclength of a degree of longitude; i.e. if you move east or west
    # on the earth's surface by one degree, how many meters have you moved? This
    # obviously varies depending on what latitude you're at; e.g. if you're at
    # one of the poles, the answer is zero. The approximation we use here is to
    # calculate it at the midway point between the min and max latitude we have
    # in the set.
    midwaylat = minlat + ((maxlat - minlat) / 2)

    # Length of the arc subtended by lon at lat, on a sphere of radius r, is:
    #   (lon) (r) (cos lat)
    # with all angles expressed in radians.
    radianonedegree = (math.pi / 180)
    earthradius = 6371000  # meters
    radianlat = (math.pi / 180) * midwaylat
    londeglength = radianonedegree * earthradius * math.cos(radianlat)

    # The length of one degree of latitude is duh.
    latdeglength = earthradius * radianonedegree

    # I am pleased at how well I remember 10th grade trigonometry

    xmax = 0
    ymax = 0

    for struct in structs:
        pieces = struct['pieces']
        for piece in pieces:
            for index, (lat, lon) in enumerate(piece):
                x = (lon - minlon) * londeglength
                y = (maxlat - lat) * latdeglength
                if x > xmax: xmax = x
                if y > ymax: ymax = y
                piece[index] = (int(round(x)), int(round(y)))

    return (xmax, ymax)
