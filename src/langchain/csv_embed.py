import os

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import json

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def csv_embed():
    loader = CSVLoader(file_path="src/langchain/phone.csv", encoding="utf8")
    data = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    result = list()
    for t in data:
        query_result = embeddings.embed_query(t.page_content)
        result.append(query_result)
    with open("src/langchain/phone.json", "w") as outfile:
        json.dump(result, outfile, indent=2)


if __name__ == "__main__":
    csv_embed()
