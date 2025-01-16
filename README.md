# Cat Breed Identification and Description App

## Overview

This application allows users to **identify a cat's breed** based on a description of the cat. Additionally, users can **generate a description of a cat breed** by selecting a breed from a dropdown list. The app consists of two main parts:
- **Backend**: A FastAPI application that handles breed identification and description generation.
- **Frontend**: An Angular web application that allows users to interact with the backend.

## Prerequisites

To run the application, you will need the following software installed:

- **Python** (for FastAPI backend)
- **Node.js** and **npm** (for the Angular frontend)
- **FastAPI dependencies** (for backend)
- **Angular dependencies** (npm packages for the frontend)

### Backend (FastAPI) Setup

1. **Navigate to the backend directory** (where `main.py` is located).

2. **Create and activate a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\\venv\\Scripts\\activate  # On Windows
    ```

3. **Install Python dependencies**:
    Make sure you have a `requirements.txt` file in your backend folder. To install dependencies, run:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the FastAPI backend**:
    Run the following command to start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
    This will start the FastAPI backend on `http://127.0.0.1:8000`.

### Frontend (Angular) Setup

1. **Navigate to the frontend directory** (`front/`):
    ```bash
    cd front/
    ```

2. **Install Angular dependencies** using npm:
    ```bash
    npm install
    ```

3. **Start the Angular frontend**:
    After installing dependencies, start the frontend server:
    ```bash
    ng serve
    ```
    This will start the Angular frontend on `http://localhost:4200`.

4. **Ensure proper connection** between the frontend and backend by verifying that the frontend is making requests to the FastAPI server.

## How to Use the App

1. Open your browser and go to `http://localhost:4200` (Angular frontend).
2. You will see two main pages:
    - **Identify Cat Page**: Enter a description of a cat, and the app will attempt to identify its breed using a neural network model based on data from the following database:
      [Cat Breed Database](https://data.mendeley.com/datasets/ht5p5pg7b7/1)
    - **Generate Description Page**: Select a breed from the dropdown, and the app will generate a description for that breed by randomly combining phrases, synonyms, and generating multiple propositions.

### Example Workflow

- On the **Identify Cat** page, you can describe a cat by entering details like fur color, size, and behavior, and the app will identify the breed based on that input.
- On the **Generate Description** page, simply select a breed from the dropdown list, and a detailed description will be generated about that breed.

## Troubleshooting

- **Backend issues**: If the backend doesn't start, make sure that all Python dependencies are installed correctly by running `pip install -r requirements.txt`.
- **Frontend issues**: If the frontend doesn't start, ensure that you have Node.js and npm installed, and that you've installed the necessary frontend dependencies using `npm install`.
- **Ensure both servers are running**: Both the FastAPI backend and the frontend server must be running simultaneously for the application to function properly. The backend runs on `http://127.0.0.1:8000` and the frontend on `http://localhost:4200`.

## Final Notes

- This app provides a simple way to interact with a cat breed identification model and generate breed descriptions.
- You can extend the application by adding more features, such as displaying breed images or including a larger set of breed descriptions.
- If you want to improve the breed identification accuracy, you could integrate an actual machine learning model or external API.

## License

MIT License. See LICENSE for more information.
