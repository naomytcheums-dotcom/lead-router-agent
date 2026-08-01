from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_site_password
from app.database import get_db
from app.models import CompanyProfile, TeamMember
from app.schemas import CompanyProfileIn, CompanyProfileOut, TeamMemberIn, TeamMemberOut

router = APIRouter(dependencies=[Depends(require_site_password)])


@router.get("/api/company-profile", response_model=CompanyProfileOut | None)
def get_profile(db: Session = Depends(get_db)):
    return db.query(CompanyProfile).first()


@router.put("/api/company-profile", response_model=CompanyProfileOut)
def upsert_profile(payload: CompanyProfileIn, db: Session = Depends(get_db)):
    profile = db.query(CompanyProfile).first()
    if not profile:
        profile = CompanyProfile()
        db.add(profile)
    profile.company_name = payload.company_name
    profile.products_and_services = payload.products_and_services
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/api/team", response_model=list[TeamMemberOut])
def list_team(db: Session = Depends(get_db)):
    return db.query(TeamMember).order_by(TeamMember.created_at).all()


@router.post("/api/team", response_model=TeamMemberOut)
def add_team_member(payload: TeamMemberIn, db: Session = Depends(get_db)):
    member = TeamMember(name=payload.name, email=payload.email, responsibility=payload.responsibility)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/api/team/{member_id}")
def remove_team_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(404, "Team member not found.")
    db.delete(member)
    db.commit()
    return {"ok": True}
