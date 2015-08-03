#!/usr/bin/python
#Created by Victoria Nelson July 31,2015
#Takes vertex and tri lists
#Removes duplicated vertexes and updates tri list
#IMPORTANT NOTE: ID starts at 1
__author__ = 'Tori'
import os
import sys

vfile = open("mb_verts_all_27_6.dat",'r')
vlines = vfile.readlines()
verts = vlines

nv = len(vlines)
trifile = open("mb_tri_all_27_6.dat",'r')
tlines = trifile.readlines()
ntri = len(tlines)
tri = [[0]*3 for i in range(ntri)]

for j in range(ntri): #Create matrix of the triangle list - tested
    tl = tlines[j].split()
    for k in range(3):
        tri[j][k] = int(tl[k])

for m in range(len(vlines)):
    vlines = verts
    for n in range(len(verts)):
        if (vlines[m] == verts[n] and n > m):#Finds duplicate vertex
            del verts[n]#Delete duplicate vertex
            for i in range(ntri):#Fix tri IDs
                for j in range(3):
                    if tri[i][j] > (n+1):#Account for removed vert from list
                        tri[i][j] = tri[i][j] - 1
                    elif tri[i][j] == (n+1):#Replace w/ new ID
                        tri[i][j] = m

triout = open("mb_clean_tri_all_27_6.dat",'w')
triout.write(tri)
vertout = open("mb_clean_verts_all_27_6.dat",'w')
vertout.write(verts)