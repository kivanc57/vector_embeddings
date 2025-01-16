import os
import chromadb
from pathlib import Path
import google.generativeai as genai
from chromadb.utils import embedding_functions
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

client = chromadb.PersistentClient(path='dbs')

genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel('gemini-1.5-flash')
gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GOOGLE_API_KEY)

collection = client.get_or_create_collection(name='youtube_notes', embedding_function=gemini_ef)



# CREATE A FUNCTION TO GET THE ID

# uris = [
#   "https://www.youtube.com/watch?v=wRmOOWPTRBs",
#   "https://www.youtube.com/watch?v=7EMa8hMHcXI",
#   "https://www.youtube.com/watch?v=xWhfs1MYNfc",
#   "https://www.youtube.com/watch?v=BrQLpAGlvko",
#   "https://www.youtube.com/watch?v=ht_PoCwpUFQ",
#   "https://www.youtube.com/watch?v=9x1y392RBfc",
#   "https://www.youtube.com/watch?v=jR3TZv_2jJg",
#   "https://www.youtube.com/watch?v=0e4xgZkLuNg"
# ]

video_uri = "https://www.youtube.com/watch?v=0e4xgZkLuNg"
video_id = "0e4xgZkLuNg"

# transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['en', 'en-US', 'en-GB'])
# transcript = TextFormatter().format_transcript(transcript)


# UTILS
def join_paths(*args):
  return os.path.join(*args)


# ADD THESE AS PARAMETERS TO FUNCTIONS!!!!!
# video_name = video_id
# transcript_name = 'transcript.txt'
# notes_name = 'notes.txt'
output_folder_name = 'output'


# CREATE VIDEO FOLDER
# video_folder_path = join_paths(output_folder_name, video_name)
# Path(video_folder_path).mkdir(parents=True, exist_ok=True)


# GET PATH
# transcript_path = join_paths(video_folder_path, transcript_name)
# notes_path = join_paths(video_folder_path, notes_name)


# WRITE TRANSCRIPT
# with open(transcript_path, "w") as file:
#   file.write(transcript)



# prompt = "Extract key notes from video transcript: "
# response = genai_model.generate_content(prompt + transcript, stream=False)

# WRITE NOTES
# with open(notes_path, "w") as file:
#   file.write(response.text)


# UPSERT (UPDATE IF EXISTS, INSERT IF NOT) ALL NOTES TO DB
# for dirpath, dirname, filenames in os.walk(output_folder_name):
#   for filename in filenames:
#     if filename.endswith('.txt'):
#       file_path = join_paths(dirpath, filename)
#       with open(file_path, 'r') as file:
#         content = file.read()
#         collection.upsert(ids=[video_id], documents=[content], uris=[video_uri])


# QUERY THE RESULTS
query_text = "What practicing boxing changes?"
n_results = 3

query_results = collection.query(
  query_texts=[query_text],
  n_results=n_results,
  include=['distances', 'documents', 'uris']
)

# PRINT THE RESULTS
# for i in range(len(query_results['ids'][0])):
#   id       = query_results["ids"][0][i]
#   uri      = query_results["uris"][0][i]     
#   document = query_results["documents"][0][i]

#   print("************************************************************************")
#   print(f"Video ID: {i+1}")
#   print(f"Video URI: {uri}")
#   print("************************************************************************")
#   print(document, "\n")


prompt = "Answer the following QUESTION using DOCUMENT as context."
prompt += f"QUESTION: {query_text}"
prompt += f"DOCUMENT: {query_results["documents"][0][0]}"

response = genai_model.generate_content(prompt, stream=False)
print(response.text)