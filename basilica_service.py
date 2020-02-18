import basilica
import os
from dotenv import load_dotenv

load_dotenv()

BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")


sentences = [
    "This is a sentence.",
    "This is a similar sentence!",
    "I dont think this sentence is very similar whatsoever...",
]

with basilica.Connection(BASILICA_API_KEY) as c:
    embeddings = list(c.embed_sentences(sentences))
    
    
    
print(embeddings) # [[0.8556405305862427, ...], ...]

# connection = basilica.Connection(BASILICA_API_KEY)

# embeddings = list(connection.embed_sentences(sentences))

# for emb in embeddings:
#     print(type(emb))
#     print(emb)
#     print("-----------")
