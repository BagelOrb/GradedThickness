# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import trimesh
import numpy as np

#file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/3D_models/obj/cube.obj'
file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/3D_models/simple_shapes/cube_2cm.stl'
#file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 cell.stl'
#file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 cell__fixed.stl'
#file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 cell__thick.stl'
file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 cell__surface.stl'
file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 grid__thick.stl'
file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid bridging v4 3x3x3 grid__thick.stl'
file = 'C:/Users/t.kuipers/OneDrive - Ultimaker B.V/Documents/PhD/Gyroid/Overhang constrained/solid gyroid modelled grid__thick.stl'

# attach to logger so trimesh messages will be printed to console
trimesh.util.attach_to_log()


mesh = trimesh.load(file, force='mesh')

print("watertight:",     mesh.is_watertight)
print(mesh.euler_number)

Z_dim = 2

face_zs = mesh.vertices[mesh.faces][:,:,Z_dim]
face_is_horizontal = np.max(face_zs, 1) - np.min(face_zs, 1) < .0001
horizontal_face_indices = np.where(face_is_horizontal)
print("horizontal_faces: ", np.sum(face_is_horizontal))

print("n verts: ", mesh.vertices.shape)
print("n faces: ", mesh.faces.shape)

print("min: ", np.min(mesh.vertices, 0), "max: ", np.max(mesh.vertices, 0))
print("offsetting...")
offset = np.abs(mesh.vertices[:,0] * mesh.vertices[:,1] * mesh.vertices[:,2])
offset -= np.min(offset)
offset /= np.max(offset)
offset2 = (1 - np.abs(mesh.vertices[:,0]) / np.abs(np.max(mesh.vertices[:,0]))) * (1 - np.abs(mesh.vertices[:,1]) / np.abs(np.max(mesh.vertices[:,1]))) * (1 - np.abs(mesh.vertices[:,2]) / np.abs(np.max(mesh.vertices[:,2])))
offset += offset2
offset *= .05
offset += .01

print(offset.shape)
print(mesh.vertices.shape)
mesh.vertices += mesh.vertex_normals * np.repeat([offset], 3, axis=0).T
print("offsetted!")




if False:
    print("making faces horizontal...")
    if horizontal_face_indices[0].size > 0:
        for i in range(20):
            for f in range(horizontal_face_indices[0].shape[0]):
                face_vert_indices = mesh.faces[horizontal_face_indices[0][f]]
                face_verts = mesh.vertices[face_vert_indices]
                face_middle = np.average(face_verts[:, Z_dim])  # has to be done async because faces influence each other!
                for v in range(3):  # TODO: unroll this loop
                    vert = face_vert_indices[v]
                    mesh.vertices[vert][Z_dim] = face_middle
    print("finished horizontalizing!")




output_filename = file[:-4] + "__graded.stl"
with open(output_filename, "wb") as fout:
    mesh.export(fout, file_type="stl")
print("saved to ", output_filename)

# preview mesh in an opengl window if you installed pyglet with pip
# mesh.show()
