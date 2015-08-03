#!/usr/bin/python
#Created by Victoria Nelson July 31,2015
#Takes vertex and tri lists
#Removes duplicated vertexes and updates tri list
#IMPORTANT NOTE: ID in tri list starts at 1
__author__ = 'Tori'
import os
import sys

vfile = open("mb_verts_all_27_6.dat",'r')
vlines = vfile.readlines()
verts = vlines

nv = len(vlines)
print nv
trifile = open("mb_tri_all_27_6.dat",'r')
tlines = trifile.readlines()
ntri = len(tlines)
tri = [[0]*3 for i in range(ntri)]

for j in range(ntri): #Create matrix of the triangle list - tested
    tl = tlines[j].split()
    for k in range(3):
        tri[j][k] = int(tl[k])
s = 0
for v in vlines:
    if s > 10: break

    coo = v.split()
    vx = float(coo[0])
    vy = float(coo[1])
    vz = float(coo[2])
    m = vlines.index(v)
    for vert in verts:
        ver = vert.split()
        vertx = float(ver[0])
        verty = float(ver[1])
        vertz = float(ver[2])

        if vertx == vx and verty == vy and vertz == vz and verts.index(vert) > m:#Finds duplicate vertex
            num = verts.count(v)
            print vert, len(verts), num
            n = verts.index(vert)
            #m = vlines.index(v)
            print m,n
            del verts[n] #Delete duplicate vertex
            s = s+1
            print s
            for i in range(ntri):#Fix tri IDs
                for j in range(3):
                    if tri[i][j] > (n+1):#Account for removed vert from list
                        tri[i][j] = tri[i][j] - 1
                    elif tri[i][j] == (n+1):#Replace w/ new ID
                        tri[i][j] = m+1
    vlines = verts

vertout = open("mb_clean_verts_all_27_6.dat",'w')
for vert in verts:
    vertout.write(vert)
triout = open("mb_clean_tri_all_27_6.dat",'w')
for t in tri:
    for i in range(3):
        triout.write(str(t[i])+" ")
    triout.write("\n")

