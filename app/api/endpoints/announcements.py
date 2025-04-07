"""Announcement API endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import func

from app.db.session import get_db
from app.db.models import Announcement
from app.schemas.announcement import AnnouncementResponse

router = APIRouter()


@router.get("/", response_model=List[AnnouncementResponse])
def get_announcements(db: Session = Depends(get_db)):
    """
    Retrieve all announcements with their related programs, institutions and states
    """
    try:
        # Fetch all announcements with eager loading of related entities
        # Fixed: Load relationships separately to avoid the nested attribute error
        announcements = (
            db.query(Announcement)
            .options(
                joinedload(Announcement.programs),
                joinedload(Announcement.institution),
                joinedload(Announcement.state),
            )
            .filter(Announcement.announcement_type != "admission_dates")
            .order_by(func.random())  # Randomize the results
            .limit(10)
            .all()
        )

        return announcements

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching announcements: {str(e)}"
        )


@router.get("/admission-dates", response_model=List[AnnouncementResponse])
def get_admission_dates_announcements(db: Session = Depends(get_db)):
    """
    Retrieve up to 10 random announcements with announcement_type="admission_dates"
    and their related programs, institutions and states
    """
    try:
        # Fetch announcements filtered by announcement_type, randomized and limited to 10
        announcements = (
            db.query(Announcement)
            .options(
                joinedload(Announcement.programs),
                joinedload(Announcement.institution),
                joinedload(Announcement.state),
            )
            .filter(Announcement.announcement_type == "admission_dates")
            .order_by(func.random())  # Randomize the results
            .limit(10)
            .all()  # Limit to 10 items
        )

        return announcements

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching admission dates announcements: {str(e)}",
        )


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
def get_announcement(announcement_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a specific announcement by ID with its related programs, institution and state
    """
    try:
        # Fetch the specific announcement with eager loading of related entities
        # Fixed: Load relationships separately to avoid the nested attribute error
        announcement = (
            db.query(Announcement)
            .options(
                joinedload(Announcement.programs),
                joinedload(Announcement.institution),
                joinedload(Announcement.state),
            )
            .filter(Announcement.announcement_id == announcement_id)
            .first()
        )

        if not announcement:
            raise HTTPException(status_code=404, detail="Announcement not found")

        return announcement

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching announcement: {str(e)}"
        )
