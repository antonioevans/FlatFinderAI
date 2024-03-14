import requests
import time
import sys
from openai import OpenAI

session = requests.Session()
# Use session.post() instead of requests.post()


# Algolia configuration
algolia_app_id = '<algolia id>'
algolia_api_key = '<algolia key>'
algolia_index_name = '<algolia index_name>'

# OpenAI configuration
groq_api_key = "<LLM key>"

# Function to search Algolia
def algolia_search(query):
    url = f'https://{algolia_app_id}-dsn.algolia.net/1/indexes/{algolia_index_name}/query'
    headers = {
        'X-Algolia-API-Key': algolia_api_key,
        'X-Algolia-Application-Id': algolia_app_id,
        'Content-Type': 'application/json'
    }
    data = {"params": f"query={query}"}
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Algolia search execution time: {execution_time:.2f} seconds")
    return response.json()  # Assuming Algolia returns JSON response

# Function for non-streaming OpenAI interaction
def groq_interaction_refine(messages, temperature=0.5, tokens=1024):
    groq_endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {groq_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "messages": messages,
        "model": "gpt-3.5-turbo-0125",
        "temperature": float(.5),  # Ensure this is a float
        "max_tokens": int(4000)  # Ensure this is an integer
    }
    response = requests.post(groq_endpoint, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# Function for streaming OpenAI interaction
def groq_interaction_process_stream(messages, temperature=0.5, tokens=1024):
    client = OpenAI(api_key=groq_api_key)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        temperature=float(.5),  # Ensure this is a float
        max_tokens=int(4000),  # Ensure this is an integer
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

# Function to preprocess Algolia results
def preprocess_algolia_results(algolia_results):
    hits = algolia_results.get('hits', [])
    
    hits_data = []
    for hit in hits:
        hit_data =        f"Title: {hit.get('title', 'N/A')}\n" \
        f"Price: {hit.get('price', 'N/A')}\n" \
        f"Typology: {hit.get('typology', 'N/A')}\n" \
        f"Square Feet: {hit.get('sqft', 'N/A')}\n" \
        f"Bathrooms: {hit.get('baths', 'N/A')}\n" \
        f"Features: {', '.join(hit.get('features', []))}\n" \
        f"Location: {' > '.join(hit.get('breadcrumbs', []))}\n" \
        f"Energy Rating: {hit.get('energy efficiency rating:', 'N/A')}\n" \
        f"Address: {hit.get('address', 'N/A')}\n" \
        f"URL: {hit.get('url', 'N/A')}\n" \
        f"3D Tour: {hit.get('3dtour', 'N/A')}\n" \
         f"Advertiser Professional Name: {hit.get('advertiserProfessionalName', 'N/A')}\n" \
        f"Description: {hit.get('description', 'N/A')}\n" \
                     f"Listing URL: {hit.get('listingUrl', 'N/A')}\n" \
                    f"Photo 1: {hit.get('photos/0', 'N/A')}\n" \
                    f"Tag 1: {hit.get('tags/0', 'N/A')}\n" \
                    f"Video: {hit.get('video', 'N/A')}\n" \
                    f"Virtual Tour: {hit.get('virtualTour', 'N/A')}\n"
        hits_data.append(hit_data)
    
    hits_str = "\n\n".join(hits_data)
    
    return hits_str

# Main logic
if __name__ == "__main__":
    if len(sys.argv) > 1:
        initial_user_query = sys.argv[1]
    else:
        initial_user_query = input("Enter your query: ")

    # Refine the user query for Algolia
    refining_system_prompt = "You are a search query machine. you are helping take user queries and converting them to simple queries to query.. Your users are looking for information on apartments in Portugal. Your outputs should be similar to : T2 in <city> or t3 with a view in <neighborhood>. so all queries are plain text and should be a single statement. Provide Name, price, location, sizing.  These are rentals. never use colons, or quote.  your query should be at max 20 words.  examples: Input: Give me a 2 bedroom in Almada.  output: t2 almada  example:  input: Hey what are the prices for 1 beds in Setubal?  output: t1 setubal"
    refining_user_prompt = f"User query: {initial_user_query}\n is the user query.  Take it and convert it to a simple query. This is a plain text query. Only output simple queries, no extra text."
    refined_query = groq_interaction_refine([
        {"role": "system", "content": refining_system_prompt},
        {"role": "user", "content": refining_user_prompt}
    ])
    print(f"Refined query for Algolia: {refined_query}")

    # Query Algolia
    algolia_results = algolia_search(refined_query)
    algolia_results_str = preprocess_algolia_results(algolia_results)

    # Process Algolia results with streaming
    processing_system_prompt = "You are a realtor ai that convert idealista.pt results in an easy to understand language to answer a users query. you are helping take results from algolia and provide them for the users. You have the ability to provide external links Do not add your own additions comments. Your users are looking for information on apartments in Portugal.  Provide as much extra data about the apartments to make the interesting to the buyers. but try to put it as a sentences for human readable. Never make up a response. If no data say no data and suggest for them to refine their search.  exampe: input: Can I get a t1 in Almada?   output: of course you can! Now in Almada I have 2 great listings.  Remember your realtor AI so you trying to get people into apartments."
    processing_user_prompt = f"User query: {initial_user_query}\nAlgolia results:\nAnalyze the results of the query.  {algolia_results_str}\n <===now we need to come up with a response to the person's query.  If no results suggest for them to try something else, you can give suggestions.'."
    print("Processing Algolia results in real-time:")
    groq_interaction_process_stream([
        {"role": "system", "content": processing_system_prompt},
        {"role": "user", "content": processing_user_prompt}
    ])