# from flask import Flask, render_template
from flask import Flask, url_for, render_template, request, flash, redirect

import keras_ocr
import matplotlib.pyplot as plt
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from wtforms import FileField, SubmitField 
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")


    
pipeline = keras_ocr.pipeline.Pipeline()

# Read images from folder path to image object
images = [
    keras_ocr.tools.read(img) for img in ['ss-1.jpg',
                                          'doc.png',
    ]
]

from PIL import Image
# create figure
fig = plt.figure(figsize=(20, 10))
  
# setting values to rows and column variables
rows = 1
columns =2
  
# reading images
Image1 = Image.open('doc.png')
Image2 = Image.open('ss-1.jpg')
  
# First Image
# fig.add_subplot(rows, columns, 1)
# plt.imshow(Image1)
# plt.axis('off')
# plt.title ("Handwritten Text")
  
# # Second Image
# fig.add_subplot(rows, columns, 2)
# plt.imshow(Image2)
# plt.axis('off')
# plt.title ("Image with Text")

# # generate text predictions from the images
# prediction_groups = pipeline.recognize(images)

# # plot the text predictions
# fig, axs = plt.subplots(ncols=len(images), figsize=(25, 15))
# for ax, image, predictions in zip(axs, images, prediction_groups):
#     keras_ocr.tools.drawAnnotations(image=image, 
#                                     predictions=predictions, 
#                                     ax=ax)

# predicted_image_1 = prediction_groups[0]
# for text, box in predicted_image_1:
#     print(text)


# predicted_image_2 = prediction_groups[1]
# for text, box in predicted_image_2:
#     print(text)
# ALLOWED_EXTENSIONS = set(['txt','jpg'])
@app.route("/", methods = ['GET' , 'POST'])
@app.route("/index", methods = ['GET' , 'POST'])
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html',methods=['GET','POST'])

@app.route('/upload')
def register():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "file uploaded"

    return render_template('upload.html', form = form,methods=['GET','POST'])

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig




if __name__ == '__main__':
    app.run(host='localhost', port=80)
    