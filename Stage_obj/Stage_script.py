from typing import Optional
import c4d

doc: c4d.documents.BaseDocument # The document evaluating this tag
op: c4d.BaseTag # The Python scripting tag
flags: int # c4d.EXECUTIONFLAGS
priority: int # c4d.EXECUTIONPRIORITY

tp: Optional[c4d.modules.thinkingparticles.TP_MasterSystem] # Particle system
bt: Optional[c4d.threading.BaseThread] # The thread executing this tag

def main() -> None:
    #print(op[c4d.ID_USERDATA,3])
    if op[c4d.ID_USERDATA,3] == 1:
        viewport: c4d.BaseDraw = doc.GetRenderBaseDraw()
        View_cam = viewport[c4d.BASEDRAW_DATA_CAMERA]

        if View_cam != op[c4d.ID_USERDATA,2]:
            #View_cam = op[c4d.ID_USERDATA,2]
            viewport.SetSceneCamera(op[c4d.ID_USERDATA,2], False)
            #print("Changing Camera")

