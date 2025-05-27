from .nodes import LoadLiveCCVideo, LoadLiveCCModel, LiveCCPrompt, LiveCC, SaveLiveCCText

NODE_CLASS_MAPPINGS = {
    "LoadLiveCCVideo": LoadLiveCCVideo,
    "LoadLiveCCModel": LoadLiveCCModel,
    "LiveCCPrompt": LiveCCPrompt,
    "LiveCC": LiveCC,
    "SaveLiveCCText": SaveLiveCCText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLiveCCVideo": "Load LiveCC Video",
    "LoadLiveCCModel": "Load LiveCC Model",
    "LiveCCPrompt": "LiveCC Prompt",
    "LiveCC": "LiveCC",
    "SaveLiveCCText": "Save LiveCC Text",
} 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
