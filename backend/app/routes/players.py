from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.player import PlayerResponse, PlayerUpdate
from app.models.auth import TokenData
from app.core.database import db
from app.core.deps import get_current_user_token
from bson import ObjectId

router = APIRouter()

@router.get("/me", response_model=PlayerResponse)
async def read_users_me(current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "player":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.db.players.find_one({"_id": ObjectId(current_user.id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "player":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = db.db.players.delete_one({"_id": ObjectId(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.put("/me", response_model=PlayerResponse)
async def update_user_me(player_update: PlayerUpdate, current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "player":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in player_update.model_dump().items() if v is not None}
    
    if update_data:
        db.db.players.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": update_data}
        )
    
    user = db.db.players.find_one({"_id": ObjectId(current_user.id)})
    return user

@router.get("/", response_model=List[PlayerResponse])
async def read_players(skip: int = 0, limit: int = 100):
    players = list(db.db.players.find().skip(skip).limit(limit))
    return players

@router.get("/{player_id}", response_model=PlayerResponse)
async def read_player(player_id: str):
    if not ObjectId.is_valid(player_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    player = db.db.players.find_one({"_id": ObjectId(player_id)})
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
