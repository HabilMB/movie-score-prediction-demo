from flask import Flask, render_template, request
import tensorflow as tf

app = Flask(__name__)

model = tf.keras.models.load_model('saved_model_pycharm')

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/howtouse')
def howtouse():
    return render_template("howtouse.html")


@app.route('/predict',  methods=['GET'])
def predict():
    return render_template("main.html")

@app.route('/predict', methods=['POST'])
def prediction():
    user_input = request.form.to_dict()
    user_input['year'] = int(user_input['year'])

    converted = {name: tf.convert_to_tensor([value]) for name, value in user_input.items()}
    predict = model.predict(converted)
    final_pred = predict[0][0]
    verdict = ""
          
    if final_pred >= 9:
        verdict = "Amazing!"
    elif final_pred >= 8:
        verdict = "Great!"
    elif final_pred >= 7:
        verdict = "Good"
    elif final_pred >= 6:
        verdict = "Decent"
    elif final_pred >= 5:
        verdict = "Mediocre"
    elif final_pred >= 3:
        verdict = "Bad"
    elif final_pred < 3 :
        verdict = "Terrible"

    return render_template("prediction.html", prediction ="{:.1f}".format(final_pred), verdict = verdict)
    

if __name__ == '__main__':
    app.run(port=3000, debug=True)