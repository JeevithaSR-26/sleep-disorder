from flask import Flask, render_template, request
import pandas as pd
import joblib
from predict import predict_sleep_disorder

app = Flask(__name__)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        data = {
            'Gender': [request.form['gender']],
            'Age': [int(request.form['age'])],
            'Occupation': [request.form['occupation']],
            'Sleep Duration': [float(request.form['sleep_duration'])],
            'Quality of Sleep': [int(request.form['quality_of_sleep'])],
            'Physical Activity Level': [int(request.form['physical_activity_level'])],
            'Stress Level': [int(request.form['stress_level'])],
            'BMI Category': [request.form['bmi_category']],
            'Heart Rate': [int(request.form['heart_rate'])],
            'Daily Steps': [int(request.form['daily_steps'])],
            'Blood Pressure': [request.form['blood_pressure']]
        }

        input_df = pd.DataFrame(data)
        input_df = input_df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
        prediction = predict_sleep_disorder(input_df)
        prediction_label = prediction[0]
        def get_suggestion(pred):
            if pred == "Insomnia":
                return "Maintain a regular sleep schedule, avoid mobile before bed."

            elif pred == "Sleep Apnea":
                return "Consult a doctor, avoid sleeping on your back."

            elif pred == "No Disorder":
                return "You are healthy. Keep maintaining good sleep habits."

            else:
                return "Take care of your sleep and health."
        suggestion = get_suggestion(prediction_label)

        return render_template('result.html', prediction=prediction_label,suggestion=suggestion)


if __name__ == '__main__':
    app.run(debug=True)
