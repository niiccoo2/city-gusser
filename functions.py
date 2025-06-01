from openai import OpenAI
import os
from main import *
from api import *

def get_summary(city):
    client = OpenAI(api_key=get_openai_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Write a one paragraph summary of {city}. It is for a city gussing game so you can't give away the city is. Maybe some fun facts. Do not give any locations."},
        ],
        temperature=0,
    )

    return response.choices[0].message.content