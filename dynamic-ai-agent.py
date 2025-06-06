from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def find_it_companies(location):
    # Construct the prompt for the OpenAI API
    prompt = f"""You are a very aware Business environment researcher in the United Kingdom. Please analyse the current business opportunities in IT opportunities that are locally based in the area named at {location} area in the United Kingdom. Please include currenct links to resources that you used for your analysis. Provide at least 1000 words of analysis.
    
    Output format:
    The format should be in a way that is compatible with Microsoft word Document or google docs.
    """
    
    # Call the OpenAI API using the new method
    response = openai.ChatCompletion.create(
        model="o4-mini",  # Use the latest OpenAI model
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