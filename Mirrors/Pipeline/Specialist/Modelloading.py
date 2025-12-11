import numpy as np

class ReadingOBJ:
    def __init__(self, path, ExtractVertices: bool = True,
                             ExtractNormals: bool = True,
                             ExtractTexCoords: bool = True):
        self.path = path
        self.ExtractVertices = ExtractVertices
        self.ExtractNormals = ExtractNormals
        self.ExtractTexCoords = ExtractTexCoords
        self.Dictionary = {
            "Vertices": [],
            "Normals": [],
            "TexCoords": [],
            "Interleaved": []
        }
        self.read_file_v_vn_vt()

    def GetVBO_data(self):
        Data = self.Dictionary["Interleaved"]
        Data = np.array(Data, dtype=np.float32)
        return Data

    def read_file_v_vn_vt(self):
        with open(self.path, "r") as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue
                
                prefix = parts[0]
                if self.ExtractVertices and prefix == "v":
                    self.Dictionary["Vertices"].append(list(map(float, parts[1:])))
                elif self.ExtractTexCoords and prefix == "vt":
                    reverse_technique = self.FixingYAxis(parts[1:])
                    self.Dictionary["TexCoords"].append(list(map(float, reverse_technique)))
                elif self.ExtractNormals and prefix == "vn":
                    self.Dictionary["Normals"].append(list(map(float, parts[1:])))
                elif prefix == "f":
                    self.read_faces(parts[1:])

    def read_faces(self, face_data: str): 
        '''1/1/1 2/2/1 3/3/1 4/4/1'''
        vertex_indices = []
        normal_indices = []
        texcoord_indices = []

        for IndexAttrib in face_data:
            indices = IndexAttrib.split("/")
            if self.ExtractVertices and len(indices) > 0 and indices[0]:
                vertex_indices.append(int(indices[0]) - 1)  # OBJ is 1-indexed, convert to 0-indexed
            if self.ExtractTexCoords and len(indices) > 1 and indices[1]:
                texcoord_indices.append(int(indices[1]) - 1)
            if self.ExtractNormals and len(indices) > 2 and indices[2]:
                normal_indices.append(int(indices[2]) - 1)
        
        # Using GL_TRIANGLE_FAN style: 0, 1, 2 and 0, 2, 3
        for i in range(1, len(vertex_indices) - 1):
            self.add_interleaved(vertex_indices[0], texcoord_indices[0], normal_indices[0])
            self.add_interleaved(vertex_indices[i], texcoord_indices[i], normal_indices[i])
            self.add_interleaved(vertex_indices[i + 1], texcoord_indices[i + 1], normal_indices[i + 1])

    def add_interleaved(self, v_idx, t_idx, n_idx):
        """Adds interleaved vertex data (vertex, texcoord, normal) to the dictionary."""
        vertex = self.Dictionary["Vertices"][v_idx] if self.ExtractVertices else []
        texcoord = self.Dictionary["TexCoords"][t_idx] if self.ExtractTexCoords else []
        normal = self.Dictionary["Normals"][n_idx] if self.ExtractNormals else []
        interleaved_data = vertex + texcoord + normal
        self.Dictionary["Interleaved"].extend(interleaved_data)
    
    @staticmethod
    def FixingYAxis(parts: list[str]):
        '''
        Input sample: [0.4, 0.2, 0.5]
        Output sample: [0.4, 0.8, 0.5]
        Since Pygame axis is reversed
        '''
        # parts = original.split('/')
        # parts = [str(1 - float(part)) for part in parts]
        parts[1] = str(1 - float(parts[1]))
        return parts
    
if __name__ == "__main__":
    Cat = ReadingOBJ(r"D:\vspython\OPENGL_AFTER_C\Refined tutorial\Assets\Models\Table\table.obj")
    
    print(Cat.Dictionary["Interleaved"])
    