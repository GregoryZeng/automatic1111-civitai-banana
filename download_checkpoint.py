import os
import requests
import sys
import time
import re
from tqdm import tqdm

MODEL_URL = os.environ.get('MODEL_URL')
HF_TOKEN = os.environ.get('HF_TOKEN', '')

CHUNK_SIZE = 1024 * 1024

def get_filename(model_url, id="model"):
    if '.safetensors' in model_url:
        return 'models/Stable-diffusion/' + id + '.safetensors'
    elif '.ckpt' in model_url:
        return 'models/Stable-diffusion/' + id + '.ckpt'
    elif 'civitai.com' in model_url:
        # accepts url like `https://civitai.com/api/download/models/29460`
        response = requests.get(model_url, stream=True)
        fileformat = re.search('filename="(.+)"', response.headers['Content-Disposition']).group(1).split('.')[-1]
        response.close()
        return 'models/Stable-diffusion/' + id + '.' + fileformat
    else:
        raise Exception("model_url must be a .safetensors/.ckpt file or from civitai")

def check_model_file(filename):
    file_size_mb = round(os.path.getsize(filename) / (1024 * 1024))
    if file_size_mb < 100:
        print(f'The downloaded file is only {file_size_mb} MB and does not appear to be a valid model.')
        sys.exit(1)

def download_hf_file(model_url, HF_TOKEN, id="model"):
    filename = get_filename(model_url, id)
    if os.path.exists(filename):
        return
    print("Model URL:", model_url)
    print("Download Location:", filename)
    if not HF_TOKEN:
        print("A Huggingface token was not provided.")
    else:
        print("Using Huggingface authentication token.")
    headers = {'Authorization': f'Bearer {HF_TOKEN}'}
    response = requests.get(model_url, headers=headers, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f, tqdm(desc="Downloading", unit="bytes", total=int(response.headers.get('content-length', 0))) as progress:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                progress.update(len(chunk))
    check_model_file(filename)

def download_other_file(model_url, id="model"):
    filename = get_filename(model_url, id)
    if os.path.exists(filename):
        return
    print("Model URL:", model_url)
    print("Download Location:", filename)
    response = requests.get(model_url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f, tqdm(desc="Downloading", unit="bytes", total=int(response.headers.get('content-length', 0))) as progress:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                progress.update(len(chunk))
    check_model_file(filename)

def download(url, id="model"):
    if 'huggingface.co' in url:
        if '/blob/' in url:
            url = url.replace('/blob/', '/resolve/')
        download_hf_file(url, HF_TOKEN, id)
    else:
        download_other_file(url, id)

if __name__ == '__main__':
    download(MODEL_URL)