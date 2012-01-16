
import math

# This is the latitude at which Google Maps cuts off the map. (Theoretically, a
# Mercator map's height is infinite, so you have to cut it off somewhere.)
#
# This limit was derived by solving for a square Mercator map. Consider the
# Mercator map of a unit sphere, of width 2pi (meaning that the width of the map
# is equal to the circumference of the sphere). For the northernmost point on
# the map to be pi units away from the equator, it must be at latitude phi
# satisfying:
#
# ln(tan(phi) + sec(phi)) = pi
#    or equivalently:
# phi = 2(arctan(e^pi) - (pi / 4))
#     =~ 1.4844222297453324
#     =~ 85.0511287798 degrees
#
# Lending authority to this idea is the fact that Google Maps cut off at exactly
# this latitude.
MERCATOR_LAT_LIMIT = 1.4844222297453324;

# The maximum of the resulting map coordinates. It's big enough that the units
# resolve to ~2.39m at the equator, which seems good enough.
MERCATOR_MAP_DIMENSION = 2 ** 24


# Converts a latitude into a Mercator y-coordinate. phi in radians.
def _mercator_lat(phi):
    return math.log(math.tan((math.pi / 4) + (phi / 2)))

# The structs argument is a list. Each element is a dictionary, with a key
# 'pieces', whose value is a list of lists of tuples. Each 'piece' is a list of
# points, and each point is a tuple (a pair) of floats, representing lat and
# lon, in degrees.
#
# This function converts this data structure, in-place, to express these points
# in terms of x and y from the top-left corner of a Mercator-projection world
# map, on a scale of [0, MAP_DIMENSION). The map is centered on the equator and
# prime meridian, and vertically cut off at MERCATOR_LAT_LIMIT. It assumes the
# earth is spherical.
#
# It returns a tuple with min and max x and y on these axes.
def mercatorize(structs):
    # We'll figure these out and pass them along to the client, for convenience.
    xmin = MERCATOR_MAP_DIMENSION
    ymin = MERCATOR_MAP_DIMENSION
    xmax = 0
    ymax = 0

    ylimit = _mercator_lat(MERCATOR_LAT_LIMIT)

    for struct in structs:
        for piece in struct['pieces']:
            for idx, (lat, lon) in enumerate(piece):
                # Mercator projection of longitude is trivial. It's in the range
                # (-180, 180) coming in.
                x = ((lon - (-180)) * MERCATOR_MAP_DIMENSION) / 360
                x = int(round(x))

                # Mercator projection of latitude. It's trickier. First, convert
                # to radians, and flip it upside down; latitude increases going
                # upward but the target coordinate system increases going down.
                radlat = (-lat) * (math.pi / 180)

                y = _mercator_lat(radlat)
                # y is now, mathematically, in (-inf, inf), but we're cutting it
                # off at MERCATOR_LAT_LIMIT, so act like it's in that range.
                y = ((y - (-ylimit)) * MERCATOR_MAP_DIMENSION) / \
                    (ylimit * 2)
                y = int(round(y))

                # Elements of 'piece' are tuples, so can't modify directly
                piece[idx] = (x, y)

                # Track min and max.
                if x < xmin: xmin = x
                if x > xmax: xmax = x
                if y < ymin: ymin = y
                if y > ymax: ymax = y

    return (xmin, ymin, xmax, ymax)


# Find the center of all the points. That is, the midpoint between the leftmost
# and rightmost extremes, and the midpoint between the topmost and bottommost
# extremes.
def center(structs):
    minlat = 90
    maxlat = -90
    minlon = 180
    maxlon = -180

    latsum = 0
    latcount = 0
    lonsum = 0
    loncount = 0

    for struct in structs:
        for piece in struct['pieces']:
            for lat, lon in piece:
                if lat < minlat: minlat = lat
                if lat > maxlat: maxlat = lat
                if lon < minlon: minlon = lon
                if lon > maxlon: maxlon = lon

                latsum += lat
                latcount += 1
                lonsum += lon
                loncount += 1

    return (latsum / latcount, lonsum / loncount)
    return ((minlat + maxlat) / 2, (minlon + maxlon) / 2)
