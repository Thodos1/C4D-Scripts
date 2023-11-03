"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
Execute and click on a MatCap image - create a material that works like a MatCap with selected image
MatCap folder is dynamic so that you can add more matcaps.
Tested on 200mb folder, works slower on initialize, but chugs through it.

"""
import os

from collections import defaultdict
import c4d
from c4d import gui



class TextureSetsDialog(gui.GeDialog):
    def __init__(self):
        self.script_directory = os.path.dirname(__file__)
        self.textures_directory = "MatCaps"
        self.texture_paths = []


        textures_directory_path = os.path.join(self.script_directory, self.textures_directory)

        if os.path.exists(textures_directory_path) and os.path.isdir(textures_directory_path):
            # Iterate through the files in the directory
            for filename in os.listdir(textures_directory_path):
                # Check if the file is an image (you can customize this check based on your file extensions)
                if filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                    # Build the full path to the texture
                    texture_path = os.path.join(textures_directory_path, filename)
                    # Add the (index, path) pair to the list
                    self.texture_paths.append(texture_path)


    def CreateLayout(self):




        self.SetTitle("MatCaps")

        self.GroupBegin(3232, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=2, rows=2, initw=0, inith=125)



        scroll_group = self.ScrollGroupBegin(10001, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, c4d.SCROLLGROUP_VERT, 0, 0)
        self.GroupBegin(scroll_group, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=5, rows=0)
        

        bc: c4d.BaseContainer = c4d.BaseContainer()
        bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        bc.SetInt32(c4d.BITMAPBUTTON_BORDER,c4d.BORDER_ACTIVE_4)
        bc.SetInt32(c4d.BITMAPBUTTON_OUTBORDER,c4d.BORDER_ACTIVE_3)
        bc.SetInt32(c4d.BITMAPBUTTON_BACKCOLOR, c4d.COLOR_BORDER_ACTIVE_4)
        #bc.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)

        for i, filename in enumerate(self.texture_paths):

            first_texture = c4d.bitmaps.BaseBitmap()
            first_texture.InitWith(filename)
            #print("wowrked path")

            preview_size = 128
            preview_texture = c4d.bitmaps.BaseBitmap()
            preview_texture.Init(preview_size, preview_size, first_texture.GetBt())
            first_texture.ScaleIt(preview_texture, 256, True, False)


            bmp_btn = self.AddCustomGui(4200+i, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, bc)
            bmp_btn.SetImage(preview_texture, True)
            

        





        self.GroupEnd()



        self.GroupEnd()
        self.GroupEnd()
        self.AddButton(3000, c4d.BFH_FIT | c4d.BFV_BOTTOM, 25, 30, name="Create Materials")
        self.GroupEnd()
        return True

    def Command(self, id, msg):
        if 4200 <= id <= 4300 + len(self.texture_paths) - 1:
            corr_id = id - 4200
            path = self.texture_paths[corr_id]
            self.gen_material(path)

        return True

    def gen_material(self, path):
        c4d_name = "MatCap_mat.c4d"
        mat_c4d = os.path.join(self.script_directory, c4d_name)
        c4d.documents.MergeDocument(doc, mat_c4d, c4d.SCENEFILTER_MATERIALS)
        c4d.EventAdd()


        mat = doc.GetFirstMaterial()
        Art_shader = mat[c4d.MATERIAL_COLOR_SHADER]
        Bitmap_shd = Art_shader[c4d.ARTSHADER_TEXTURE]
        Bitmap_shd[c4d.BITMAPSHADER_FILENAME] = path
        #texturs = path
        #print(texturs)
        c4d.EventAdd()




# Open the dialog
dlg_mul = TextureSetsDialog()
dlg_mul.Open(dlgtype=c4d.DLG_TYPE_ASYNC)
