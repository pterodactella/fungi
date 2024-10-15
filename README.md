### Chatbot Project
This project consists of a FastAPI-based backend and a Next.js frontend for a chatbot that interacts with users and provides information about coins (for now just the price of a given coin and the list of stable coins). Due to time constrains, this is a minimum viable product, it didn't take more than 3-4 hours and should be assesed accordingly. [See Demo](https://www.youtube.com/watch?v=7lAyHlCS3m8)

## Prerequisites

- Python 3.9+
- `pip` (Python package installer)
- `virtualenv or conda` (optional but recommended, i personally don't like virtualenv as it creates a env folder in the repo :D which of course can be ignored in a .gitignore file)
- Node.js and npm

## Setup

### Backend

1. **Set up environment variables:**

```sh
conda create --name fungi python=3.10
conda activate fungi
```

2. **Install dependencies:**

```sh
pip install -r requirements.txt
```

3. **Start the FastAPI server:**

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will be running at `http://0.0.0.0:8000`.

### Frontend

1. **Navigate to the frontend directory:**

   ```sh
   cd ../chatbot-frontend
   ```

2. **Install dependencies:**

   ```sh
   npm install
   ```

3. **Run the development server:**

   ```sh
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## API Endpoints

### `/chat` (POST)

This endpoint accepts a chat request and returns a chat response.

- **Request Body:**

  ```json
  {
    "prompt": "Your message here"
  }
  ```

- **Response Body:**

  ```json
  {
    "response": "Chatbot's response"
  }
  ```

## How It Works

### Backend

1. **Environment Variables:**

   The application loads environment variables using the `load_env_variables` function from `config.py`. This includes the OpenAI API key required for generating responses.

2. **FastAPI Setup:**

   The FastAPI application is set up in `app.py`

3. **State Graph:**

   The chatbot uses a state graph defined by the `StateGraph` class from `langgraph.graph`. Nodes and edges are added to the graph to define the conversation flow.

   - **Nodes:**

     - `chatbot`: Initial node that handles user messages.
     - `query_coin_price`: Node that queries the price of a specific coin.
     - `list_stablecoins`: Node that lists all stablecoins.

   - **Edges:**
     - Transitions from `chatbot` to `query_coin_price` or `list_stablecoins`.

4. **Chat Endpoint:**

   The `/chat` endpoint defined in `app.py` handles incoming chat requests. It initializes the state with the user's message and invokes the state graph to process the message and generate a response.

### Frontend

1. **Next.js Setup:**

   The frontend is built using Next.js. The main page is defined in `page.tsx`, which includes the `Chatbot` component.

2. **Chatbot Component:**

   The `Chatbot` component handles user input and displays the chatbot's responses. It communicates with the backend via the `/chat` endpoint.
