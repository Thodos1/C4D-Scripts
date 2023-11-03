"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

WARNING! Works with tags selected on a single object! Will be updated.
Description: 
From selected tags on a single objects creates a decal behaviour with a plane that drives position, rotation and scale of the material in flat projection
So it's basically a Decal.
Works with any engine

"""

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def decals_geom_create(material_tag, matname, main_obj):

    plane_obj = c4d.BaseObject(c4d.Oplane)
    plane_obj.InsertUnder(main_obj)
    plane_obj.SetName(matname)
    plane_obj[c4d.PRIM_AXIS] = 5
    plane_obj[c4d.PRIM_PLANE_WIDTH] = 100
    plane_obj[c4d.PRIM_PLANE_HEIGHT] = 100
    plane_obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
    plane_obj[c4d.PRIM_PLANE_SUBW] = 1
    plane_obj[c4d.PRIM_PLANE_SUBH] = 1
    #abc = 3
    return plane_obj
def max_y_coord(node_master, root):
    list_y_coord = []
    _enabled = node_master.IsEnabled()
    #print(_enabled)
    nodes = [root]

    node = root.GetDown()
    while node is not None:
        #print("NODE IS: " + str(node))
        y_coord = node.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[101]
        list_y_coord.append(round(y_coord))

        node = node.GetNext()
    #print(list_y_coord)
    #print(max(list_y_coord, key=abs) if list_y_coord else 0)
    return max(list_y_coord, key=abs) if list_y_coord else 0



def xpresso_func(plane_obj, tag_m, node_master, root, x_boole, x_count, matname):
    
    if x_boole is True:
        max_y = max_y_coord(node_master, root)
        #print("MAX VALUE NOW: " + str(max_y))
        if max_y < 0:
            y_val = max_y - 50
        else:
            y_val = max_y + 50

    else:
        y_val = x_count*70
    plane_node = node_master.CreateNode(root, 400001000, None, -200, y_val)
    plane_node[c4d.GV_OBJECT_OBJECT_ID] = plane_obj
    plane_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.PRIM_PLANE_WIDTH, c4d.GV_PORT_FLAG_IS_VISIBLE)
    plane_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.PRIM_PLANE_HEIGHT, c4d.GV_PORT_FLAG_IS_VISIBLE)
    plane_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_POSITION, c4d.GV_PORT_FLAG_IS_VISIBLE)
    plane_node.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_ROTATION, c4d.GV_PORT_FLAG_IS_VISIBLE)

    if x_boole is True:
        # Defines Y size
        plane_node.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[109] = 70
        # Defines X size
        plane_node.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[108] = 75
    math_width = node_master.CreateNode(root, 400001121, None, -100, y_val-24)
    math_width[c4d.GV_MATH_FUNCTION_ID] = 3
    subContainerID = c4d.DescLevel(2000, c4d.DTYPE_SUBCONTAINER, c4d.ID_OPERATOR_MATH)
    inputID = c4d.DescLevel(1001, c4d.DTYPE_REAL, c4d.ID_OPERATOR_MATH);
    paramID = c4d.DescID(subContainerID, inputID)
    math_width.SetParameter(paramID, float(2.0), c4d.DESCFLAGS_SET_0)

    plane_width = plane_node.GetOutPort(0)
    math_width_inp = math_width.GetInPort(0)
    plane_width.Connect(math_width_inp)

    math_height = node_master.CreateNode(root, 400001121, None, -100, y_val-22)
    math_height[c4d.GV_MATH_FUNCTION_ID] = 3
    subContainerID = c4d.DescLevel(2000, c4d.DTYPE_SUBCONTAINER, c4d.ID_OPERATOR_MATH)
    inputID = c4d.DescLevel(1001, c4d.DTYPE_REAL, c4d.ID_OPERATOR_MATH);
    paramID = c4d.DescID(subContainerID, inputID)
    math_height.SetParameter(paramID, float(2.0), c4d.DESCFLAGS_SET_0)

    plane_height = plane_node.GetOutPort(1)
    math_height_inp_2 = math_height.GetInPort(0)
    plane_height.Connect(math_height_inp_2)



    mat_node = node_master.CreateNode(root, 400001000, None, 20, y_val)
    mat_node[c4d.GV_OBJECT_OBJECT_ID] = tag_m
    mat_node[c4d.ID_BASELIST_NAME] = matname
    if x_boole is True:
        mat_node.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[109] = 70
        # Defines X size
        mat_node.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[108] = 75
    DID_POS_X: c4d.DescID = c4d.DescID(
        c4d.DescLevel(c4d.TEXTURETAG_SIZE, c4d.DTYPE_VECTOR, 0),
        c4d.DescLevel(c4d.VECTOR_X, c4d.DTYPE_REAL, 0))

    DID_POS_Y: c4d.DescID = c4d.DescID(
        c4d.DescLevel(c4d.TEXTURETAG_SIZE, c4d.DTYPE_VECTOR, 0),
        c4d.DescLevel(c4d.VECTOR_Y, c4d.DTYPE_REAL, 0))

    mat_node.AddPort(c4d.GV_PORT_INPUT, DID_POS_X, c4d.GV_PORT_FLAG_IS_VISIBLE)
    mat_node.AddPort(c4d.GV_PORT_INPUT, DID_POS_Y, c4d.GV_PORT_FLAG_IS_VISIBLE)
    mat_node.AddPort(c4d.GV_PORT_INPUT, c4d.TEXTURETAG_POSITION, c4d.GV_PORT_FLAG_IS_VISIBLE)
    mat_node.AddPort(c4d.GV_PORT_INPUT, c4d.TEXTURETAG_ROTATION, c4d.GV_PORT_FLAG_IS_VISIBLE)


    #plane_height = plane_node.GetOutPort(1)
    #math_height_inp_2 = math_height.GetInPort(0)
    math_width.GetOutPort(0).Connect(mat_node.GetInPort(0))
    math_height.GetOutPort(0).Connect(mat_node.GetInPort(1))
    plane_node.GetOutPort(2).Connect(mat_node.GetInPort(2))
    plane_node.GetOutPort(3).Connect(mat_node.GetInPort(3))






def main() -> None:
    tags = []
    tags_uns = doc.GetActiveTags()

    if not tags_uns:
        return
    for tg in tags_uns:
        if tg.GetType() == c4d.Ttexture:
            tags.append(tg)

    main_obj = tags[0].GetObject()
    

    xpresso_tag = None
    x_boole = True
    for tag in main_obj.GetTags():
        if tag.GetType() == c4d.Texpresso:
            xpresso_tag = tag
            break

    if xpresso_tag is None:

        xpresso_tag = c4d.BaseTag(c4d.Texpresso)
        main_obj.InsertTag(xpresso_tag)
        x_boole = False
        c4d.EventAdd()
        

    node_master = xpresso_tag.GetNodeMaster()
    root = node_master.GetRoot()
    
    new_xpresso_counter = 1

    for tag_m in tags:
        if tag_m[c4d.TEXTURETAG_PROJECTION] != 2:
            tag_m[c4d.TEXTURETAG_PROJECTION] = 2
        tag_m[c4d.TEXTURETAG_SIDE] = 1
        tag_m[c4d.TEXTURETAG_TILE] = False
        mat = tag_m[c4d.TEXTURETAG_MATERIAL]
        matname = mat.GetName()
        plane_obj = decals_geom_create(tag_m, matname, main_obj)
        new_xpresso_counter += 1
        xpresso_func(plane_obj, tag_m, node_master, root, x_boole, new_xpresso_counter, matname)
    child_o = main_obj.GetChildren()
    doc.SetSelection(child_o[0], c4d.SELECTION_NEW)
    c4d.CallCommand(1055908) # Place


    c4d.EventAdd()


if __name__ == '__main__':
    main()
