
import bpy
import random

def div2(pol, rand_factor=0.5):
    ((x1,y1),(x4,y4)) = pol
    if x4-x1 < y4-y1:
        ymid = round(y1 + 0.5*(y4-y1) + rand_factor*(random.random()-0.5)*(y4-y1),3)
        (x2,y2) = (x4,ymid)
        (x3,y3) = (x1,ymid)
    else:
        xmid = round(x1 + 0.5*(x4-x1) + rand_factor*(random.random()-0.5)*(x4-x1),3)
        (x2,y2) = (xmid,y4)
        (x3,y3) = (xmid,y1)
    return [((x1,y1),(x2,y2)),((x3,y3),(x4,y4))]

def divn(parent, depth, rand_factor=0.5):
    acca = div2(parent, rand_factor)
    accb = []
    for i in range(depth):
        accb = []
        for p in acca:
            accb.extend(div2(p, rand_factor))
        acca = accb
    return accb

y_dim=5
x_dim=5
dep=1
rf=0.5

top = [[(x1,y1,z),(x2,y1,z),(x2,y2,z),(x1,y2,z)]
        for ((x1,y1),(x2,y2)) in divn(((-x_dim/2, -y_dim/2), (x_dim/2, y_dim/2)), dep, rf)
        for z in [round(random.random(),3)]]

top_verts = [item for sublist in top for item in sublist]
bot_verts = []

for v in top_verts:
    if (v[0],v[1],0.0) not in bot_verts:
        bot_verts.append((v[0],v[1],0.0))

top_faces = []
side_faces = []

for i in range(0,len(top_verts),4):
    top_faces += [ (i,i+1,i+2,i+3) ]
    for (a,b) in [ (i,i+1), (i+1,i+2), (i+2,i+3), (i+3,i) ]:
        c = bot_verts.index((top_verts[a][0],top_verts[a][1],0.0))+len(top_verts)
        d = bot_verts.index((top_verts[b][0],top_verts[b][1],0.0))+len(top_verts)
        side_faces.append((c,d,b,a))

verts = top_verts+bot_verts
faces = top_faces+side_faces

me = bpy.data.meshes.new("WhateverMesh")
ob = bpy.data.objects.new("Whatever", me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(verts,[],faces)
me.update(calc_edges=True)
