# initialize pinecone
import pinecone

from src.common.utils import (
    PINECONE_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
)

DIMENSION = 1536
METRIC = "cosine"
POD_TYPE = "p1.x1"


# get the existing index in pinecone or create a new one
def init_pinecone(index_name, flag=True):
    pinecone.init(api_key=PINECONE_KEY, environment=PINECONE_ENV)
    if flag:
        return pinecone.Index(index_name)
    else:
        # create a new index in pinecone
        return pinecone.create_index(
            index_name, dimension=DIMENSION, metric=METRIC, pod_type=POD_TYPE
        )


# get pinecone index name
def get_pinecone_index_name(uuid):
    return PINECONE_INDEX_NAME + "-" + uuid


def get_pinecone_index_namespace(uuid):
    return PINECONE_NAMESPACE + "-" + uuid
