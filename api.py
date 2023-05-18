from flask import Flask, request, jsonify
from PIL import Image
import os
from AI.model_captioning import generate_caption_img
from AI.model_emotion import emotion_img
from AI.sen2word_similarity import similar
import fasttext
import datetime
from keras.models import load_model

#load model AI
emo_md = load_model('statics/model/Image_emotion/imageclassifier.h5')
ft_md = fasttext.load_model('statics/model/cc.vi.300.bin')

app = Flask(__name__)

# Input: request file image
# Output: caption of image, image link
@app.route('/caption', methods=['POST'])
def caption():
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400
    file = request.files['file']
    if not file:
        return jsonify({'error': 'invalid file'}), 400
    try:
        img = Image.open(file)
        if not os.path.exists('Statics/Images/uploads'):
            os.mkdir('Statics/Images/uploads')
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '-' + file.filename
        filelink = os.path.join('Statics/Images/uploads', filename)
        img.save(filelink)
        return generate_caption_img(filelink), filelink
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Input: request file image
# Output: sentiment of image, image link
@app.route('/emotion', methods=['POST'])
def emo():
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
        return emotion_img(filelink, emo_md), filelink
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Input: request.form text
# Output: similar score
@app.route('/similar', methods=['POST'])
def similar():
    text1 = request.form['text1']
    text2 = request.form['text2']
    return similar(text1, text2, ft_md)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port="8080")