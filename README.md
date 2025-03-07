# 🚀 Extract Metadata from Long PDFs Using LLMs  

![Metadata Extraction](https://img.shields.io/badge/Metadata%20Extraction-LLM%20%7C%20PyMuPDF-brightgreen)  
📄 **AI-powered extraction of structured metadata from academic handbooks using Large Language Models (LLMs) and PyPDF2.**  

---

## 🌟 Overview  

Academic module handbooks contain critical course-related metadata, such as **course names, faculty details, credits, and assessment methods**. However, extracting structured data from these PDFs is challenging due to their **varying formats** and **lack of standardization** across universities.  

🔍 **This project automates metadata extraction from these documents by leveraging:**  
- **🧠 Large Language Models (Meta-Llama-3.1-8B)** to intelligently extract structured metadata from long PDFs.  
- **📄 PyPDF2** for efficient PDF parsing and text segmentation.  
- **🛠 Content-aware segmentation** to process long documents while preserving table structures.  
- **⚡ Streamlit-based UI** for uploading PDFs and exporting extracted metadata in structured formats.  

💡 **Key Benefits:**  
✅ **Scalable** – Handles large academic PDFs efficiently.  
✅ **Accurate** – Extracts structured metadata, preserving document hierarchy.  
✅ **User-Friendly** – Provides a simple UI for document upload & data export.  
✅ **Optimized for Long Documents** – Uses token-aware segmentation to process large handbooks.  

---

## 📂 Project Structure  


---

## 🚀 Core Features  

✅ **Automated metadata extraction** from academic handbooks.  
✅ **Processes long and complex PDFs** while preserving structured information.  
✅ **Uses LLMs (Meta-Llama-3.1-8B)** to extract course-related metadata.  
✅ **Token-aware segmentation** to efficiently handle large documents.  
✅ **Outputs in structured formats** (Markdown, CSV).  
✅ **Interactive UI** using Streamlit for easy document processing.  

---

## 🔥 Key Components  

### 🏆 `app.py` (Main File)  
- **Implements LLama Model (Meta-Llama-3.1-8B) for metadata extraction.**  
- Processes **long academic PDFs**, extracts structured metadata.  
- **Handles text segmentation, table reconstruction, and structured output generation.**  

### 🧪 `llama_with_pymupdf4llm.ipynb` (Testing LLM for PDFs)  
- **Experimental Notebook** for testing **LLM-based** PDF processing.  
- Uses **PyMuPDF4LLM** for extracting metadata from PDFs.  

### 📚 `english_handbook_pdf/`  
- **Contains 10 PDFs** from **top German universities**.  
- Used for **testing and benchmarking metadata extraction**.  

### 📑 `output.md` (Sample Output)  
- A **Markdown file** showing extracted metadata using PyMuPDF4LLM.  

---

## 🛠 Methodology  

This project follows an **AI-driven metadata extraction pipeline**:

1️⃣ **Text Extraction (PyPDF2)**  
   - Extracts **raw text** while preserving document layout.  

2️⃣ **Content-Aware Segmentation**  
   - Splits extracted text into **manageable chunks** for LLM processing.  
   - Uses **token-aware segmentation** (max 4000 tokens per chunk).  

3️⃣ **Metadata Extraction Using LLMs (Meta-Llama-3.1-8B)**  
   - Uses **instruction-based prompts** to identify key metadata fields:  
     - **Course Title**  
     - **Module Number**  
     - **ECTS Credits**  
     - **Assessment Methods**  
     - **Faculty Names**  

4️⃣ **Post-Processing & Data Structuring**  
   - Converts extracted text into structured **tables** (Pandas DataFrame).  
   - Ensures **clean, organized metadata** before export.  

5️⃣ **User Interface & Data Export (Streamlit UI)**  
   - Users **upload PDFs** → Extracted metadata is displayed in a **structured table**.  
   - Supports **CSV export** for easy integration into academic databases.  

---

## 🛠 Installation & Usage  

### 1️⃣ Clone the Repository  

```sh
git clone https://github.com/keertisuryawanshids/Extract_Metadata_From_Handbook.git
cd Extract_Metadata_From_Long_PDF
