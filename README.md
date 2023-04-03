
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

### txt2img example

```
{
  "endpoint": "txt2img",
  "params": {
    "prompt": "an astronaut riding a (horse:motorcycle:0.5) on the moon",
    "negative_prompt": "cartoonish, low quality",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    "seed": 42,
    "batch_size": 1,
    "n_iter": 1,
    "width": 768,
    "height": 768,
    "tiling": false
    
  }
}
```

(Only `prompt` is required.)

Output:

```
{
  "images": [
    "<base64 image>"
  ]
}
```

### img2img example

```
{
  "endpoint": "img2img",
  "params": {
    "prompt": "an astronaut riding a horse on the moon in anime style",
    "negative_prompt": "cartoonish, low quality",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    "denoising_strength": 0.7,
    "seed": 42,
    "batch_size": 1,
    "n_iter": 1,
    "width": 768,
    "height": 768,
    "tiling": false
    "init_images": [
        "<base64 image>"
    ]
  }
}
```

(Only `prompt` and `init_images` are required.)

Output:

```
{
  "images": [
    "<base64 image>"
  ]
}
```
