from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.community import Community
from app.schemas.community import CommunityCreate, CommunityUpdate, CommunityResponse
from typing import List
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/communities", tags=["Communities"])

# CREATE Community
@router.post("/", response_model=CommunityResponse)
def create_community(community: CommunityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_community = Community(**community.dict())
    db.add(new_community)
    db.commit()
    db.refresh(new_community)
    return new_community

# GET ALL Communities
@router.get("/", response_model=List[CommunityResponse])
def get_communities(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    communities = db.query(Community).all()
    return communities

# GET Communities by Manager Fetch in oah portal.js and oah dashboard.js
@router.get("/manager/{manager_id}", response_model=List[CommunityResponse])
def get_manager_communities(manager_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    communities = db.query(Community).filter(Community.manager_id == manager_id).all()
    return communities

# GET Single Community fetch  Inquiries oah dashboard.js
@router.get("/{community_id}", response_model=CommunityResponse)
def get_community(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community

# UPDATE Community
@router.put("/{community_id}", response_model=CommunityResponse)
def update_community(
    community_id: int, community_update: CommunityUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    for key, value in community_update.dict(
        exclude_unset=True
    ).items():  # Update pannumbodhu:Frontend anuppina fields mattum change Other values safe-aa irukkum
        setattr(community, key, value)

    db.commit()
    db.refresh(community)
    return community


@router.delete("/{community_id}")
def delete_community(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    db.delete(community)
    db.commit()
    return {"message": "Community deleted successfully"}
