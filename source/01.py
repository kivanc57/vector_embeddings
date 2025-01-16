import csv
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
client = chromadb.PersistentClient(path='dbs')

sentence_transormer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='paraphrase-albert-small-v2')

collection = client.create_collection(name='my_collection', embedding_function=sentence_transormer_ef)

with open('./data/dishes.csv') as f:
  lines = csv.reader(f)

  documents = []
  metadatas = []
  ids = []
  id = 1

  for i, line in enumerate(lines):
    if i==0:
      continue
    
    documents.append(line[1])
    metadatas.append({'item_id': line[0]})
    ids.append(str(id))
    id+=1

# client.delete_collection('my_collection')

collection.add(
  documents=documents,
  metadatas=metadatas,
  ids=ids)

result = collection.query(
  query_texts=["salt n pepper"],
  n_results=2,
  include=['distances', 'metadatas', 'documents']
)

print(result)

