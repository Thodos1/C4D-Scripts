"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
Part of the code from SMART SPLIT
Select objects and this script will parse through texture tags and selections.
Deletes empty selection tags, material tags to them and empty material tags.

"""

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    for obj in objs:
        tags = obj.GetTags()
        for tag in tags:
            if tag.GetType() == 5616:

                my_selection_tag_name = tag[c4d.TEXTURETAG_RESTRICTION]
                if tag[c4d.TEXTURETAG_MATERIAL] == None:
                    tag.Remove()

                elif my_selection_tag_name is not None:
                    for sel_tg in tags:
                        if sel_tg.GetType() == 5673 and sel_tg.GetName() == my_selection_tag_name:

                            if sel_tg.GetBaseSelect().GetCount() == 0:
                                sel_tg.Remove()
                                tag.Remove()
                                print(f"The selection {sel_tg.GetName()} tag is empty.")
                            else:
                                print(f"The selection {sel_tg.GetName()} tag is not empty.")
                else:
                    print(f"The selection {sel_tg.GetName()} tag does not exist.")
    c4d.EventAdd()

if __name__ == '__main__':
    main()
