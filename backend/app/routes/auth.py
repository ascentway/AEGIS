from fastapi import APIRouter, HTTPException, status, Body
from app.models.auth import Token, UserLogin
from app.models.player import PlayerCreate, PlayerInDB, PlayerResponse
from app.models.organization import OrganizationCreate, OrganizationInDB, OrganizationResponse
from app.core.database import db
from app.core.security import get_password_hash, verify_password, create_access_token
from bson import ObjectId

router = APIRouter()

@router.post("/register/player", response_model=PlayerResponse)
async def register_player(player: PlayerCreate):
    # Check if user already exists
    if db.db.players.find_one({"email": player.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(player.password)
    player_in_db = PlayerInDB(**player.model_dump(), hashed_password=hashed_password)
    
    # Exclude id (None) and hashed_password from the insert dict 
    # But wait, we need hashed_password in DB
    player_dict = player_in_db.model_dump(by_alias=True, exclude={"id"})
    
    result = db.db.players.insert_one(player_dict)
    player_in_db.id = str(result.inserted_id)
    
    return player_in_db

@router.post("/register/organization", response_model=OrganizationResponse)
async def register_organization(org: OrganizationCreate):
    # Check if user already exists
    if db.db.organizations.find_one({"email": org.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(org.password)
    org_in_db = OrganizationInDB(**org.model_dump(), hashed_password=hashed_password)
    
    org_dict = org_in_db.model_dump(by_alias=True, exclude={"id"})
    
    result = db.db.organizations.insert_one(org_dict)
    org_in_db.id = str(result.inserted_id)
    
    return org_in_db

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    user = None
    collection = None
    
    if login_data.role == "player":
        user = db.db.players.find_one({"email": login_data.email})
        collection = db.db.players
    elif login_data.role == "organization":
        user = db.db.organizations.find_one({"email": login_data.email})
        collection = db.db.organizations
    
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        subject=str(user["_id"]), 
        role=login_data.role
    )
    return {"access_token": access_token, "token_type": "bearer"}
