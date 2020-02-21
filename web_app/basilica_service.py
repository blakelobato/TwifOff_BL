import basilica
import os
from dotenv import load_dotenv

load_dotenv()

BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

def basilica_connection():
    connection = basilica.Connection(BASILICA_API_KEY)
    print(connection)
    return connection

if __name__ == "__main__":

    sentences = ["This is a sentence.", "This is a similar sentence!", "I dont think this sentence is very similar whatsoever...",]

    connection = basilica_connection()

    embeddings = list(connection.embed_sentences(sentences))

    for emb in embeddings:
        print(type(emb))
        print(len(emb))
        print(emb)
        print("_________________________________________")

    result = connection.embed_sentence("Hello World, how are you?", model = "twitter")
    print(len(result))
    print(result)


#with basilica.Connection(BASILICA_API_KEY) as c:
 #   embeddings = list(c.embed_sentences(sentences))
    
    
    
#print(embeddings) # [[0.8556405305862427, ...], ...]

# connection = basilica.Connection(BASILICA_API_KEY)

# embeddings = list(connection.embed_sentences(sentences))

# for emb in embeddings:
#     print(type(emb))
#     print(emb)
#     print("-----------")
