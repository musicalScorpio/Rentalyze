"""

author : Sam Mukherjee

"""
import json
import openai
from dotenv import load_dotenv
import os
import openai
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os


load_dotenv('../env/relatize.env')
# Load the JSON data from a file
with open("../utils/prompts.json", "r") as file:
    data = json.load(file)

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI with the given prompt
# Function to call OpenAI with the given prompt
# Function to call OpenAI with the given prompt
def call_openai(prompt):
    # Initialize LangChain's ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    # Use LangChain's PromptTemplate and LLMChain to handle the prompt
    # Define the prompt template
    template = """
    You are a real estate expert with comprehensive knowledge of the market. Please provide the details of the 5 most recently sold properties within a 3-mile radius of {address}, sorted by date sold, sale price in descending order. For each property, include the following information in a table format: Address, Number of Bedrooms, Number of Bathrooms, Square Footage, Sale Price, Sale Date.
    """

    # Use LangChain's PromptTemplate and LLMChain to handle the prompt
    prompt = PromptTemplate(input_variables=["address"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Define the address
    address = "1915 Hailsham Court, Orlando, FL 32824"

    # Get the result from LangChain
    result = chain.run(address=address)

    # Print the result
    print(result)


# Function to get a prompt by reference_key
def get_prompt(reference_key, address):
    for prompt in data["prompts"]:
        if prompt["reference_key"] == reference_key:
            return prompt["prompt"].format(address)
    return None


# Example usage
reference_key="TREND_SEARCH_FOR_ADDRESS"
address = "1234 main street"
prompt = get_prompt(reference_key, address)
if prompt:
    result = call_openai(prompt)
    print(result)
else:
    print(f"Prompt with reference key '{reference_key}' not found.")

# Output:
# You are a real estate expert with comprehensive knowledge of the market. Please provide the details of the 5 most recently sold properties within a 3-mile radius of 1915 Hailsham Court, Orlando, FL 32824, sorted by sale price in descending order. For each property, include the following information in a table format: Address, Number of Bedrooms, Number of Bathrooms, Square Footage, Sale Price, Sale Date.
