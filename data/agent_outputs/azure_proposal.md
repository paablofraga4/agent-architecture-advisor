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