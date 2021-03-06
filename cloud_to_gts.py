import numpy as np
from scipy.spatial import Delaunay
import math

'''
This python utility contains functions that allow a .xyz file to be converted into a .gts file.

GTS is the GNU Triangulated Surface Library for C. 

For Reference (this was surprisingly hard to find in the documentation):
    The file format is as follows
    First line:     np ne nv
                    (np = number of points, ne = number of edges, nf = number of faces)
    Next np lines:  coordinates of each point
    Next ne lines:  indices of each edge's pair of points
    Next nf lines:  indices of each face's edges
'''

'''
Function:   input_triangulation()
Use:        return Delaunay triangulation of input .xyz file
'''
def input_triangulation(testing):

    filename = "bunny.xyz"
    subsample_rate = 5

    if (not testing):
        filename = input("Input file name: ")
        subsample_rate = int(input("Subsampling rate (0 for none): "))

    f = open(filename, 'r')

    p = []

    # Read points from the file into numpy array
    for l in f:
        row = l.split()
        p.append([row[0], row[1], row[2]])
        # in case there are two 'columns' in the file
        if (len(row) == 6):
            p.append([row[3], row[4], row[5]])

    points = np.array(p)

    # Perform subsampling (really noticeable impact with large datasets)
    if (subsample_rate > 0):
        points = points[::subsample_rate]

    print("Points Loaded")

    tri = Delaunay(points[:-1], qhull_options="Qbb Qc Qz Q12 QJ Qt")

    print("Triangulation Complete")

    return tri, points;


'''
Function:   gts_to_cloud()
Use:        convert a gts file into an xyz file
'''
def gts_to_cloud(filename, out_filename):

    f = open(filename, 'r')

    num_points = 0
    string_write = ""
    rowcount = 0

    for l in f:
        row = l.split()
        if (rowcount == 0):
            num_points = int(row[0])
        elif (rowcount < num_points+1):
            string_write += l
        rowcount += 1

    out_f = open(out_filename, 'w')
    out_f.write(string_write)

        

'''
Function:   gts_write()
Use:        convert point cloud into gts file for non iterative
            algorithm execution
'''
def gts_write(tri, points, testing):

    filename = "bunny_mesh.gts"
    if (not testing):
        filename = input("Initial GTS generation filename: ")

    print("Formatting mesh data...")

    num_points = points.shape[0]
    
    edges = []
    for s in tri.simplices:
        p1 = s[0] + 1
        p2 = s[1] + 1
        p3 = s[2] + 1
        edges.append([p1, p2])
        edges.append([p2, p3])
        edges.append([p3, p1])

    num_edges = len(edges)

    faces = []
    count = 1
    for s in tri.simplices:
        faces.append([count, count+1, count+2])
        count += 3

    num_faces = len(faces)

    f = open(filename, 'w')

    print("Writing to GTS file...")

    string_write = ""
    string_write += str(num_points) + " " + str(num_edges) + " " + str(num_faces) + "\n"
    for p in points:
        string_write += str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n"
    for e in edges:
        string_write += str(e[0]) + " " + str(e[1]) + "\n"
    for x in faces:
        string_write += str(x[0]) + " " + str(x[1]) + " " + str(x[2]) + "\n"
    f.write(string_write)

    return filename

