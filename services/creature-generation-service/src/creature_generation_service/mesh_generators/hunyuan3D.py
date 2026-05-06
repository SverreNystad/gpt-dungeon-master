from PIL import Image

from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
from hy3dgen.texgen import Hunyuan3DPaintPipeline

model_path = "tencent/Hunyuan3D-2"
pipeline_shapegen = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(model_path)
pipeline_texgen = Hunyuan3DPaintPipeline.from_pretrained(model_path)


def generate_textured_mesh_from_image(image_path: str, output_path: str = "demo.glb"):
    image = Image.open(image_path).convert("RGBA")
    if image.mode == "RGB":
        rembg = BackgroundRemover()
        image = rembg(image)

    mesh = pipeline_shapegen(image=image)[0]
    mesh = pipeline_texgen(mesh, image=image)
    mesh.export(output_path)
    return mesh
