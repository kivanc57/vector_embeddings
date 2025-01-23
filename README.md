# 🎯 Vector Embedding & CRUD Operations with ChromaDB and Gemini AI

## 📌 Overview

This project integrates **ChromaDB**, **Google Gemini AI**, and **YouTube Transcript API** to handle **vector embeddings, text processing, and CRUD operations**. It supports **semantic search, text embeddings, and AI-generated keynotes** from video transcripts.

## 🚀 Features

- **ChromaDB integration** for vector storage
- **Google Gemini AI** for text embeddings and summarization
- **YouTube Transcript API** to fetch video transcripts
- **CRUD operations** (Create, Read, Update, Delete) on embeddings
- **Persistent and ephemeral database modes** using `chromadb`
- **File handling** for storing transcripts and notes

## 🛠️ Setup & Installation

### **1️⃣ Install Dependencies**

Ensure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### **2️⃣ Set Up Environment Variables**

Create a `.env` file with:

```sh
GOOGLE_API_KEY=your_gemini_api_key
```

### **3️⃣ Run the Project**

```sh
python main.py
```

---

## 📝 Key Functionalities

### **🔹 ChromaDB Client**

Defined in `utils.py`, the `get_client()` function initializes a ChromaDB client:

```python
def get_client(client_type=None, path=None):
    if client_type.lower() != 'persistent' and path is None:
        return chromadb.EphemeralClient()
    return chromadb.PersistentClient(path=path)
```

- **Persistent Mode:** Saves embeddings for future retrieval.
- **Ephemeral Mode:** Stores data only for the current session.

### **🔹 Creating & Managing Collections**

Collections store vector embeddings and text data.

```python
def get_or_create_collection(client, name='my_collection', embedding_function=None, data_loader=None):
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_function,
        data_loader=data_loader
    )
```

### **🔹 Generating AI-Based Keynotes**

Extracts keynotes from a transcript using Gemini AI:

```python
response = genai_model.generate_content(prompt + transcript, stream=False)
with open(notes_path, "w") as file:
    file.write(response.text)
```

---

## 📌 Usage Guide

### **1️⃣ Fetch and Store Video Transcripts**

```python
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
formatted_transcript = TextFormatter().format_transcript(transcript)
```

### **2️⃣ Generate and Store Keynotes**

```python
response = genai_model.generate_content("Extract keynotes: " + transcript)
collection.upsert(ids=[video_id], documents=[response.text])
```

### **3️⃣ Perform CRUD Operations**

- **Insert data:** `collection.upsert()`
- **Retrieve data:** `collection.get()`
- **Update existing data:** `collection.update()`
- **Delete data:** `collection.delete()`

---

## 🔗 Additional Information

- **ChromaDB Docs:** [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)
- **Google Gemini AI:** [https://ai.google.dev/](https://ai.google.dev/)
- **YouTube Transcript API:** [https://pypi.org/project/youtube-transcript-api/](https://pypi.org/project/youtube-transcript-api/)

---

## 💡 Future Enhancements

- Support for **multilingual embeddings**
- Integration with **speech-to-text models**
- Implementing **batch processing** for large video datasets

### **👨‍💻 Author**

Maintained by **@kivanc57**\
Feel free to contribute or suggest improvements! 🚀
