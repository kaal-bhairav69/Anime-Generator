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
pipe = StableDiffusionPipeline.from_single_file(
    "E:/models/anything-v4.0/anything-v4.0-pruned-fp32.safetensors",
    torch_dtype=torch.float32,
    variant="fp32"  # or remove this if not needed
)
print("Model partially loaded")

pipe.to("cpu")
print("Model moved to CPU")

print("Attaching VAE...")
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")
pipe.vae = vae

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
