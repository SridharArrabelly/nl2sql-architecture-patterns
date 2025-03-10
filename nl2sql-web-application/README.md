
### Installation

A step-by-step series of examples that tell you how to get a development environment running.

#### Setting Up Environment Variables

1. Create a `.env` file in the root directory of your project and fill in the necessary environment variables:

```plaintext
# Database Configuration
db_user = ""
db_password = ""
db_host = ""
db_name = ""

# API Keys
OPENAI_API_KEY=""
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY=""
```

2. Set up a Python virtual environment in your IDE Terminal:

```plaintext
python3 -m venv venv
```

2.1 Enable the virtual environment
```plaintext
venv\Scripts\activate
```

3. Execute this in your IDE Terminal:

```plaintext
pip install -r requirements.txt
```
