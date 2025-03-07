#Importing all the necessory library

import streamlit as st
import pandas as pd
import PyPDF2
import os
from together import Together
from dotenv import load_dotenv

#loading environment 
load_dotenv()
TOGETHER_API_KEY = os.getenv("API_KEY") #Create Own API key from Together AI 

# Defining AI model details
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K" #model used for data extraction
SAFETY_MODEL = "meta-llama/Meta-Llama-Guard-3-8B" #model used for safety filtering
MAX_TOKENS_FOR_CONTENT = 4000 # Maximum token limit per text segment

# Initialize Together AI client
client = Together(api_key=TOGETHER_API_KEY)

def extract_pdf_content(file):
    """Extracts text from all pages of an uploaded PDF."""
    pdf_reader = PyPDF2.PdfReader(file)
    content = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            content += text + "\n"
    return content.strip()

def segment_text_with_table_detection(text, max_tokens, overlap_ratio=0.3):
    """Segments text into manageable chunks while ensuring that tables are not split."""
    table_keywords = ["Module Number", "Course Title", "ECTS", "Duration", "Assessment", "Workload", "Professor Name/Module Manager"]
    words = text.split()
    segments = []
    step = int(max_tokens * (1 - overlap_ratio))
    inside_table = False
    current_segment = []
    current_token_count = 0

    for word in words:
        if any(keyword in word for keyword in table_keywords):
            inside_table = True  # Detect table start
        elif inside_table and word.strip() == "":
            inside_table = False  # Detect table end

        if current_token_count + len(word.split()) <= max_tokens or inside_table:
            current_segment.append(word)
            current_token_count += len(word.split())
        else:
            segments.append(" ".join(current_segment))
            current_segment = [word]
            current_token_count = len(word.split())

    if current_segment:
        segments.append(" ".join(current_segment))

    return segments

def extract_tables_from_text(text):
    """Uses Together AI to extract structured tables from text."""
    messages = [
            {"role": "system", "content": "You are an AI assistant that extracts structured tables from unstructured text. Your task is to detect and reconstruct tables even when they are not clearly formatted."},
            {"role": "user", "content": f"""
            Extract **all tables** from the following text. Some tables span multiple pages, while others fit on a single page. You must detect **both** types.

            **How to Identify Tables in This Text:**
            - A table **contains structured information**, often using columns like **Module Number, Course Title, ECTS, Duration, Professor name**.
            - A table **may not have a clear separator** (like `|`), but it follows a pattern: **columns are grouped together** and followed by structured data.
            - If a list contains **numbers, credits, or structured course details**, assume it is a table.

            **Instructions:**
            - Identify **all tables**, even those that appear in a single-page or span multiple pages.
            - If a table is **not formatted properly**, reconstruct it into a structured table.
            - Ensure **no tables are skipped**.

            **Extracted Text:**
            {segment}

            **Output Format:**
            ```
            Table 1:
            | Column1 | Column2 | Column3 | ...
            | --- | --- | --- | ...
            | Data 1  | Data 2 | Data 3 | ...

            Table 2:
            | Column1 | Column2 | Column3 | ...
            | --- | --- | --- | ...
            ```
            """}
    ]
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=4048,
        temperature=0.0,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        safety_model=SAFETY_MODEL
    )
    
    return response.choices[0].message.content.strip()

def parse_extracted_data(metadata_text):
    """Converts tabular text to a DataFrame and ensures unique column names."""
    rows = [line.split("|") for line in metadata_text.split("\n") if "|" in line]
    
    if rows:
        headers = [col.strip() for col in rows[0]]  # Extract header row
        data_rows = rows[1:]  # Extract data rows

        # Ensure unique column names
        seen = {}
        for i, col in enumerate(headers):
            if col in seen:
                seen[col] += 1
                headers[i] = f"{col}_{seen[col]}"  # Append a suffix for duplicates
            else:
                seen[col] = 0

        max_cols = len(headers)
        cleaned_data_rows = [row[:max_cols] if len(row) >= max_cols else row + [""] * (max_cols - len(row)) for row in data_rows]
        
        df = pd.DataFrame(cleaned_data_rows, columns=headers)
        return df
    
    return pd.DataFrame()


# Streamlit UI
st.title("📄 Extract Metadata From Handbook")
st.write("Upload a PDF file to extract structured table data.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.write("Extracting text from PDF...")
    pdf_text = extract_pdf_content(uploaded_file)
    
    st.write("Segmenting text to fit AI model constraints...")
    segments = segment_text_with_table_detection(pdf_text, MAX_TOKENS_FOR_CONTENT)
    
    extracted_tables = []
    for segment in segments:
        st.write("Processing text segment...")
        metadata_text = extract_tables_from_text(segment)
        df = parse_extracted_data(metadata_text)
        if not df.empty:
            extracted_tables.append(df)
    
    if extracted_tables:
        final_df = pd.concat(extracted_tables, ignore_index=True)
        st.write("### Extracted Tables:")
        st.dataframe(final_df)
        
        # Provide CSV download option
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Extracted Data as CSV",
            data=csv,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
    else:
        st.write("No structured tables were detected in the document.")