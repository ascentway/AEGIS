from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.organization import OrganizationResponse, OrganizationUpdate
from app.models.auth import TokenData
from app.core.database import db
from app.core.deps import get_current_user_token
from bson import ObjectId

router = APIRouter()

@router.get("/me", response_model=OrganizationResponse)
async def read_org_me(current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "organization":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    org = db.db.organizations.find_one({"_id": ObjectId(current_user.id)})
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_org_me(current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "organization":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = db.db.organizations.delete_one({"_id": ObjectId(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Organization not found")
    return None

@router.put("/me", response_model=OrganizationResponse)
async def update_org_me(org_update: OrganizationUpdate, current_user: TokenData = Depends(get_current_user_token)):
    if current_user.role != "organization":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in org_update.model_dump().items() if v is not None}
    
    if update_data:
        db.db.organizations.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": update_data}
        )
    
    org = db.db.organizations.find_one({"_id": ObjectId(current_user.id)})
    return org

@router.get("/{org_id}", response_model=OrganizationResponse)
async def read_org(org_id: str):
    if not ObjectId.is_valid(org_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    org = db.db.organizations.find_one({"_id": ObjectId(org_id)})
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
