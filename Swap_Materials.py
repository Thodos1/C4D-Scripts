"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
This plugin is very situational, it was made to swap materials with the same name.
Use Case - you have standard materials assigned and additionally you have Octane materials that have the same name and you need to add them.
This could be solved with Compare(), but it's broken in 2023 and 2024 C4D xD

"""
from typing import Optional
import c4d
#-----------------
#Select materials that will be replacing existing and assigned

#-----------------
def main():
    # Get selected tags
    All_obj = doc.GetObjects()

    # Get selected materials
    selected_materials = doc.GetActiveMaterials()

    
    material_dict = {material.GetName() : material for material in selected_materials}
    for obj in All_obj:
        obj_tags = obj.GetTags()
        #print(obj_tags)
        if obj_tags:

            for tag in obj_tags:
                if tag.GetType() == 5616:
                    tag_name_corr = tag[c4d.TEXTURETAG_MATERIAL].GetName()
                    #print(tag_name_corr)
                    if tag_name_corr in material_dict:
                        tag[c4d.TEXTURETAG_MATERIAL] = material_dict[tag_name_corr]
                        #print(tag_name_corr)
                else:
                    pass

    # Update the Cinema 4D scene
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()
