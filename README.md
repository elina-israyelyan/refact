# ReAct API

A FastAPI-based reasoning and action execution system that combines Large Language Models (LLMs) with external tools to perform complex reasoning tasks. The system implements the ReAct (Reasoning + Acting) paradigm, allowing AI agents to reason through problems step-by-step while executing actions to gather information or perform calculations.
The ReAct paradigm is based on the [`ReAct: Synergizing Reasoning and Acting in Language Models`]( https://arxiv.org/abs/2210.03629)


## 📋 Prerequisites

- Python 3.10+


## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd refact
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**
   - Download your Google Cloud service account JSON file
   - Set the `GEMINI_SA_CREDENTIAL_PATH` environment variable to point to your credentials file

## ⚙️ Configuration

The API uses environment variables for configuration:

```bash
export GEMINI_SA_CREDENTIAL_PATH=/path/to/your/credentials.json
export LLM_CLIENT_TYPE=gemini  # Options: 'gemini', 'mock'
export SEARCH_CLIENT_TYPE=wiki   # Options: 'wiki', 'mock'
```

### Configuration Options

- **LLM_CLIENT_TYPE**: 
  - `gemini`: Use Google Gemini models (requires credentials)
  - `mock`: Use mock LLM for testing
- **SEARCH_CLIENT_TYPE**:
  - `wiki`: Use real Wikipedia API
  - `mock`: Use mock search responses for testing

## 🚀 Running the API

### Using the provided script
```bash
./run.sh
```

### Manual startup
```bash
export GEMINI_SA_CREDENTIAL_PATH=/path/to/your/credentials.json
PYTHONPATH=src uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API Documentation will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 📡 API Endpoints

### 1. `/v1/refact` - Main ReAct Endpoint

**POST** `/v1/refact`

Performs step-by-step reasoning with action execution. Returns a streaming response showing the reasoning process.

**Request Body:**
```json
{
  "prompt": "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"
}
```

**Response:** Streaming text showing reasoning steps and actions performed.

**Example Response:**
```
Thought 1: I need to find the highest mountain in Armenia. I will use the search tool to find the answer.

---------
Observation 1: Mount Aragats (Armenian: Արագած, pronounced [ɑɾɑˈɡɑt͡s]) is an isolated four-peaked volcano massif in Armenia. Its northern summit, at 4,090 m (13,420 ft) above sea level, is the highest point of the Lesser Caucasus and Armenia. It is also one of the highest points in the Armenian Highlands.
The Aragats massif is surrounded by the Kasagh River on the east, the Akhurian River on the west, Ararat Plain on the south, and Shirak Plain on the north. The circumference of the massif is around 200 km (120 mi), and covers an area of 6,000 km2 (2,300 sq mi) or around 1⁄5 of Armenia's total area.

Thought 1: The highest mountain in Armenia is Mount Aragats, with its northern summit reaching 4,090 meters (13,420 feet) above sea level.

---------
Final answer: The highest mountain in Armenia is Mount Aragats, with its northern summit reaching 4,090 meters (13,420 feet) above sea level.
```

### 2. `/v1/act` - Direct Action Execution

**POST** `/v1/act`

Executes a specific action directly without reasoning.

**Request Body:**
```json
{
  "action": {
    "action_method_name": "sum",
    "a": 5,
    "b": 3
  }
}
```

**Response:**
```json
{
  "result": 8.0
}
```

### 3. `/v1/reason` - Pure Reasoning

**POST** `/v1/reason`

Performs reasoning without executing actions.

**Request Body:**
```json
{
  "prompt": "What would be the steps to calculate the area of a circle?"
}
```

**Response:**
```json
{
  "text": "To calculate the area of a circle, you need to follow these steps:

1.  **Find the radius (r):** The radius is the distance from the center of the circle to any point on its edge.
2.  **Square the radius:** Multiply the radius by itself (r * r or r^2).
3.  **Multiply by pi (π):**  Pi is a mathematical constant approximately equal to 3.14159. Multiply the result from step 2 by pi.

The formula for the area of a circle is: Area = π * r^2. This formula provides the area in square units (e.g., square inches, square meters) based on the units used for the radius."
}
```

## 🔧 Available Actions

### Mathematical Actions (`MathActions`)

- **sum(a: float, b: float)**: Add two numbers
- **subtract(a: float, b: float)**: Subtract b from a
- **multiply(a: float, b: float)**: Multiply two numbers
- **divide(a: float, b: float)**: Divide a by b
- **power(a: float, b: float)**: Raise a to the power of b

### Search Actions (`SearchActions`)

- **search(entity: str)**: Search Wikipedia for information about an entity
- **lookup(entity: str, string: str)**: Look up specific text within a Wikipedia article

## 🏗️ Architecture

### Core Components

1. **ReAct Engine** (`src/services/refact.py`)
   - Manages the reasoning loop
   - Coordinates between reasoning and action execution
   - Handles streaming responses

2. **Action System** (`src/actions/`)
   - Modular action framework
   - Extensible action sets
   - Automatic Pydantic model generation

3. **LLM Integration** (`src/llm/`)
   - Abstract LLM client interface
   - Google Gemini implementation
   - Mock client for testing

4. **Search System** (`src/actions/search/`)
   - Wikipedia API integration
   - Mock search for testing
   - Factory pattern for client selection

### Key Classes

- **ThoughtTraceGenerator**: Generates reasoning steps using LLM
- **ActionSet**: Base class for action collections
- **BaseLLMClient**: Abstract interface for LLM clients
- **BaseWikiClient**: Abstract interface for search clients

## 🧪 Testing

### Mock Mode

For testing without external dependencies:

```bash
export LLM_CLIENT_TYPE=mock
export SEARCH_CLIENT_TYPE=mock
```
