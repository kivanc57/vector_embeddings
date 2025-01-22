import chromadb
from chromadb.utils import embedding_functions

def get_client(client_type=None, path=None):
  if client_type.lower() != 'persistent' and path == None:
    return chromadb.EphemeralClient()
  return chromadb.PersistentClient(path=path)

def get_embedding_function(model_name='paraphrase-albert-small-v2'):
  return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

def get_or_create_collection(client, name='my_collection', embedding_function=None, data_loader=None):
  return client.get_or_create_collection(
    name=name,
    embedding_function=embedding_function,
    data_loader=data_loader
  )

def main():
  client = get_client()
  embedding_function = get_embedding_function()
  get_or_create_collection(client=client, name='my_collection', embedding_function=embedding_function)
  print(f"Client's cursor is {client}")

if __name__ == '__main__':
  main()
