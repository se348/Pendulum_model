import numpy as np

class LoadMesh:
    buffer = []

    @staticmethod
    def create_texturized_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: 
                start = ind * 3
                end = start + 3
                LoadMesh.buffer.extend(vertices[start:end])
            elif i % 3 == 1: 
                start = ind * 2
                end = start + 2
                LoadMesh.buffer.extend(textures[start:end])
            elif i % 3 == 2: 
                start = ind * 3
                end = start + 3
                LoadMesh.buffer.extend(normals[start:end])


    @staticmethod
    def load_model(file):
        vert_coords = []
        tex_coords = [] 
        norm_coords = []

        all_indices = []
        indices = [] 


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                print(line)
                for d in values:
                    if values[0] == 'v':
                        if d == "v":
                            continue
                        vert_coords.append(float(d))
                    elif values[0] == 'vt':
                        if d == "vt":
                            continue
                        tex_coords.append(float(d))
                    elif values[0] == 'vn':
                        if d == "vn":
                            continue
                        norm_coords.append(float(d))
                if values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        for d in val:
                            if d == "vn":
                                continue
                            all_indices.append(int(d)-1)
                        indices.append(int(val[0])-1)

                line = f.readline()

      
        LoadMesh.create_texturized_buffer(all_indices, vert_coords, tex_coords, norm_coords)
      

        buffer = LoadMesh.buffer.copy() 
        LoadMesh.buffer = [] 

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')