
# Agent Arena Report

## User idea


I want to build a system where users upload project documents.
The system processes the documents, indexes them, and then two agents propose
one architecture using Azure and another architecture using AWS.
A judge agent compares both proposals.
The MVP must run locally first and avoid paid cloud resources.


---

# Azure Architecture Proposal

## 1. Executive summary
The proposed architecture is a multi-agent system that allows users to submit project documents, which are then processed and evaluated by various agents to propose architectures for Azure and AWS. The architecture emphasizes simplicity and low cost, suitable for a minimum viable product (MVP) that can initially run locally before transitioning to the cloud. Key components include a FastAPI backend, Microsoft Agent Framework, and Azure Blob Storage for document storage. This architecture aligns with the project's goals of learning and clear decision-making. Evidence: [CTX-0020], [CTX-0024].

## 2. Recommended components

### Component: FastAPI
Role: Backend framework to handle user requests.
Why: FastAPI is lightweight and suitable for building APIs, making it ideal for the initial MVP.
Evidence: [CTX-0024]

### Component: Microsoft Agent Framework
Role: Orchestrates the various agents involved in the architecture evaluation process.
Why: It provides a structured way to manage the workflow of different agents, which is central to the project.
Evidence: [CTX-0020], [CTX-0024]

### Component: Azure Blob Storage
Role: Stores the generated architecture recommendations as Markdown documents.
Why: It provides a cost-effective and scalable solution for document storage.
Evidence: [CTX-0024]

### Component: Application Insights
Role: Monitors logs, errors, and latency in the application.
Why: It enhances observability, which is important for understanding application performance and user interactions.
Evidence: [CTX-0024], [CTX-0093]

### Component: RequirementsAgent
Role: Extracts structured requirements from user submissions.
Why: This agent is essential for gathering the necessary information to propose relevant architectures.
Evidence: [CTX-0020], [CTX-0024]

### Component: AzureSolutionAgent
Role: Proposes an Azure architecture based on the extracted requirements.
Why: It ensures that the architecture aligns with Azure's capabilities and best practices.
Evidence: [CTX-0020], [CTX-0024]

### Component: AWSSolutionAgent
Role: Proposes an AWS architecture based on the extracted requirements.
Why: It provides a comparative perspective, allowing users to evaluate both cloud options.
Evidence: [CTX-0020], [CTX-0024]

### Component: CloudComparisonAgent
Role: Compares the Azure and AWS proposals.
Why: This agent facilitates informed decision-making by evaluating the strengths and weaknesses of each architecture.
Evidence: [CTX-0020], [CTX-0024]

### Component: FinalDecisionAgent
Role: Recommends a final architecture based on the comparison.
Why: It consolidates the findings and provides a clear recommendation to the user.
Evidence: [CTX-0020], [CTX-0024]

## 3. Proposed flow
1. A user submits a project idea through a FastAPI frontend [CTX-0024].
2. The FastAPI backend receives the request and initiates a workflow using the Microsoft Agent Framework [CTX-0020].
3. The RequirementsAgent extracts structured requirements from the user submission [CTX-0020].
4. The AzureSolutionAgent proposes an Azure architecture based on the requirements [CTX-0020].
5. The AWSSolutionAgent proposes an AWS architecture based on the same requirements [CTX-0020].
6. The CloudComparisonAgent compares both architecture proposals [CTX-0020].
7. The FinalDecisionAgent recommends a final architecture based on the comparison [CTX-0020].
8. The generated recommendation is stored as Markdown in Azure Blob Storage [CTX-0024].
9. Application Insights monitors logs, errors, and latency throughout the process [CTX-0024].

## 4. Trade-offs
- Azure SQL Database may be unnecessary at the beginning, as the MVP can function without persistent storage for users or history [CTX-0027].
- Introducing too many managed services early on could lead to increased costs and complexity [CTX-0027].

## 5. MVP approach
The MVP can start locally using a Python notebook or a local FastAPI app, allowing for iterative development and testing without incurring cloud costs. This approach aligns with the recommendation to start local before moving to the cloud [CTX-0084].

## 6. Missing context
- Specific requirements for user authentication and security measures are not addressed, which could be important for a production-ready system.
- Details on how the agents will be implemented and interact with each other are not provided, which could clarify the architecture's operational aspects.

---

# AWS Architecture Proposal

## 1. Executive summary
The proposed architecture leverages AWS services to create a system where users can upload project documents, which are then processed and indexed. The architecture includes components for storage, backend processing, and orchestration of agents that will propose cloud architectures. The system is designed to start locally before transitioning to the cloud, aligning with best practices for early learning projects. Key components include Amazon S3 for storage, Amazon ECS Fargate for backend deployment, and the Microsoft Agent Framework for orchestration. Evidence for these choices is drawn from the context provided.

## 2. Recommended components

### Component: Amazon S3
Role: Storage for project documents and generated reports.
Why: S3 provides simple and cost-effective storage, which is essential for handling user-uploaded documents and storing outputs.
Evidence: [CTX-0016]

### Component: Amazon ECS Fargate
Role: Backend processing for handling document uploads and processing.
Why: ECS Fargate allows for containerized deployment of the backend, which is suitable for running the application in a managed environment.
Evidence: [CTX-0006]

### Component: Microsoft Agent Framework
Role: Orchestration of the multi-agent workflow.
Why: This framework is specifically mentioned for orchestrating the agents that will propose cloud architectures, making it a fitting choice for this project.
Evidence: [CTX-0002]

### Component: Amazon RDS PostgreSQL
Role: Database for structured persistence of user data and project information.
Why: Although it may be unnecessary for the MVP, it is recommended for structured data storage as the project scales.
Evidence: [CTX-0006]

### Component: AWS Secrets Manager
Role: Management of sensitive information such as API keys and database credentials.
Why: It is crucial for securely storing secrets needed for the application to function properly.
Evidence: [CTX-0003]

### Component: Amazon CloudWatch
Role: Monitoring and logging of application performance.
Why: CloudWatch provides observability, which is important for tracking application metrics and logs.
Evidence: [CTX-0003]

## 3. Proposed flow
1. **User uploads project documents**: Users interact with the frontend to upload documents, which are stored in Amazon S3 for easy access and retrieval. [CTX-0016]
2. **Document processing**: The backend, deployed on Amazon ECS Fargate, processes the uploaded documents. [CTX-0006]
3. **Agent orchestration**: The Microsoft Agent Framework orchestrates the workflow, allowing different agents to propose architectures based on the processed documents. [CTX-0002]
4. **Data storage**: User data and project information are stored in Amazon RDS PostgreSQL for structured persistence. [CTX-0006]
5. **Secrets management**: AWS Secrets Manager is used to manage sensitive information required for the application. [CTX-0003]
6. **Monitoring**: Amazon CloudWatch monitors the application, providing logs and metrics for performance tracking. [CTX-0003]

## 4. Trade-offs
- **Complexity vs. Learning**: The architecture is more complex than using Azure for a Microsoft Agent Framework learning project, which may slow down the initial MVP development. [CTX-0008]
- **RDS necessity**: Using Amazon RDS PostgreSQL may be unnecessary for the MVP if persistence is not immediately required. [CTX-0008]

## 5. MVP approach
The MVP should start locally using a Python notebook or a local FastAPI application to prototype the document upload and processing workflow. This aligns with the recommended progression of starting local before moving to cloud deployment. [CTX-0084]

## 6. Missing context
- Specific requirements for document processing and indexing are not provided.
- Details on the expected user load and traffic patterns are missing, which would help in sizing the architecture appropriately.
- Information on the frontend technology stack is not included, which is necessary for a complete architecture proposal.

---

# Architecture Comparison

## 1. Executive recommendation
Recommend Azure. The Azure proposal emphasizes simplicity and low cost, which is suitable for a minimum viable product (MVP) that can initially run locally before transitioning to the cloud. The use of Azure Blob Storage for document storage and the structured workflow managed by the Microsoft Agent Framework aligns well with the project's goals of learning and clear decision-making. Evidence: [CTX-0020], [CTX-0024].

## 2. Azure strengths
- The architecture emphasizes simplicity and low cost, suitable for a minimum viable product (MVP) that can initially run locally before transitioning to the cloud. Evidence: [CTX-0020], [CTX-0024].
- FastAPI is lightweight and suitable for building APIs, making it ideal for the initial MVP. Evidence: [CTX-0024].
- Azure Blob Storage provides a cost-effective and scalable solution for document storage. Evidence: [CTX-0024].
- Application Insights enhances observability, which is important for understanding application performance and user interactions. Evidence: [CTX-0024], [CTX-0093].
- The architecture includes a CloudComparisonAgent that facilitates informed decision-making by evaluating the strengths and weaknesses of each architecture. Evidence: [CTX-0020], [CTX-0024].

## 3. AWS strengths
- Amazon S3 provides simple and cost-effective storage, which is essential for handling user-uploaded documents and storing outputs. Evidence: [CTX-0016].
- ECS Fargate allows for containerized deployment of the backend, which is suitable for running the application in a managed environment. Evidence: [CTX-0006].
- Amazon CloudWatch provides observability, which is important for tracking application metrics and logs. Evidence: [CTX-0003].

## 4. Key trade-offs
- Azure SQL Database may be unnecessary at the beginning, as the MVP can function without persistent storage for users or history. Evidence: [CTX-0027].
- Introducing too many managed services early on could lead to increased costs and complexity. Evidence: [CTX-0027].
- The architecture is more complex than using Azure for a Microsoft Agent Framework learning project, which may slow down the initial MVP development. Evidence: [CTX-0008].
- Using Amazon RDS PostgreSQL may be unnecessary for the MVP if persistence is not immediately required. Evidence: [CTX-0008].

## 5. Recommended next step
The next practical step for the project is to develop the MVP locally using a Python notebook or a local FastAPI application, allowing for iterative development and testing without incurring cloud costs. This aligns with the recommendation to start local before moving to the cloud. Evidence: [CTX-0084].
