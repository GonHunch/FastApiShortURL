from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from app.schemas import UrlCreateSchema, UrlUpdateSchema
from app.database import get_db
from app.models import Url
import uuid
from datetime import datetime
from urllib.parse import unquote


router = APIRouter()


@router.post("/links/shorten", status_code=status.HTTP_201_CREATED)
async def create_short_link(data: UrlCreateSchema, db=Depends(get_db)):
    if data.custom_alias:
        if db.query(Url).filter(Url.short_code == data.custom_alias).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Alias already exists")
        short_code = data.custom_alias
    else:
        short_code = str(uuid.uuid4())[:6]  # Случайный шорт-код для стандарта

    new_url = Url(original_url=data.url,
                  short_code=short_code,
                  created_at=datetime.utcnow(),
                  expires_at=datetime.strptime(data.expires_at, "%Y-%m-%dT%H:%M") if data.expires_at else None,
                  click_count=0,
                  last_clicked_at=None
                  )

    db.add(new_url)
    db.commit()
    return {"short_url": f"http://localhost:8000/{short_code}"}


@router.get("/links/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_original(short_code: str, db=Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    if url.expires_at and url.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL has expired")

    url.click_count += 1
    url.last_clicked_at = datetime.now()
    db.commit()
    return RedirectResponse(url.original_url)


@router.delete("/links/{short_code}")
async def delete_link(short_code: str, db=Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    db.delete(url)
    db.commit()
    return {"message": "URL deleted"}


@router.put("/links/{short_code}")
async def update_link(short_code: str, data: UrlUpdateSchema, db=Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    if db.query(Url).filter(Url.short_code == data.new_short_code).first():
        raise HTTPException(status_code=409, detail="Short code already exists")

    url.short_code = data.new_short_code
    if data.expires_at:
        url.expires_at = datetime.strptime(data.expires_at, "%Y-%m-%dT%H:%M")

    db.commit()
    return {"message": "URL updated"}


@router.get("/links/{short_code}/stats")
async def get_stats(short_code: str, db=Depends(get_db)):
    url = db.query(Url).filter(Url.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    stats = {
        "original_url": url.original_url,
        "created_at": url.created_at,
        "click_count": url.click_count,
        "last_clicked_at": url.last_clicked_at
    }
    return stats


@router.get("/links/search")
async def search_url(original_url: str, db=Depends(get_db)):
    decoded_url = unquote(original_url)
    urls = db.query(Url).filter(Url.original_url == decoded_url).all()
    return [{"short_code": url.short_code} for url in urls]