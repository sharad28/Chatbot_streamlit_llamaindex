# Following are the follow to create a chatbot with your document:
## SimpleDirectoryReader : 
    - SimpleDirectoryReader is the simplest way to load data from local files into LlamaIndex
    There are many readers are available in LlamaHub for for """ production use case"""
    -- https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/
## Embeddings:
- Embeddings are used in LlamaIndex to represent your documents using a sophisticated numerical representation. Embedding models take text as input, and return a long list of numbers used to capture the semantics of the text. These embedding models have been trained to represent text this way, and help enable many applications, including search!
   - At a high level, if a user asks a question about dogs, then the embedding for that question will be highly similar to text that talks about dogs.
    - When calculating the similarity between embeddings, there are many methods to use (dot product, cosine similarity, etc.). By default, LlamaIndex uses cosine similarity when comparing embeddings.
    - There are many embedding models to pick from. By default, LlamaIndex uses text-embedding-ada-002 from OpenAI. We also support any embedding model offered by Langchain here, as well as providing an easy to extend base class for implementing your own embeddings.

    ```python
    index = VectorStoreIndex(docs,show_progress=True)
    ```
    *By default, VectorStoreIndex stores everything in memory.*
    

Reference:
https://docs.llamaindex.ai/