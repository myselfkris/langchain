import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Gemini_api"))

model = genai.GenerativeModel("gemini-2.5-pro")
response = model.generate_content("Hello Gemini, test connection!")
print(response.text)

