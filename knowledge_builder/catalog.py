"""
Service catalog: curated list of cloud services with their official documentation URLs.

Every URL points to the official vendor documentation. The scraper fetches these
pages and extracts factual data only — no invented content.

Structure per service:
  - name: Display name
  - provider: azure | aws | gcp
  - category: The functional category (compute, storage, ai, database, etc.)
  - urls: Dict of page_type -> URL (overview, limits, pricing)
  - tags: For search/filtering
"""

AZURE_SERVICES = {
    "azure_openai_service": {
        "name": "Azure OpenAI Service",
        "provider": "azure",
        "category": "ai",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/ai-services/openai/overview",
            "quotas": "https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/",
            "models": "https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models",
        },
        "tags": ["llm", "gpt", "embeddings", "chat", "completions"],
    },
    "azure_ai_search": {
        "name": "Azure AI Search",
        "provider": "azure",
        "category": "search",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search",
            "limits": "https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/search/",
            "vector_search": "https://learn.microsoft.com/en-us/azure/search/vector-search-overview",
        },
        "tags": ["search", "vector", "hybrid", "rag", "semantic_ranking"],
    },
    "azure_document_intelligence": {
        "name": "Azure AI Document Intelligence",
        "provider": "azure",
        "category": "ai",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview",
            "limits": "https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/",
        },
        "tags": ["ocr", "document_extraction", "forms", "invoices"],
    },
    "azure_container_apps": {
        "name": "Azure Container Apps",
        "provider": "azure",
        "category": "compute",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/container-apps/overview",
            "limits": "https://learn.microsoft.com/en-us/azure/container-apps/quotas",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-apps/",
        },
        "tags": ["containers", "serverless", "microservices", "deployment"],
    },
    "azure_functions": {
        "name": "Azure Functions",
        "provider": "azure",
        "category": "compute",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview",
            "limits": "https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/",
        },
        "tags": ["serverless", "event_driven", "functions"],
    },
    "azure_blob_storage": {
        "name": "Azure Blob Storage",
        "provider": "azure",
        "category": "storage",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview",
            "limits": "https://learn.microsoft.com/en-us/azure/storage/common/scalability-targets-standard-account",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/",
        },
        "tags": ["object_storage", "documents", "blobs"],
    },
    "azure_cosmos_db": {
        "name": "Azure Cosmos DB",
        "provider": "azure",
        "category": "database",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/cosmos-db/introduction",
            "limits": "https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/",
            "vector_search": "https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search",
        },
        "tags": ["nosql", "multi_model", "global_distribution", "vector_search"],
    },
    "azure_api_management": {
        "name": "Azure API Management",
        "provider": "azure",
        "category": "networking",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts",
            "limits": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#api-management-limits",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/api-management/",
        },
        "tags": ["api_gateway", "rate_limiting", "authentication"],
    },
    "azure_service_bus": {
        "name": "Azure Service Bus",
        "provider": "azure",
        "category": "messaging",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview",
            "limits": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-bus/",
        },
        "tags": ["messaging", "queues", "topics", "async"],
    },
    "azure_logic_apps": {
        "name": "Azure Logic Apps",
        "provider": "azure",
        "category": "integration",
        "urls": {
            "overview": "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview",
            "limits": "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/",
        },
        "tags": ["workflow", "automation", "connectors", "low_code"],
    },
}

AWS_SERVICES = {
    "aws_bedrock": {
        "name": "Amazon Bedrock",
        "provider": "aws",
        "category": "ai",
        "urls": {
            "overview": "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html",
            "quotas": "https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html",
            "pricing": "https://aws.amazon.com/bedrock/pricing/",
            "agents": "https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html",
        },
        "tags": ["llm", "foundation_models", "agents", "rag", "knowledge_bases"],
    },
    "aws_opensearch": {
        "name": "Amazon OpenSearch Service",
        "provider": "aws",
        "category": "search",
        "urls": {
            "overview": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html",
            "limits": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html",
            "pricing": "https://aws.amazon.com/opensearch-service/pricing/",
        },
        "tags": ["search", "vector", "hybrid", "analytics", "logs"],
    },
    "aws_s3": {
        "name": "Amazon S3",
        "provider": "aws",
        "category": "storage",
        "urls": {
            "overview": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
            "limits": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html",
            "pricing": "https://aws.amazon.com/s3/pricing/",
        },
        "tags": ["object_storage", "documents", "data_lake"],
    },
    "aws_lambda": {
        "name": "AWS Lambda",
        "provider": "aws",
        "category": "compute",
        "urls": {
            "overview": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
            "limits": "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html",
            "pricing": "https://aws.amazon.com/lambda/pricing/",
        },
        "tags": ["serverless", "functions", "event_driven"],
    },
    "aws_ecs_fargate": {
        "name": "Amazon ECS with Fargate",
        "provider": "aws",
        "category": "compute",
        "urls": {
            "overview": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/what-is-fargate.html",
            "limits": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-quotas.html",
            "pricing": "https://aws.amazon.com/fargate/pricing/",
        },
        "tags": ["containers", "serverless", "deployment"],
    },
    "aws_dynamodb": {
        "name": "Amazon DynamoDB",
        "provider": "aws",
        "category": "database",
        "urls": {
            "overview": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html",
            "limits": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html",
            "pricing": "https://aws.amazon.com/dynamodb/pricing/",
        },
        "tags": ["nosql", "key_value", "serverless"],
    },
    "aws_step_functions": {
        "name": "AWS Step Functions",
        "provider": "aws",
        "category": "integration",
        "urls": {
            "overview": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
            "limits": "https://docs.aws.amazon.com/step-functions/latest/dg/limits-overview.html",
            "pricing": "https://aws.amazon.com/step-functions/pricing/",
        },
        "tags": ["workflow", "orchestration", "state_machine"],
    },
    "aws_textract": {
        "name": "Amazon Textract",
        "provider": "aws",
        "category": "ai",
        "urls": {
            "overview": "https://docs.aws.amazon.com/textract/latest/dg/what-is.html",
            "limits": "https://docs.aws.amazon.com/textract/latest/dg/limits.html",
            "pricing": "https://aws.amazon.com/textract/pricing/",
        },
        "tags": ["ocr", "document_extraction", "forms", "tables"],
    },
    "aws_api_gateway": {
        "name": "Amazon API Gateway",
        "provider": "aws",
        "category": "networking",
        "urls": {
            "overview": "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html",
            "limits": "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html",
            "pricing": "https://aws.amazon.com/api-gateway/pricing/",
        },
        "tags": ["api_gateway", "rest", "websocket"],
    },
    "aws_sagemaker": {
        "name": "Amazon SageMaker",
        "provider": "aws",
        "category": "ai",
        "urls": {
            "overview": "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html",
            "limits": "https://docs.aws.amazon.com/general/latest/gr/sagemaker.html",
            "pricing": "https://aws.amazon.com/sagemaker/pricing/",
        },
        "tags": ["ml", "training", "inference", "endpoints"],
    },
}

GCP_SERVICES = {
    "gcp_vertex_ai": {
        "name": "Vertex AI",
        "provider": "gcp",
        "category": "ai",
        "urls": {
            "overview": "https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform",
            "quotas": "https://cloud.google.com/vertex-ai/docs/quotas",
            "pricing": "https://cloud.google.com/vertex-ai/pricing",
            "gemini": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models",
        },
        "tags": ["llm", "gemini", "ml", "agents", "search"],
    },
    "gcp_cloud_run": {
        "name": "Cloud Run",
        "provider": "gcp",
        "category": "compute",
        "urls": {
            "overview": "https://cloud.google.com/run/docs/overview/what-is-cloud-run",
            "limits": "https://cloud.google.com/run/quotas",
            "pricing": "https://cloud.google.com/run/pricing",
        },
        "tags": ["containers", "serverless", "deployment"],
    },
    "gcp_cloud_functions": {
        "name": "Cloud Functions",
        "provider": "gcp",
        "category": "compute",
        "urls": {
            "overview": "https://cloud.google.com/functions/docs/concepts/overview",
            "limits": "https://cloud.google.com/functions/quotas",
            "pricing": "https://cloud.google.com/functions/pricing",
        },
        "tags": ["serverless", "functions", "event_driven"],
    },
    "gcp_cloud_storage": {
        "name": "Cloud Storage",
        "provider": "gcp",
        "category": "storage",
        "urls": {
            "overview": "https://cloud.google.com/storage/docs/introduction",
            "quotas": "https://cloud.google.com/storage/quotas",
            "pricing": "https://cloud.google.com/storage/pricing",
        },
        "tags": ["object_storage", "documents", "data_lake"],
    },
    "gcp_firestore": {
        "name": "Firestore",
        "provider": "gcp",
        "category": "database",
        "urls": {
            "overview": "https://cloud.google.com/firestore/docs/overview",
            "limits": "https://cloud.google.com/firestore/quotas",
            "pricing": "https://cloud.google.com/firestore/pricing",
        },
        "tags": ["nosql", "document", "realtime", "serverless"],
    },
    "gcp_bigquery": {
        "name": "BigQuery",
        "provider": "gcp",
        "category": "analytics",
        "urls": {
            "overview": "https://cloud.google.com/bigquery/docs/introduction",
            "quotas": "https://cloud.google.com/bigquery/quotas",
            "pricing": "https://cloud.google.com/bigquery/pricing",
            "vector_search": "https://cloud.google.com/bigquery/docs/vector-search-intro",
        },
        "tags": ["analytics", "data_warehouse", "sql", "vector_search"],
    },
    "gcp_document_ai": {
        "name": "Document AI",
        "provider": "gcp",
        "category": "ai",
        "urls": {
            "overview": "https://cloud.google.com/document-ai/docs/overview",
            "quotas": "https://cloud.google.com/document-ai/quotas",
            "pricing": "https://cloud.google.com/document-ai/pricing",
        },
        "tags": ["ocr", "document_extraction", "forms"],
    },
    "gcp_pubsub": {
        "name": "Pub/Sub",
        "provider": "gcp",
        "category": "messaging",
        "urls": {
            "overview": "https://cloud.google.com/pubsub/docs/overview",
            "quotas": "https://cloud.google.com/pubsub/quotas",
            "pricing": "https://cloud.google.com/pubsub/pricing",
        },
        "tags": ["messaging", "event_driven", "streaming"],
    },
    "gcp_cloud_sql": {
        "name": "Cloud SQL",
        "provider": "gcp",
        "category": "database",
        "urls": {
            "overview": "https://cloud.google.com/sql/docs/introduction",
            "quotas": "https://cloud.google.com/sql/docs/quotas",
            "pricing": "https://cloud.google.com/sql/pricing",
        },
        "tags": ["sql", "postgresql", "mysql", "relational"],
    },
    "gcp_api_gateway": {
        "name": "API Gateway",
        "provider": "gcp",
        "category": "networking",
        "urls": {
            "overview": "https://cloud.google.com/api-gateway/docs/about-api-gateway",
            "limits": "https://cloud.google.com/api-gateway/quotas",
            "pricing": "https://cloud.google.com/api-gateway/pricing",
        },
        "tags": ["api_gateway", "rest", "openapi"],
    },
}

# Full catalog
SERVICE_CATALOG = {
    **AZURE_SERVICES,
    **AWS_SERVICES,
    **GCP_SERVICES,
}


def get_services_by_provider(provider: str) -> dict:
    return {k: v for k, v in SERVICE_CATALOG.items() if v["provider"] == provider}


def get_all_service_keys() -> list[str]:
    return list(SERVICE_CATALOG.keys())
