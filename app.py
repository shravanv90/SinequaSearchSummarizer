import requests
import streamlit as st
import openai

# Define Sinequa REST API endpoint
SINEQUA_API_ENDPOINT = "<hostname>/api/v1/query"

# Define OpenAI API key and initialize the client
OPENAI_API_KEY = "<your-key>"
openai.api_key = OPENAI_API_KEY

def summarize(text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Summarize the following text:\n{text}"}
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    summary = response.choices[0].message['content'].strip()
    return summary

def generate_questions(text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Generate 5 questions based on the following text:\n{text}"}
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    questions = response.choices[0].message['content'].split('\n')  # Assuming questions are newline-separated
    return questions

# Streamlit layout and design enhancements
st.title("Sinequa Search Summarizer")
st.write("""
This tool uses GPT3.5 Turbo to provide concise summaries for your search results. 
Enter your search query below and get human-like summaries for each result.
""")

# Sidebar content
st.sidebar.header("Settings & Info")
st.sidebar.write("This tool uses GPT-3.5 Turbo from OpenAI to generate summaries.")

# Main content
query = st.text_input("Enter your search query:")
if st.button("Search"):
    # Prepare the payload for the POST request
    payload = {
        "app": "<app>",
        "user": "<user>",
        "password": "<passw>",
        "query": {
            "name": "<queryname>",
            "text": query
        }
    }

    # Query Sinequa enterprise search using REST API
    response = requests.post(SINEQUA_API_ENDPOINT, json=payload)
    response_data = response.json()

    # Check if 'records' key exists in the response
if 'records' in response_data:
    records = response_data["records"]
    
    # Display the results from the 'records' array
    for i, record in enumerate(records):
        st.subheader(f"**Result {i+1}**")
        st.write(f"**Title:** {record['title']}")
        
        # Summarize the relevant extracts directly using GPT-3.5 Turbo
        if 'relevantExtracts' in record:
            summary = summarize(record['relevantExtracts'])
            st.write(f"**Summary:** {summary}")

            # Generate questions based on the relevant extracts
            questions = generate_questions(record['relevantExtracts'])
            st.write("**Suggested Questions:**")
            for q in questions:
                st.write(f"- {q}")
        else:
            st.write("No relevant extracts found for this record.")
else:
    st.write("Error: The API response does not contain the 'records' key.")
    st.write("Full API Response:")
    st.json(response_data)  # Display the full API response in a formatted manner