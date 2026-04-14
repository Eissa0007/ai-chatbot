# AI Chatbot Application

This application is a simple AI chatbot built using Flask for the backend and HTML/CSS/JavaScript for the frontend. It integrates with the Groq API to provide chatbot functionalities.

## Requirements

- Python 3.6+
- Flask
- Requests

## Running the Application

1. Clone the repository:
    ```bash
    git clone https://github.com/Eissa0007/ai-chatbot.git
    cd ai-chatbot
    ```
2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the environment variables in a `.env` file using the `.env.example` as a guide.
4. Run the application:
    ```bash
    python server.py
    ```
5. Access the application at `http://127.0.0.1:5000`.

## Docker

To run the application using Docker, use the following commands:

1. Build the Docker image:
    ```bash
    docker-compose build
    ```
2. Start the application:
    ```bash
    docker-compose up
    ```

## API Integration

This application uses the Groq API to handle the chatbot functionalities. Make sure to read the Groq API documentation for details on how to integrate and use their services.

## License

This project is licensed under the MIT License.