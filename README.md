# LLama Eats - Food Ordering App
<div align="center">
  <img src="assets/cover.jpeg" alt="LLama Eats" width="400">
</div>

This is a food ordering application that allows users to interact with an AI assistant to order food from nearby restaurants. The application uses the Falcon Web Framework, Langchain, and Qdrant for natural language processing and order management. The system leverages advanced language models and embedding techniques to create an intelligent food ordering assistant that understands user preferences and makes contextually aware dish recommendations.

## Demo Video
Working demo can be viewed [here](https://youtu.be/CrdYy5BZYcQ)

## Core Components and Workflow

The system employs `TheBloke/Llama-2-7B-GGUF`, a quantized `LLama-2-7B` model (GGUF format), as its primary language model for understanding user intent during conversations. This model processes user inputs while considering the evolving context of the interaction - tracking what information has been collected (delivery address, food preferences, budget) and what's still needed.

To accurately classify user intents, the system utilizes the `all-MiniLM-L6-v2` embedding model, which converts both user messages and predefined intent categories into high-dimensional vectors. By comparing these vectors through cosine similarity, the system determines whether the user is providing an address, expressing food preferences, setting a budget, or asking general questions.

For budget analysis, the system employs `tensorblock/math_gpt2_sft-GGUF` a specialized fine-tuned `GPT-2` model (also quantized to GGUF format) that's been trained specifically to deduce mathematical values from natural language expressions. This specialized model ensures accurate budget constraint interpretation regardless of how users express their spending limits.

## Key Features

- **Contextual Understanding**: The system maintains conversation context by progressively building a detailed understanding of user requirements. Each piece of information, such as cuisine preferences, delivery location, or budget constraints, enhances the context for subsequent interactions.

- **Intelligent Recommendations**: 
  - If a user requests *Italian food*, the system selects **Caprese Salad** based on the lowest score, showcasing its ability to prioritize the best match:
    - **Score**: 1.0644991397857666
    - **Item**: Caprese Salad
    - **Ingredients**: fresh mozzarella, tomatoes, basil, olive oil, balsamic vinegar
    - **Category**: Italian
  - If the user expands their preference to include *calamari*, the system updates its recommendation to **Fritto Misto**:
    - **Score**: 1.04770827293396
    - **Item**: Fritto Misto
    - **Ingredients**: shrimp, calamari, zucchini, flour, lemon
    - **Category**: Italian

- **Two-Step Filtering Process**:
  1. Identifies dishes matching user preferences through vector similarity.
  2. Applies budget constraints to ensure recommendations stay within specified limits.

- **Final Selection**: Optimizes for user preferences, picking the most relevant dish within the budget.

## User Session Management and Context Tracking
The system implements a cookie-based session management approach to maintain conversation context across multiple interactions. When a user initiates their first request to the server, the system checks for the presence of a user_id cookie. If none exists, the server generates a new UUID, which serves as a unique identifier for that user's session. This UUID is then sent back to the client as a cookie and should be included in all subsequent requests.

The UserStore component uses this UUID to maintain a persistent context for each user throughout their ordering journey. As the conversation progresses and the user provides information about their preferences, delivery location, and budget constraints, all this data is associated with their unique UUID in the UserStore. This stateful approach ensures that the system can maintain context and provide coherent responses even across multiple interactions, creating a seamless ordering experience.

## System Architecture
The system follows a modern client-server architecture designed with security and scalability in mind. At its core, the backend is built on the Falcon framework, a minimalist WSGI web framework for Python that's known for its high performance and reliability. This framework was chosen for its speed and simplicity, making it ideal for handling the specialized nature of our AI-powered ordering system.
The server exposes two primary POST endpoints, each serving a distinct purpose in the ordering flow:

- `/query` - This endpoint handles all interactions with the AI agent, processing natural language inputs and managing the progressive collection of order details.
- `/order` - A separate endpoint dedicated to processing payment details and finalizing orders. This endpoint is deliberately isolated from the AI components of the system to enhance security. By keeping payment processing separate, we ensure that sensitive financial information never passes through the AI models' logging systems, significantly reducing the risk of inadvertent exposure of payment details.

On the client side, the application is built using Next.js, providing a robust and responsive user interface with server-side rendering capabilities.

## Limitations
The current implementation has several notable limitations that should be considered:
Non-OpenAI Compatible Server Architecture
The server implementation is not compatible with OpenAI's API specification (OAI-compatible). This means that existing tools and libraries designed to work with OpenAI's API structure cannot be directly integrated with our system without modifications.
LLM Model Integration Architecture
The current tight coupling between the agent and LLM models creates scalability constraints. A key improvement would be to decouple these components and implement LlamaCpp-server as a microservice. This architectural change would:

### Enable better horizontal scaling
Improve resource utilization
Allow for more flexible model deployment options
Reduce system dependencies

### Testing Coverage
The testing framework currently has limited scope:

Only happy path flows have been thoroughly tested
More comprehensive unit testing coverage is needed
End-to-end (e2e) testing requires expansion
Edge cases and error scenarios need additional test coverage

### Response Quality
The system's responses require refinement in several areas:

Response tone and natural language quality needs improvement
Context awareness in conversations could be enhanced
Response consistency across different scenarios needs standardization

### Preference Management
The preference system has limited support for negative preferences. For example, while users can specify preferences for ingredients they like, they cannot easily exclude ingredients they wish to avoid (such as garlic). A more robust preference management system would enhance user experience and system functionality.

## Prerequisites

Before running the application, make sure you have the following installed:

- Conda (Miniconda or Anaconda)

## Installation

1. Clone the repository

2. Create a virtual environment
    ```
    conda env create --file environment.yaml
    ```
3. Activate the Conda environment:
    ```
    conda activate llama-eats-server
    ```
4. Make sure numpy 1.x.x is installed
    ```
    pip install --upgrade --force-reinstall numpy==1.26.4 --no-cache-dir
    ```
5. (Optionally) For optimisations, install necessary libraries - e.g. Apple Silicon Metal support:
    ```
    CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir
    pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
    ```

Here’s the Markdown section you can add to your `README.md` for the downloading models instructions:

## Download the Required Models

Follow the steps below to download the necessary models for this project:

1. Install `huggingface-cli`
Install the Hugging Face CLI by following the instructions on their website:  
[Hugging Face Hub Installation Guide](https://huggingface.co/docs/huggingface_hub/main/en/installation)

2. Log in to Hugging Face
Log in to your Hugging Face account using the CLI:

    ```bash
    huggingface-cli login
    ```

3. Download `tensorblock/math_gpt2_sft-GGUF`
Download the `tensorblock/math_gpt2_sft-GGUF` model using the Hugging Face CLI:

    ```bash
    huggingface-cli download tensorblock/math_gpt2_sft-GGUF --cache-dir=tmp
    ```

4. Download `TheBloke/Llama-2-7B-GGUF`
Download the `TheBloke/Llama-2-7B-GGUF` model:

    ```bash
    huggingface-cli download TheBloke/Llama-2-7B-GGUF --cache-dir=tmp
    ```

5. Download `sentence-transformers/all-MiniLM-L6-v2`
Download the `sentence-transformers/all-MiniLM-L6-v2` model:

    ```bash
    huggingface-cli download sentence-transformers/all-MiniLM-L6-v2 --cache-dir=tmp
    ```

## Running the Application
Start the Falcon web server:
```
python main.py
```
Use an API testing tool like cURL or Postman to interact with the application.

- To query the AI assistant:
  ```
  POST /query
  Content-Type: application/json

  {
    "input": "What are some good Italian restaurants nearby?"
  }
  ```

## Testing
To run the test suite, execute the following command:
```
python -m unittest discover tests
```
This will run all the test files located in the `tests` directory.

## Limitations

- The application uses mock data for the 3rd party delivery provider API. To use a real API, you would need to replace the `MockEatsAPI` with an actual implementation that communicates with the Uber Eats API.

- Make sure to handle sensitive information, such as payment details, securely in a production environment. The current implementation is for demonstration purposes only and does not include proper security measures.

## Project File Structure Overview

Here's what each file would contain:

#### `models/order.py`
Defines Pydantic models related to orders:
- `OrderItem`: Model for individual order items
- `OrderDetails`: Model for the details of an order
- `OrderDetails`: Model for the credit card details of an order

#### `models/user.py`
Defines Pydantic models related to users, if applicable.

### `services/llm_service.py`
Contains the `OrderingAgent` class that handles interactions with the Language Model (LLM) using Langchain and LlamaIndex.

#### `services/eats`
- `eats_api.py`:Defines an abstract `EatsAPI` interface for food delivery operations and orders.
- `mock_eats_api.py`: Simulates `EatsAPI` functionality with mock data for testing and development.
- `fill_api.py`: Generates mock files with restaurant and food descriptions with random attributes.

#### `services/agents`
- `chains.py` Defines customizable Chains for QA and mathematical reasoning tasks.
- `embeddings.py` Configures embedding generation using HuggingFace for text representation.

#### `stores/userstore.py`
Manages user-specific data, preferences, and vector embeddings.

#### `resources/order_resource.py`
Defines the `OrderResource` class, a Falcon resource for handling order-related requests.

#### `data/venues.json`, `data/menus.json`
JSON files containing mock data for testing purposes:
- `venues.json`: Mock data for nearby venues
- `menus.json`: Mock data for menus

#### `tmp/venues.json`
- `orders.json`: Mock data for orders

#### `tests/test_llm_service.py`
Unit tests for the `OrderingAgent` class, ensuring correct behavior of LLM interactions.

#### `tests/test_uber_eats_api.py`
Unit tests for the `MockUberEatsAPI` class, verifying that the API endpoints function correctly.

#### `tests/test_order_resource.py`
Unit tests for the `OrderResource` class, ensuring the proper handling of order-related requests.

#### `main.py`
The entry point of the application, responsible for:
- Creating the Falcon app
- Initializing necessary dependencies

#### `requirements.yaml`
Lists the required Python packages for the project.