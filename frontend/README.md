# Frontend Application

This text User and Order Management frontend is built with React + Vite.

## Prerequisites

You need **Node.js** installed to run this application.
You can download it from [nodejs.org](https://nodejs.org/).

## Getting Started

1.  **Install Dependencies**
    Open your terminal in this `frontend` directory and run:

    ```bash
    npm install
    ```

2.  **Run Development Server**
    Start the frontend server:

    ```bash
    npm run dev
    ```

3.  **Access the App**
    Open your browser to `http://localhost:5173`.

## Features

-   **Authentication**: Login and Register with JWT support.
-   **Orders**: View your orders, filter by status, and create new orders.
-   **Premium UI**: Glassmorphism design, smooth animations, and responsive layout.

## API Connection

The app is configured to proxy API requests to your FastAPI backend at `http://localhost:8000`.
Ensure your backend is running (`uvicorn main:app --reload`) before using the frontend.
