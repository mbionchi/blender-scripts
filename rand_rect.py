
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
extra_verts = []

for p in top:
    (x1,y1,z1) = p[0]
    (x2,y2,z2) = p[2]
    right = set()
    left = set()
    up = set()
    down = set()
    for q in top:
        for (x,y,z) in q:
            if p != q:
                if x2 == x and y1 < y and y < y2:
                    right.add((x,y,z1))
                if x1 == x and y1 < y and y < y2:
                    left.add((x,y,z1))
                if y2 == y and x1 < x and x < x2:
                    up.add((x,y,z1))
                if y1 == y and x1 < x and x < x2:
                    down.add((x,y,z1))
    right = list(right)
    left = list(left)
    up = list(up)
    down = list(down)
    right.sort(key=lambda x: x[1], reverse=True)
    left.sort(key=lambda x: x[1], reverse=True)
    up.sort()
    down.sort(reverse=True)
    [p.insert(1,x) for x in down]
    [p.insert(2+len(down),x) for x in right]
    [p.insert(3+len(down)+len(right),x) for x in up]
    p.extend(left)

top_verts = [item for sublist in top for item in sublist]

faces = []
running_len = 0
for p in top:
    faces.append(tuple(range(running_len,running_len+len(p))))
    running_len += len(p)

for p in top:
    for i,j in [(x,x+1) for x in range(len(p)-1)]+[(len(p)-1,0)]:
        (x1,y1,z1) = p[i]
        (x2,y2,z2) = p[j]
        for q in top:
            if p != q:
                for k,l in [(x,x+1) for x in range(len(q)-1)]+[(len(q)-1,0)]:
                    (x4,y4,z4) = q[k]
                    (x3,y3,z3) = q[l]
                    if (x3,y3) == (x1,y1) and (x4,y4) == (x2,y2):
                        w = top_verts.index((x1,y1,z1))
                        x = top_verts.index((x2,y2,z2))
                        y = top_verts.index((x4,y4,z4))
                        z = top_verts.index((x3,y3,z3))
                        faces.append((z,y,x,w))

verts = []
verts.extend(top_verts)

me = bpy.data.meshes.new("WhateverMesh")
ob = bpy.data.objects.new("Whatever", me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(verts,[],faces)
me.update(calc_edges=True)
