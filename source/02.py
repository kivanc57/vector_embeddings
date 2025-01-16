from matplotlib import pyplot as plt
import chromadb
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions.open_clip_embedding_function import OpenCLIPEmbeddingFunction

client = chromadb.PersistentClient(path='dbs')
image_loader = ImageLoader()
multimodal_ef = OpenCLIPEmbeddingFunction()


db = client.get_or_create_collection(
  name='my_collection',
  embedding_function=multimodal_ef,
  data_loader=image_loader)

# print(db.count())

# db.add(
#   ids=['0', '1'],
#   uris=['./data/lion.jpg', './data/tiger.jpg'],
#   metadatas=[{'image_category': 'animals'}, {'image_category': 'animals'}]
# )

def print_query_results(query_list, query_results):
  result_count = len(query_results['ids'][0])

  for i in range(len(query_list)):
    print(f'Results for query: {query_list[i]}')

    for j in range(result_count):
      id       = query_results["ids"][i][j]
      distance = query_results['distances'][i][j]
      data     = query_results['data'][i][j]
      document = query_results['documents'][i][j]
      metadata = query_results['metadatas'][i][j]
      uri      = query_results['uris'][i][j]
      print(f'id: {id}, distance: {distance}, metadata: {metadata}, document: {document}') 
      print(f'data: {uri}')
      plt.imshow(data)
      plt.axis("off")
      plt.show()

# query_texts = ['lion']
# query_results = db.query(
#   query_texts=query_texts,
#   n_results=10,
#   include=['documents', 'distances', 'metadatas', 'data', 'uris'],
#   where={'image_category': 'animals'}
# )

# print_query_results(query_texts, query_results)



ids=[
  'A01-01',
  'A01-02',
  'A02-01'
]

uris=[
  f'./data/{ids[0]}.jpg',
  f'./data/{ids[1]}.jpg',
  f'./data/{ids[2]}.jpg'
]

metadatas=[
  {'item_id': ids[0], 'image_category':'food', 'item_name': 'Bean Dish'},
  {'item_id': ids[1], 'image_category':'food', 'item_name': 'Broccoli Dish'},
  {'item_id': ids[2], 'image_category':'food', 'item_name': 'Meat Dish'}
]

db.update(ids=ids, uris=uris, metadatas=metadatas)


query_texts = ['broccoli']
query_results = db.query(
  query_texts=query_texts,
  n_results=5,
  include=['documents', 'distances', 'metadatas', 'data', 'uris'],
  where={'image_category': {'$ne':'food'}}
)

print_query_results(query_texts, query_results)