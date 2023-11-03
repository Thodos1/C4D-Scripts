"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
R&D into why most render engines treat MoGraph Color as a bitmap - it limits MoGraph colour split.
With similar behaviour as in the script, it's possible to make a dynamic node that will eat vector data and create inputs for each vector group!
ESPECIALLY IN OCTANE!

"""
from typing import Optional
import c4d
from c4d.modules import mograph as mo

def main():
    # Get the active object
    active_object = doc.GetActiveObject()

    # Check if the active object is a MoGraph Cloner
    if not active_object or active_object.GetType() != 1018544:
        print("Select a MoGraph Cloner object.")
        return

    # Initialize the MoGraph selection
    md = mo.GeGetMoData(active_object)
    if md is None:
        return

    # Access clone data (assuming it's color for this example)
    clone_data = md.GetArray(c4d.MODATA_COLOR)

    # Set to hold unique vectors
    unique_vectors = set()

    # Dictionary to hold vector: [index1, index2,...]
    vector_dict = {}

    # Identify unique vectors
    for i, vector in enumerate(clone_data):
        #print(vector)
        # Converting the vector to a tuple so it can be added to a set
        vector_tuple = (vector.x, vector.y, vector.z)
        #print(vector_tuple)
        unique_vectors.add(vector_tuple)

    # Loop to identify indices for each unique vector
    for vector in unique_vectors:
        vector_dict[vector] = []
        for i, clone in enumerate(clone_data):
            clone_tuple = (clone.x, clone.y, clone.z)
            if vector == clone_tuple:
                vector_dict[vector].append(i)

    # Print out the vectors and their corresponding indices
    for vector, indices in vector_dict.items():
        print(f"Vector {vector}: {indices}")

if __name__=='__main__':
    main()
