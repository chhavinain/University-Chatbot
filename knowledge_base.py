import boto3

# Configuration
region = "us-east-1"
knowledge_base_name = "my-opensearch-kb-v2"
s3_bucket_arn = ""
s3_data_prefix = "document.csv"
role_arn = ""
opensearch_collection_arn = ""
opensearch_vector_index_name = "mytraditionalkb-idx"
embedding_model_arn = "amazon.nova-pro-v1:0"

# Initialize Bedrock Agent client
bedrock = boto3.client("bedrock-agent", region_name=region)

# Step 1: Create Knowledge Base
create_kb_response = bedrock.create_knowledge_base(
    name=knowledge_base_name,
    description="Knowledge base using OpenSearch and S3",
    roleArn=role_arn,
    knowledgeBaseConfiguration={
        "type": "VECTOR",
        "vectorKnowledgeBaseConfiguration": {
            "embeddingModelArn": embedding_model_arn
        }
    },
    storageConfiguration={
        "type": "OPENSEARCH_SERVERLESS",
        "opensearchServerlessConfiguration": {
            "collectionArn": opensearch_collection_arn,
            "vectorIndexName": opensearch_vector_index_name,
            "fieldMapping": {
                "metadataField": "metadata",
                "textField": "text",
                "vectorField": "vector"
            }
        }
    }
)

kb_id = create_kb_response["knowledgeBase"]["knowledgeBaseId"]
print(" Knowledge Base created:", kb_id)

# Step 2: Create Data Source from S3
create_ds_response = bedrock.create_data_source(
    knowledgeBaseId=kb_id,
    name="s3-source",
    dataSourceConfiguration={
        "type": "S3",
        "s3Configuration": {
            "bucketArn": s3_bucket_arn,
            "inclusionPrefixes": [s3_data_prefix]
        }
    },
    vectorIngestionConfiguration={
        "chunkingConfiguration": {
            "chunkingStrategy": "FIXED_SIZE",
            "fixedSizeChunkingConfiguration": {
                "maxTokens": 500,
                "overlapPercentage": 20
            }
        }
    }
)

ds_id = create_ds_response["dataSource"]["dataSourceId"]
print(" Data Source created:", ds_id)

# Step 3: Start Ingestion Job
ingestion_response = bedrock.start_ingestion_job(
    knowledgeBaseId=kb_id,
    dataSourceId=ds_id
)

ingestion_job_id = ingestion_response["ingestionJob"]["ingestionJobId"]
print(" Ingestion job started:", ingestion_job_id)
