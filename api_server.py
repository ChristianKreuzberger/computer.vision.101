import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np
import keras

from keras.applications import imagenet_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.regularizers import l2

from PIL import Image
from flask import Flask
from flask_restful import Api, Resource, reqparse
import werkzeug


input_shape = (28, 28, 1)
num_classes = 10


def build_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', kernel_regularizer=l2(0.01), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (5, 5), kernel_regularizer=l2(0.01)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.01)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (5, 5), kernel_regularizer=l2(0.01)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    return model


model = build_model()
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.load_weights("fashion-mnist-90.h5")
model._make_predict_function()

mapping = {
    0: "T-shirt/top", 
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot"
}


app = Flask(__name__)
api = Api(app)

@app.route('/')
def get_index():
    return """
    <html>
    <head>
    <title>Classify Image</title>
    </head>
    <body>
        <form method="post" action="/classify" enctype="multipart/form-data">
            File: <input type="file" name="image" /><br />
            <input type="submit">
        </form>
    </body>
    </html>
    """

@app.route('/classify', methods=['POST'])
def post_image():
    parse = reqparse.RequestParser()
    parse.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

    args = parse.parse_args()

    if not 'image' in args or not args['image']:
        return {
            'message': "Please provide an image"
        }, 400

    img_stream = args['image'].stream

    prepared_image = image.load_img(img_stream, target_size=(28, 28))
    # convert input image to gray scale
    prepared_image = prepared_image.convert('L')
    # convert the image to a numpy array
    prepared_image = image.img_to_array(prepared_image)
    prepared_image = np.expand_dims(prepared_image, axis=0)

    # and finally reshape the array
    prepared_image = prepared_image.reshape(1, 28, 28, 1)


    result = model.predict_classes(prepared_image)

    classification = result[0]

    import json

    return json.dumps({
        "classifications": result.tolist(),
        "string": mapping[classification]
    })



app.run(debug=True, host="0.0.0.0")

# Test with
# curl -F image=@`pwd`/fashion-mnist-handbag.png -X POST http://127.0.0.1:5000/classify
# # curl -F image=@`pwd`/fashion-mnist-shoe.png -X POST http://127.0.0.1:5000/classify
