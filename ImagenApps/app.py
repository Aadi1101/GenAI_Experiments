import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDCM9fCkQAtCI5ouzIPH5gwYATdUev5J_A")
for model in genai.list_models():
    print(model,end=",")
# imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

# result = imagen.generate_images(
#     prompt="A vibrant young woman with white skin tone, long black hair, expressive features, and a confident pose. She is wearing a sleeveless top and stylish modern shorts, showcasing her physique. The setting is a simple outdoor park with warm light, green grass, and a clear sky, creating a peaceful and cheerful atmosphere. The focus is on her stylish appearance and dressing sense, drawn in a realistic and natural style.",
#     number_of_images=1,
#     safety_filter_level=None,
#     person_generation="allow_adult",
#     aspect_ratio="3:4",
#     negative_prompt=None,
# )

# for image in result.images:
#   print(image)

# # The output should look similar to this:
# # <vertexai.preview.vision_models.GeneratedImage object at 0x78f3396ef370>
# # <vertexai.preview.vision_models.GeneratedImage object at 0x78f3396ef700>
# # <vertexai.preview.vision_models.GeneratedImage object at 0x78f33953c2b0>
# # <vertexai.preview.vision_models.GeneratedImage object at 0x78f33953c280>

# for image in result.images:
#   # Open and display the image using your local operating system.
#   image._pil_image.show()