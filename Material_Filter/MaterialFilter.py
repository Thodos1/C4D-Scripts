import c4d
from c4d import gui

class MaterialFilterDialog(gui.GeDialog):
    def __init__(self):
        super().__init__()

    def CreateLayout(self):
        self.SetTitle("Material Filter")

        self.AddEditText(1001, c4d.BFH_SCALEFIT | c4d.BFV_TOP,0,0,c4d.EDITTEXT_ENABLECLEARBUTTON)
        self.UpdateMaterials("")
        return True

    def Command(self, id, msg):
        if id == 1001:
            input_text = self.GetString(1001).lower()
            self.UpdateMaterials(input_text)
        return True

    def UpdateMaterials(self, filter_text):
        doc = c4d.documents.GetActiveDocument()
        materials = doc.GetMaterials()

        for mat in materials:
            if filter_text in mat.GetName().lower() or filter_text == "":
                mat.ChangeNBit(c4d.NBIT_OHIDE, c4d.NBITCONTROL_CLEAR)  # Show the material
            else:
                mat.ChangeNBit(c4d.NBIT_OHIDE, c4d.NBITCONTROL_SET)  # Hide the material

        c4d.EventAdd()

    def AskClose(self):
        self.SetString(1001, "")
        self.UpdateMaterials("")
        c4d.EventAdd()  # Ensure the changes are applied before closing
        return super().AskClose()  # Dialog Close


if __name__ == "__main__":
    dlg = MaterialFilterDialog()
    dlg.Open(dlgtype=c4d.DLG_TYPE_ASYNC, defaultw=300)