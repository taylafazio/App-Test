# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# 1. Serve the Frontend HTML
@app.get("/")
async def get_homepage():
    try:
        with open("index.html", "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Error: index.html not found!</h1><p>Make sure index.html is in the same folder as main.py</p>", status_code=404)

# 2. Manage WebSocket Connections & Game State
class GameManager:
    def __init__(self):
        self.active_connections = []
        self.board = [""] * 9
        self.current_turn = "X"
        self.players = {} # Maps the connection to "X" or "O"

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Assign roles based on connection order
        if len(self.active_connections) == 1:
            self.players[websocket] = "X"
        elif len(self.active_connections) == 2:
            self.players[websocket] = "O"
        else:
            self.players[websocket] = "Spectator"

        await self.broadcast_state()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.players:
            del self.players[websocket]
        
        # If someone leaves, wipe the board clean so the remaining player can wait for a new game
        if len(self.active_connections) < 2:
            self.board = [""] * 9
            self.current_turn = "X"

    async def broadcast_state(self):
        """Sends the current board and turn to all connected players."""
        base_state = {
            "board": self.board,
            "current_turn": self.current_turn,
            "players_connected": len(self.active_connections)
        }
        
        for connection in self.active_connections:
            # Tell each specific client who they are
            client_state = {**base_state, "role": self.players.get(connection, "Spectator")}
            await connection.send_text(json.dumps(client_state))

    async def process_move(self, index: int, player: str):
        """Validates and updates a move."""
        if self.board[index] == "" and player == self.current_turn:
            self.board[index] = player
            # Switch turns
            self.current_turn = "O" if self.current_turn == "X" else "X"
            await self.broadcast_state()

    async def reset_game(self):
        self.board = [""] * 9
        self.current_turn = "X"
        await self.broadcast_state()

manager = GameManager()

# 3. The WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Wait for a message from a player
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["action"] == "move":
                await manager.process_move(message["index"], message["player"])
            elif message["action"] == "reset":
                await manager.reset_game()
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_state()