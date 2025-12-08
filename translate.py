import google.generativeai as genai 

import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key='AIzaSyAZ0n0cMMTD6doseTnNyloigWRwH141yK4')

model = genai.GenerativeModel('gemini-2.5-flash')

def translate(text, target_language):
    prompt = f"Translate the following text to {target_language}. Only provide the translation, nothing else:\n\n{text}"
    # print(prompt, target_language)
    response = model.generate_content(prompt)
    # print(response)
    return response.text


if __name__ == "__main__":

    text = str(input("text: "))
    print(translate(text, "tj"))