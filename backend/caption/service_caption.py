from flask import Blueprint, jsonify, request
#from ..model import Tag, Favourite, Caption, CaptionTag, captions_schema, des_schema, emotion_schema, cap_list_schema, caption_tag_count_schema, caption_tag_schema
from PIL import Image
from AI.model_captioning import generate_caption_img
from AI.model_emotion import emotion_img
from AI.sen2word_similarity import sentence_embedding
import fasttext 
from flask_jwt_extended import jwt_required
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import func
from googletrans import Translator

def get_all_captions_service():
    from ..model import Caption, captions_schema
    all_captions = g.dbsession.query(Caption).filter(Caption.author_id == 1 or g.id).all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)

def get_caption_favorite_service():
    from ..model import captions_schema, Caption, Favourite
    favorite = g.dbsession.query(Caption).join(Favourite).filter(Caption.author_id == Favourite.user_id).all()
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
        g.dbsession.add(newCaption)
        g.dbsession.commit()
    return captions_schema.jsonify(newCaption)

def delete_caption_service(id):
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).first()
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        g.dbsession.delete(caption)
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

def get_des_service():
    from ..model import des_schema
    img_url = request.get('img_url')
    im = Image.open(request.get(img_url, stream=True).raw)
    im = im.convert('RGB')
    im.save('tmp.jpg')

    des = generate_caption_img('tmp.jpg')
    translator = Translator()
    des = translator.translate(des, dest="vi")
    return des_schema.jsonify(des)

def get_emotion_service():
    from ..model import emotion_schema
    img_url = request.get('img_url')
    im = Image.open(request.get(img_url, stream=True).raw)
    im = im.convert('RGB')
    im.save('tmp.jpg')

    emotion = emotion_img('tmp.jpg')
    return emotion_schema.jsonify(emotion)

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
    ft = fasttext.load_model('E:\do_an\recapnew\Model\word2vec\cc.vi.300.bin')
    vector_des = sentence_embedding(des, ft)
    captions = Caption.query.filter(Caption.author_id == 1).all()
    for caption in captions:
        dict = {"content":[], "similarity":[]}
        vector_cap = sentence_embedding(caption.content, ft)
        similarity = cosine_similarity([vector_des], [vector_cap])[0][0]
        similarity = round(similarity*100, 2)
        if 50 <= similarity <= 100:
            dict["content"].append(caption.content)
            dict["similarity"].append(similarity)
            list_cap.append(dict)
    return cap_list_schema.jsonify(list_cap)

def get_list_caption_login_service():
    from ..model import Caption, cap_list_schema
    img_url = request.get('img_url')
    im = Image.open(request.get(img_url, stream=True).raw)
    im = im.convert('RGB')
    im.save('tmp.jpg')

    des = generate_caption_img('tmp.jpg')
    list_cap = []
    ft = fasttext.load_model('E:\do_an\recapnew\Model\word2vec\cc.vi.300.bin')
    vector_des = sentence_embedding(des, ft)
    captions = Caption.query.filter(Caption.author_id == 1 and g.id).all()
    for caption in captions:
        dict = {"content":[], "similarity":[]}
        vector_cap = sentence_embedding(caption.content, ft)
        similarity = cosine_similarity([vector_des], [vector_cap])[0][0]
        similarity = round(similarity*100, 2)
        if 50 <= similarity <= 100:
            dict["content"].append(caption.content)
            dict["similarity"].append(similarity)
            list_cap.append(dict)
    return cap_list_schema.jsonify(list_cap)

def get_list_tag_service():
    from ..model import CaptionTag, caption_tag_count_schema
    tag_list = g.dbsession.query(CaptionTag).with_entities(CaptionTag.caption_id, CaptionTag.tag_id, CaptionTag.tag_name, func.count(1)).group_by(CaptionTag.tag_id).all()
    return caption_tag_count_schema(tag_list)

def get_tag_by_id_service():
    from ..model import CaptionTag, caption_tag_schema
    caption = g.dbsession.query(CaptionTag).join(Tag).filter(CaptionTag.caption_id == id).all()
    return caption_tag_schema.jsonify(caption)

def add_favorite_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).first()
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.favorite=True
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

def remove_favorite_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).fisrt()
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.favorite=False
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

def edit_content_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).fisrt()
    new_content = request.json['content']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.content=new_content
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

def edit_emotion_service():
    from ..model import Caption, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).fisrt()
    new_emotion = request.json['emotion']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    else:
        caption.content=new_emotion
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

def edit_tag_id_service():
    from ..model import Caption, CaptionTag, captions_schema
    msg = None
    caption = Caption.query.filter(Caption.id == id).fisrt()
    new_tag_id = request.json['tag_id']
    if caption.author_id != g.id:
        msg = "This caption is not belong to you"
        return msg
    caption_tag = CaptionTag.query.filter(CaptionTag.caption_id == id).fisrt()
    if new_tag_id == caption_tag.tag_id:
        msg = "Tag id is already exist"
        return msg
    else:
        caption_tag.tag_id=new_tag_id
        g.dbsession.commit()
    return captions_schema.jsonify(caption)

