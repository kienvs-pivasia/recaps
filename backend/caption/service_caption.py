from flask import Blueprint, jsonify, request, g
#from ..model import Tag, Favourite, Caption, CaptionTag, captions_schema, des_schema, emotion_schema, cap_list_schema, caption_tag_count_schema, caption_tag_schema
from PIL import Image
from AI.model_captioning import generate_caption_img
from AI.model_emotion import emotion_img
from AI.sen2word_similarity import sentence_embedding
import fasttext 
# from flask_jwt_extended import jwt_required
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import func
from googletrans import Translator
# import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

import fasttext
import datetime
from keras.models import load_model

#load model AI
emo_md = load_model('statics/model/Image_emotion/imageclassifier.h5')
ft_md = fasttext.load_model('statics/model/cc.vi.300.bin')

# Tạo đối tượng session
engine = create_engine("mariadb+mariadbconnector://root:12345678@127.0.0.1:3307/restapidb")
Session = sessionmaker(bind=engine)
session = Session()

def get_all_captions_admin_service():
    from ..model import Caption, captions_schema
    all_captions = session.query(Caption).filter(Caption.author_id == 1).all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)

def get_caption_favorite_service():
    from ..model import captions_schema, Caption, Favourite
    favorite = session.query(Caption).join(Favourite).filter(Caption.author_id == Favourite.user_id).all()
    return captions_schema.jsonify(favorite)

def add_caption_service():
    from ..model import Caption, captions_schema
    content = request.json["content"]
    emotion = request.json["emotion"]
    tag = request.json['tag']

    caption = Caption.query.filter(Caption.content == content).first()
    if caption:
        raise "Caption already exits"
    else:
        newCaption = Caption(
            content=content,
            emotion=emotion,
            tag=tag
        )
        session.add(newCaption)
        session.commit()
    return captions_schema.jsonify(newCaption)

def delete_caption_service(id):
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).first()
    if caption.author_id != id:
        msg = "This caption is not belong to you"
        return msg
    else:
        session.delete(caption)
        session.commit()
    return captions_schema.jsonify(caption)

def get_des_service():
    from ..model import des_schema
    import os
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400
    file = request.files['file']
    if not file:
        return jsonify({'error': 'invalid file'}), 400
    try:
        img = Image.open(file)
        if not os.path.exists('../statics/Images/uploads'):
            os.mkdir('../statics/Images/uploads')
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '-' + file.filename
        filelink = os.path.join('../statics/Images/uploads', filename)
        img.save(filelink)
        des = generate_caption_img(filelink)
        translator = Translator()
        des = translator.translate(des, dest="vi")
        return des_schema.jsonify(des)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_emotion_service():
    from ..model import emotion_schema
    import os
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400

    file = request.files['file']
    if not file:
        return jsonify({'error': 'invalid file'}), 400

    try:
        img = Image.open(file)
        # xử lý ảnh tại đây

        if not os.path.exists('Statics/Images/uploads'):
            os.mkdir('Statics/Images/uploads')

        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '-' + file.filename
        filelink = os.path.join('Statics/Images/uploads', filename)
        img.save(filelink)
        emotion = emotion_img(filelink, emo_md)
        return emotion_schema.jsonify(emotion)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_list_caption_no_login_service():
    from ..model import Caption, cap_list_schema
    img_url = request.get('img_url')
    im = Image.open(request.get(img_url, stream=True).raw)
    im = im.convert('RGB')
    im.save('tmp.jpg')

    des = generate_caption_img('tmp.jpg')
    translator = Translator()
    des = translator.translate(des, dest="vi")
    list_cap = []
    vector_des = sentence_embedding(des, ft_md)
    captions = Caption.query.filter(Caption.author_id == 1).all()
    for caption in captions:
        dict = {"content":[], "similarity":[]}
        vector_cap = sentence_embedding(caption.content, ft_md)
        similarity = cosine_similarity([vector_des], [vector_cap])[0][0]
        similarity = round(similarity*100, 2)
        if 50 <= similarity <= 100:
            dict["content"].append(caption.content)
            dict["similarity"].append(similarity)
            list_cap.append(dict)
    return cap_list_schema.jsonify(list_cap)

def get_list_caption_login_service():
    from ..model import Caption, cap_list_schema
    from ..model import des_schema
    import os
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400
    file = request.files['file']
    if not file:
        return jsonify({'error': 'invalid file'}), 400
    try:
        img = Image.open(file)
        if not os.path.exists('../statics/Images/uploads'):
            os.mkdir('../statics/Images/uploads')
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '-' + file.filename
        filelink = os.path.join('../statics/Images/uploads', filename)
        img.save(filelink)
        des = generate_caption_img(filelink)
        list_cap = []
        vector_des = sentence_embedding(des, ft_md)
        captions = Caption.query.filter(Caption.author_id == 1 and g.id).all()
        for caption in captions:
            dict = {"content":[], "similarity":[]}
            vector_cap = sentence_embedding(caption.content, ft_md)
            similarity = cosine_similarity([vector_des], [vector_cap])[0][0]
            similarity = round(similarity*100, 2)
            if 50 <= similarity <= 100:
                dict["content"].append(caption.content)
                dict["similarity"].append(similarity)
                list_cap.append(dict)
        return cap_list_schema.jsonify(list_cap)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_list_tag_service():
    from ..model import caption_tag, caption_tag_count_schema
    tag_list = session.query(caption_tag).with_entities(caption_tag.caption_id, caption_tag.tag_id, caption_tag.tag_name, func.count(1)).group_by(caption_tag.tag_id).all()
    return caption_tag_count_schema(tag_list)

def get_tag_by_id_service():
    from ..model import Tag
    from ..model import CaptionTag, caption_tag_schema
    caption = session.query(CaptionTag).join(Tag).filter(CaptionTag.caption_id == g.id).all()
    return caption_tag_schema.jsonify(caption)

def add_favorite_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == g.id).first()
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.favorite=True
        session.commit()
    return captions_schema.jsonify(caption)

def remove_favorite_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == g.id).fisrt()
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.favorite=False
        session.commit()
    return captions_schema.jsonify(caption)

def edit_content_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == g.id).fisrt()
    new_content = request.json['content']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.content=new_content
        session.commit()
    return captions_schema.jsonify(caption)

def edit_emotion_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == g.id).fisrt()
    new_emotion = request.json['emotion']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.content=new_emotion
        session.commit()
    return captions_schema.jsonify(caption)

def edit_tag_id_service():
    from ..model import Caption, CaptionTag, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == g.id).fisrt()
    new_tag_id = request.json['tag_id']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    caption_tag = CaptionTag.query.filter(CaptionTag.caption_id == g.id).fisrt()
    if new_tag_id == caption_tag.tag_id:
        msg = "Tag id is already exist"
        return msg
    else:
        caption_tag.tag_id=new_tag_id
        session.commit()
    return captions_schema.jsonify(caption)

