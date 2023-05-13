# Recap app

## How to run:
```
git clone https://github.com/kienvs-pivasia/recaps.git
cd recaps/
pip install -r requirements.txt
mkdir statics
cd statics
mkdir Images
mkdir model
```

Paste file * *cc.vi.300.bin* * , * *Flickr8k.token.txt* * ; Folder * *Image_captioning* * , * *Image_emotion* * to * *statics/model* *

## AI API

AI API:

```
python api.py
```

Listen on : http://127.0.0.1:8080

## Database:
Using the database recorded in the file **run_db.py**

> Config username:password@host/db_name at backend/model.py

> Create_app just one time

> Create Database **db_name** in mariadb first
