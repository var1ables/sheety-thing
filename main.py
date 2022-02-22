from datetime import datetime
import requests
import os

GENDER = 'male'
WEIGHT = 180
HEIGHT = 178
AGE = 30

APP_ID = os.environ["YOUR_APP_ID"]
API_KEY = os.environ["YOUR_API_KEY"]

exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercis'
sheet_endpoint = 'https://api.sheety.co/8a9268e45d797f17e12931991a01e405/copyOfMyWorkouts/workouts'

exercise_text = input('What exercises did you do?')

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

parameters = {
    'query': exercise_text,
    'gender': GENDER,
    'weight': WEIGHT,
    'height': HEIGHT,
    'age': AGE
}


response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime('%d/%m/%Y')
now_time = datetime.now().strftime('%X')

for exercise in result['exercises']:
    sheet_inputs = {
        'workout': {
            'date': today_date,
            'time': now_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    # No Auth
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

    # Basic Auth
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["USERNAME"],
            os.environ["PASSWORD"],
        )
    )

    # Bearer Token
    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(sheet_response.text)