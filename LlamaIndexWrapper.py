import openai
import  os
from dotenv import  load_dotenv

from Config import Config
import pandas as pd
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core.indices import VectorStoreIndex

from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import LLMRerank

load_dotenv()

Config.open_api_key = os.environ["OpenAI_API_Key"]

openai.api_key = Config.open_api_key

class LlamaIndexWrapper:

    def __init__(self):
        print("Creating new object of LlamaIndexWrapper")
        self.index = None
        self.fashion_df = None

    def setup_llamaindex_settings(self):
        #### Configuring embedding model to be used by LlamaIndex
        embedding_model = OpenAIEmbedding(model=Config.embedding_model)
        Settings.embed_model = embedding_model

        #### Configuring LLM to be used by LlamaIndex
        openai.api_key = os.environ["OpenAI_API_Key"]
        llm = OpenAI(model=Config.llm_model, api_key=os.environ["OpenAI_API_Key"])
        Settings.llm = llm

    def create_documents(self):
        fashion_df = pd.read_csv(Config.dataset_file_path)
        """
        Creates list of Document from the given dataframe of fashion products.
        :param df: Dataframe with data about fashion products.
        :return: List of LlamaIndex documents.
        """
        return [
            Document(
                doc_id=str(row["p_id"]),
                text=row["name"],
                metadata={
                    "description": row["description"],
                    "img": row["img"],
                    "price": row["price"],
                    "color": row["colour"],
                    "brand": row["brand"]
                }
            )
            for _, row in fashion_df.iterrows()
        ]

    def create_vector_store_index(self):
      """
      Create VectorStoreIndex from input list of documents
      """

      documents = self.create_documents()
      self.index = VectorStoreIndex.from_documents(documents)

    def create_query_engine(self):
        """
        Creates query engine for the vector index created.
        :return: RetrieverQueryEngine object.
        """
        # configure retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=Config.similarity_top_k
        )

        # configure response synthesizer
        response_synthesizer = get_response_synthesizer()

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[LLMRerank(top_n=Config.similarity_top_k)]
        )

        return query_engine

    def main(self):
        self.setup_llamaindex_settings()
        self.create_vector_store_index()