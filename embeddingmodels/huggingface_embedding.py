from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(

    model_name = "sentence-transformers/all-MiniLM-L6-v2"

)

text = [

  "Hello this is Prerana ",
  "Hello my nae is Youtube",
  "And you all are very beautiful"

]

vector = embeddings.embed_documents(text)


print(vector)