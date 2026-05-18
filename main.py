# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.get("/")
async def get_homepage():
    try:
        with open("index.html", "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Error: index.html not found!</h1>", status_code=404)

# 1. New Structure: A class for an individual room
class GameRoom:
    def __init__(self):
        self.active_connections = []
        self.board = [""] * 9
        self.current_turn = "X"
        self.players = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
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

    async def broadcast_state(self):
        base_state = {
            "board": self.board,
            "current_turn": self.current_turn,
            "players_connected": len(self.active_connections)
        }
        for connection in self.active_connections:
            client_state = {**base_state, "role": self.players.get(connection, "Spectator")}
            await connection.send_text(json.dumps(client_state))

    async def process_move(self, index: int, player: str):
        if self.board[index] == "" and player == self.current_turn:
            self.board[index] = player
            self.current_turn = "O" if self.current_turn == "X" else "X"
            await self.broadcast_state()

    async def reset_game(self):
        self.board = [""] * 9
        self.current_turn = "X"
        await self.broadcast_state()

# 2. Dictionary to hold all active games
rooms = {}

# 3. Updated Endpoint: Now accepts a room_code in the URL
@app.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    # If the room doesn't exist yet, create it
    if room_code not in rooms:
        rooms[room_code] = GameRoom()
        
    room = rooms[room_code]
    await room.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["action"] == "move":
                await room.process_move(message["index"], message["player"])
            elif message["action"] == "reset":
                await room.reset_game()
                
    except WebSocketDisconnect:
        room.disconnect(websocket)
        # Clean up: If everyone leaves the room, delete the room from memory
        if len(room.active_connections) == 0:
            del rooms[room_code]
        else:
            await room.broadcast_state()