The Elevator Pitch
A full-stack, real-time multiplayer web application that allows users to generate private 5-digit room codes and play Tic-Tac-Toe across different devices instantly. It bypasses traditional HTTP requests in favor of persistent, bidirectional connections to ensure zero-latency gameplay.

The Tech Stack
Backend: Python, FastAPI, Uvicorn

Frontend: Vanilla JavaScript, HTML5, CSS3

Protocol: WebSockets

Version Control & Hosting: Git, GitHub, Render (PaaS)

Key Technical Milestones Achieved
WebSocket Implementation: Replaced standard HTTP request/response cycles with WebSockets (ws:// and wss://) to achieve real-time, bidirectional communication between the server and multiple clients.

State Management: Engineered a Python backend capable of managing multiple concurrent game states in memory. The server acts as the "source of truth," validating moves, managing turns, and broadcasting updates to the correct clients.

Scalable Room Architecture: Implemented a lobby system using dynamic dictionary routing in FastAPI. This allows the server to isolate game states based on unique 5-digit codes, scaling the app from a single game to theoretically limitless concurrent private rooms.

Cloud Deployment & CI/CD: Connected a local Git repository to GitHub and deployed the application to the internet using Render, configuring the environment to serve a Uvicorn ASGI application on a public port.
