# Telegram Voice Cloner Bot

Team project. More info will be added.

## Installation
1) Install Python 3.7.x
2) Install Pytorch:
```
pip3 install torch==1.8.2+cpu torchvision==0.9.2+cpu torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
```
3) Run ```pip install -r requirements.txt``` to install the necessary packages.
4) Install ```ffmpeg```.
5) Download archive with pretrained models for voice cloning from [here](https://drive.google.com/uc?id=1aQBmpflbX_ePUdXTSNE4CfEL9hdG2-O8)
and unpack them into models.
6) Download pretrained model for language classification from [here](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz)
and unpack it to ```model/lang_classification/saved_models/lid.176.ftz```.

## Usage
Command to start for Linux/MacOS:
```
export API_TOKEN="TOKEN" && python main.py
```
Command to start for Windows Powershell:
```
$env:API_TOKEN = "TOKEN"
python .\main.py
```
