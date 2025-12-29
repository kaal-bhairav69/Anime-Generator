import sys
import os
import torch
from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler
from diffusers import AutoencoderKL
import torch
import uuid
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("Loading model...")
pipe = StableDiffusionPipeline.from_pretrained(
    "nimit12/my_anything_model",  # or full URL if needed
    torch_dtype=torch.float32,
    use_safetensors=True,
)
pipe.to("cpu")
print(pipe.vae)

print("Attaching scheduler...")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.safety_checker = None
pipe.enable_attention_slicing()

print("Model loaded!")
def generate_image(prompt):
    negative_prompt = "blurry, deformed face, bad hands, bad anatomy,worst quality, low resolution, bad proportions"
    result = pipe(
        prompt,
        height=280,
        width=280,
        num_inference_steps=30,
        guidance_scale=9.0,
        negative_prompt=negative_prompt
    )
    image = result.images[0]
    from io import BytesIO
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
