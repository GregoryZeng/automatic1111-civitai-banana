
# Deploy any Civitai model as API in 🍌Banana

Deploy an API for AUTOMATIC1111's [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) to generate images with any model from [Civitai](https://civitai.com/).
[Banana](https://www.banana.dev/) is a serverless GPU platform.

Currently supported Civitai model types:
- [x] Checkpoint
- [ ] TextualInversion
- [ ] Hypernetwork
- [ ] AestheticGradient
- [ ] LORA
- [ ] Controlnet
- [ ] Poses

This deployment provides an API only and does not include the WebUI's user interface. Please report any issues you encounter.


## Deploy a model
1. Clone this repo.
2. Find the civitai you would like to deploy. [Take this model as an example](https://civitai.com/models/4201/realistic-vision-v20).
3. Right click the `Download Latest` (or `Download` button for previous versions) and select `Copy Link Address`. Now you get a URL like `https://civitai.com/api/download/models/[NUMBER]` in your clipboard.
4. Edit the `Dockerfile` and substitue the original string after `ARG MODEL_URL=` with the civitai model URL.
5. Commit and git push the changes to your personal repo.
6. You can now deploy your model in [Banana Deploy](https://app.banana.dev/deploy). Select `Deploy from Github` and choose your repo.

## Inference

After the `Status` field in your model page turns to `Deployed`, you can send requests to perform inference.

```python
import banana_dev as banana

api_key = "YOUR_API_KEY_HERE"
model_key = "YOUR_MODEL_KEY"
model_inputs = {'endpoint': 'txt2img', 'params': {'prompt': 'RAW photo, a close up portrait photo of 26 y.o woman in wastelander clothes, long haircut, pale skin, slim body, background is city ruins, (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3', 'negative_prompt': '(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck', 'steps': 25, 'sampler_name': 'Euler a', 'cfg_scale': 7.5, 'seed': 42, 'batch_size': 1, 'n_iter': 1, 'width': 768, 'height': 768, 'tiling': False}}

out = banana.run(api_key, model_key, model_inputs)
```

You should be able to save the generated image by:
```python
import base64
import io
from PIL import Image

base64img = out['modelOutputs'][0]['images'][0]
Image.open(io.BytesIO(base64.b64decode(base64img.split(",",1)[0]))).save('output1.png')
```
