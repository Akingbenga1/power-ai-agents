from dotenv import load_dotenv
import openai
import os
import requests  # Import requests to make web calls

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def find_it_companies(location):
    # Construct the prompt for the OpenAI API
    prompt = f"List all IT companies including the website and contact details and postcode in the {location} area in the United Kingdom."
    
    # Call the OpenAI API using the new method
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response text
    companies_list = response['choices'][0]['message']['content']
    return companies_list

if __name__ == "__main__":
    location = input("Please enter the location (e.g., Cambridgeshire): ")
    it_companies = find_it_companies(location)
    print(it_companies)