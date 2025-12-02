# Build a CLI Q&A; chatbot ask one question, get one answer
# step 1:import libraries
# step 2: get the key from .env file
# step 3: configure the api key
# step 4: create a model object 
# step 5: get user input with while loop
# step 6: generate response from the model object
import os
import google.generativeai as genai
from dotenv import load_dotenv  

load_dotenv()  # load the .env file
genai.configure(api_key=os.getenv("Gemini_api"))  # configure the api key
model=genai.GenerativeModel("gemini-2.5-pro")  # create a model object
print(" i you want to exit, type 'exit' or 'quit'")
while True:
    user_input=input("You: enter your prompt :") 

     # get user input
    if user_input.lower() in ['exit', 'quit'] :
        print("Exiting the chatbot. Goodbye!")
        break
    if user_input.strip() == "":
        print("Please enter a valid prompt. or type 'exit' to quit.")
        continue
    try:
    response=model.generate_content(user_input) 
    except Exception as e:
        print(f"An error occurred: {e}")
        

  
    