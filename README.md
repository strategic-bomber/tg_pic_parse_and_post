# Parser-poster script
## Description
This script is created for auto parsing pictures from public telegram channels and posting
## Download
1. Clone repository
```sh
   git clone https://github.com/strategic-bomber/tg_pic_parse_and_post.git
```
2. Download requirements
``` 
pip install -r requirements.txt
```
3. Edit configs.py
4. Create session file
``` 
python generate_session.py
```
5. Copy pictures from any telegram channel
```
python listener.py
```
6. Posting pictures
``` python post_photos.py
```

P.S: pictures will be post every 3 hours, but you can change it in 64`s line