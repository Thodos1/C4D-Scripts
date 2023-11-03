"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
Had some issues with Project Asset Inspector not using local versions through Dropbox in Octane
Swaps paths in selected VDB objects
Nothing much

"""
from typing import Optional
import c4d
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    new_path = "PUT YOUR PATH TO THE FOLDER HERE"
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)
    for obj in objs:
        x_path = obj[c4d.VOLUMEOBJECT_VDB_FILE]
        file_n = os.path.basename(x_path)
        #print(file_n)
        upd_path = os.path.join(new_path, file_n)
        obj[c4d.VOLUMEOBJECT_VDB_FILE] = upd_path

    c4d.EventAdd()




if __name__ == '__main__':
    main()
