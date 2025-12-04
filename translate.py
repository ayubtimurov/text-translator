import google.generativeai as genai 

genai.configure(api_key="AIzaSyDx4mgRiKvDy7LBxNGMHxEebS-jIIBEpGA")

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