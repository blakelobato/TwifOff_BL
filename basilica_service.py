import basilica

sentences = [
    "This is a sentence.",
    "This is a similar sentence!",
    "I dont think this sentence is very similar whatsoever...",
]

with basilica.Connection('7c4f4e09-9cab-ca9c-608a-de9ad17e46b9') as c:
    embeddings = list(c.embed_sentences(sentences))
    
    
    
print(embeddings) # [[0.8556405305862427, ...], ...]