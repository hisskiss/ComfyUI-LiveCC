from .src.infer import LiveCCDemoInfer


class LoadLiveCCVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {
                    "default": "demo/sources/howto_fix_laptop_mute_1080p.mp4",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "load_path"
    CATEGORY = "LiveCC"

    def load_path(self, video_path):
        video = video_path
        return (video,)


class LoadLiveCCModel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {
                    "default": "chenjoya/LiveCC-7B-Instruct",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_model"
    CATEGORY = "LiveCC"

    def load_model(self, model_path):
        model = model_path
        return (model,)


class Prompt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "query": ("STRING", {
                    "default": "Please describe the video.",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("TEXT",)
    RETURN_NAMES = ("text",)
    FUNCTION = "input_text"
    CATEGORY = "LiveCC"

    def input_text(self, query):
        text = query
        return (text,)


class LiveCC:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video": ("VIDEO", {}),
                "model": ("MODEL", {}),
                "text": ("TEXT", {}),
                "pixel_x": ("INT", {
                    "default": 384
                }),
                "pixel_y": ("INT", {
                    "default": 28
                }),
                "pixel_z": ("INT", {
                    "default": 28
                }),
                "repetition_penalty": ("FLOAT", {
                    "default": 1.05
                }),
                "streaming_eos_base_threshold": ("FLOAT", {
                    "default": 0.0
                }),
                "streaming_eos_threshold_step": ("FLOAT", {
                    "default": 0.0
                }),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("commentaries",)
    FUNCTION = "run_infer"
    CATEGORY = "LiveCC"

    def run_infer(self, video, model, text,
                  pixel_x, pixel_y, pixel_z,
                  repetition_penalty,
                  streaming_eos_base_threshold, streaming_eos_threshold_step):

        max_pixels = pixel_x * pixel_y * pixel_z

        infer = LiveCCDemoInfer(model_path=model)
        state = {'video_path': video}
                      
        commentaries = []
        
        t = 0
        for t in range(31):
            state['video_timestamp'] = t
            for (start_t, stop_t), response, state in infer.live_cc(
                message=text, state=state, 
                max_pixels=max_pixels, repetition_penalty=repetition_penalty, 
                streaming_eos_base_threshold=streaming_eos_base_threshold, 
                streaming_eos_threshold_step=streaming_eos_threshold_step
            ):
                print(f'{start_t}s-{stop_t}s: {response}')
                commentaries.append([start_t, stop_t, response])
                
            if state.get('video_end', False):
                break
            
            t += 1

        return (commentaries,)


class SaveLiveCCText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "commentaries": ("LIST", {}),
                "output_path": ("STRING", {
                    "default": "./livecc_output.txt",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "save_text"
    CATEGORY = "LiveCC"

    def save_text(self, commentaries, output_path):
        commentaries_list = commentaries
        lines = []
        for start_t, stop_t, text in commentaries_list:
            lines.append(f"{start_t}s - {stop_t}s: {text}")
        
        text_output = "\n".join(lines)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_output)

        return (output_path,)


