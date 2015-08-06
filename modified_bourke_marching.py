# Modified by Victoria Nelson July 20, 2015
# VN:Each vertex has an index
# VN:Each tetrahedron has four indices that correspond to four vertices
# VN:Used Delaunay triangulation to find tetrahedron list
# VN:Need to assign index to each vertex in list (so keep attr associated with vertex)

# VN:Take attr list - assign each line an index
# VN:Take Connectivity list (list of tetrahedrons)
# VN:Remove g variable (gridcell)

# VN:INPUT Vertex List FILE FORMAT:X Y Z ATTR...
# VN:Also take Face List file - tetrahedrons, 4 vertex IDs

class Vector:  # struct XYZ
    vID = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)


# class Gridcell: # struct GRIDCELL
# def __init__(self,p,n,val):
#  self.p   = p   # p=[8]
#  self.n   = n   # n=[8]
# self.val = val # val=[8]

class Point:  # VN:associate attr values with ID
    def __init__(self, x, y, z, a1, u, v, w, t, s, c):
        #  self.x = x
        #  self.y = y
        #  self.z = z
        self.p = Vector(x, y, z)
        self.a1 = a1
        self.v = Vector(u, v, w)
        self.a = Vector(t, s, c)


class Interp:
    def __init__(self, vID, x, y, z, iu, iv, iw, it, isal, ic):
        self.ID = vID
        self.p = Vector(x, y, z)
        self.v = Vector(iu, iv, iw)
        self.a = Vector(it, isal, ic)

    def __str__(self):
        return """%s %s %s""" % (self.p, self.v, self.a)  # ,self.v)


class Triangle:  # struct TRIANGLE
    def __init__(self, v1, v2, v3):
        self.p = [v1, v2, v3]
        self.ID1 = v1.ID
        self.ID2 = v2.ID
        self.ID3 = v3.ID
        self.p1 = v1
        self.p2 = v2
        self.p3 = v3

    # VN: Change to PLY format
    # return triangle as an ascii STL facet
    def __str__(self):
        return"""facet normal 0 0 0
outer loop
vertex %s
vertex %s
vertex %s
endloop
endfacet"""%(self.p[0],self.p[1],self.p[2])

        #"""%s %s %s
#%s
#%s
#%s""" % (self.ID1, self.ID2, self.ID3, self.p1, self.p2, self.p3)

def main():
    import sys
    #vID = 0
    ID = 1
    triangles = []
    #isostr = sys.argv[1]
    isolevel = 27.6 #float(isostr)
    # vert = [None]*190001
    sID = [None] * 190001
    for line in open("mb_sphere_sig_all.xyz"):  # MESH AND ATTR FILE
        items = line.split()
        density = float(items[3])
        if density >= 999: density = 100.0
        # vert[ID] = Vector(float(items[0]),float(items[1]),float(items[2]))
        sID[ID] = Point(float(items[0]), float(items[1]), float(items[2]), density, float(items[4]), float(items[5]),
                        float(items[6]), float(items[7]), float(items[8]), float(items[9]))
        ID = ID + 1  # Range from 1 to 190000

    for line in open("clean_sphere_delaunay_tetras.dat"):
        verts = line.split()
        f1 = int(verts[0])
        f2 = int(verts[1])
        f3 = int(verts[2])
        f4 = int(verts[3])

        triangles.extend(PolygoniseTri(isolevel, sID[f1], sID[f2], sID[f3], sID[f4]))  # Repeat for each tetrahedron

    export_triangles(triangles)



def export_triangles(triangles):  # stl format; VN: not anymore
    print("solid points")
    #output = ("mb_all_newline_27_6.dat",'w')
    for tri in triangles:
        print tri
    print("endsolid points")


def t000F(iso, f0, f1, f2, f3):
    return []


def t0E01(iso, f0, f1, f2, f3):
    return [Triangle(
        VertexInterp(iso, f0, f1), # .p, f0.a1, f1.a1, f0.v, f1.v, f0.a, f1.a),
        VertexInterp(iso, f0, f2), #.p, f0.a1, f2.a1, f0.v, f2.v, f0.a, f2.a),
        VertexInterp(iso, f0, f3)) #.p, f0.a1, f3.a1, f0.v, f3.v, f0.a, f3.a))
    ]


def t0D02(iso, f0, f1, f2, f3):
    return [Triangle(
        VertexInterp(iso, f1, f0), #.p, f1.a1, f0.a1, f1.v, f0.v, f1.a, f0.a),
        VertexInterp(iso, f1, f3), #.p, f1.a1, f3.a1, f1.v, f3.v, f1.a, f3.a),
        VertexInterp(iso, f1, f2)) #.p, f1.a1, f2.a1, f1.v, f2.v, f1.a, f2.a))
    ]


def t0C03(iso, f0, f1, f2, f3):
    tri = Triangle(
        VertexInterp(iso, f0, f3), #.p, f0.a1, f3.a1, f0.v, f3.v, f0.a, f3.a),
        VertexInterp(iso, f0, f2), # .p, f0.a1, f2.a1, f0.v, f2.v, f0.a, f2.a),
        VertexInterp(iso, f1, f3)) #.p, f1.a1, f3.a1, f1.v, f3.v, f1.a, f3.a))
    return [tri, Triangle(
        tri.p[2],
        VertexInterp(iso, f1, f2), #.p, f1.a1, f2.a1, f1.v, f2.v, f1.a, f2.a),
        tri.p[1])
            ]


def t0B04(iso, f0, f1, f2, f3):
    return [Triangle(
        VertexInterp(iso, f2, f0), #.p, f2.a1, f0.a1, f2.v, f0.v, f0.a, f2.a),
        VertexInterp(iso, f2, f1), #f2.a1, f1.a1, f2.v, f1.v, f2.a, f1.a),
        VertexInterp(iso, f2, f3)) # f2.a1, f3.a1, f2.v, f3.v, f2.a, f3.a))
    ]


def t0A05(iso, f0, f1, f2, f3):
    tri = Triangle(
        VertexInterp(iso, f0, f1), #.p, f0.a1, f1.a1, f0.v, f1.v, f0.a, f1.a),
        VertexInterp(iso, f2, f3), # f2.a1, f3.a1, f2.v, f3.v, f2.a, f3.a),
        VertexInterp(iso, f0, f3)) # f0.a1, f3.a1, f0.v, f3.v, f0.a, f3.a))
    return [tri, Triangle(
        tri.p[0],
        VertexInterp(iso, f1, f2), #, f1.a1, f2.a1, f1.v, f2.v, f1.a, f2.a),
        tri.p[1])
            ]


def t0906(iso, f0, f1, f2, f3):
    tri = Triangle(
        VertexInterp(iso, f0, f1), #.p, f0.a1, f1.a1, f0.v, f1.v, f0.a, f1.a),
        VertexInterp(iso, f1, f3), #.p, f1.a1, f3.a1, f1.v, f3.v, f1.a, f3.a),
        VertexInterp(iso, f2, f3)) #.p, f2.a1, f3.a1, f2.v, f3.v, f2.a, f3.a))
    return [tri,
            Triangle(
                tri.p[0],
                VertexInterp(iso, f0, f2), #.p, f0.a1, f2.a1, f0.v, f2.v, f0.a, f2.a),
                tri.p[2])
            ]


def t0708(iso, f0, f1, f2, f3):
    return [Triangle(
        VertexInterp(iso, f3, f0), #.p, f3.a1, f0.a1, f3.v, f0.v, f3.a, f0.a),
        VertexInterp(iso, f3, f2), #.p, f3.a1, f2.a1, f3.v, f2.v, f3.a, f2.a),
        VertexInterp(iso, f3, f1)) #.p, f3.a1, f1.a1, f3.v, f1.v, f3.a, f1.a))
    ]


# VN:This is a dictionary
trianglefs = {7: t0708, 8: t0708, 9: t0906, 6: t0906, 10: t0A05, 5: t0A05, 11: t0B04, 4: t0B04, 12: t0C03, 3: t0C03,
              13: t0D02, 2: t0D02, 14: t0E01, 1: t0E01, 0: t000F, 15: t000F}


def PolygoniseTri(iso, f0, f1, f2, f3):
    triangles = []

    #   Determine which of the 16 cases we have given which vertices
    #   are above or below the isosurface
    b0 = f0.a1
    b1 = f1.a1
    b2 = f2.a1
    b3 = f3.a1

    triindex = 0;
    if b0 < iso: triindex |= 1
    if b1 < iso: triindex |= 2
    if b2 < iso: triindex |= 4
    if b3 < iso: triindex |= 8
    return trianglefs[triindex](iso, f0, f1, f2, f3)


# VN:Don't include missing values!
# VN:Find new point, interpolate velocity components and additional attributes
from math import sqrt


def VertexInterp(isolevel, f1, f2): # val1, val2, vel1, vel2, attr1, attr2):
    Vector.vID = Vector.vID + 1
    tolerance = 0.00001
    vert1 = f1.p
    vert2 = f2.p
    vel1 = f1.v
    vel2 = f2.v
    attr1 = f1.a
    attr2 = f2.a
    val1 = f1.a1
    val2 = f2.a1
    if abs(isolevel - val1) < tolerance:
        vert1.vID = Vector.vID
        return vert1, vel1, attr1
    if abs(isolevel - val2) < tolerance:
        vert2.vID = Vector.vID
        return vert2, vel2, attr2
    if abs(val1 - val2) < tolerance:
        vert1.vID = Vector.vID
        return vert1, vel1, attr1
    mu = (isolevel - val1) / (val2 - val1)
    xnr = vert1.x + mu * (vert2.x - vert1.x)
    ynr = vert1.y + mu * (vert2.y - vert1.y)
    znr = vert1.z + mu * (vert2.z - vert1.z)
    xnew = round(xnr, 3)
    ynew = round(ynr, 3)
    znew = round(znr, 3)
    a = sqrt(
        (xnew - vert1.x) * (xnew - vert1.x) + (ynew - vert1.y) * (ynew - vert1.y) + (znew - vert1.z) * (znew - vert1.z))
    b = sqrt(
        (vert2.x - xnew) * (vert2.x - xnew) + (vert2.y - ynew) * (vert2.y - ynew) + (vert2.z - znew) * (vert2.z - znew))
    weight = a / (a + b)
    iu = vel1.x + (vel2.x - vel1.x) * weight
    iv = vel1.y + (vel2.y - vel1.y) * weight
    iw = vel1.z + (vel2.z - vel1.z) * weight
    it = attr1.x + (attr2.x - attr1.x) * weight
    isal = attr1.y + (attr2.y - attr1.y) * weight
    ic = attr1.z + (attr2.z - attr1.z) * weight
    if iu >= 999: #VN: Make sure missing values stay missing (missing data flag is 999)
        iw = 999.98999023
        it = 999.98999023
        isal = 999.98999023
        ic = 999.98999023
    point = Vector(xnew, ynew, znew)
    point.vID = Vector.vID
    vel_vec = Vector(iu, iv, iw)
    # output.write(point,vel_vec,"\n")
    return Interp(point.vID, xnew, ynew, znew, iu, iv, iw, it, isal, ic)


if __name__ == "__main__":
    main()
