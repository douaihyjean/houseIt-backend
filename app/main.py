from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .database import engine, SessionLocal

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",  # For Android emulators
    "http://your-frontend-domain.com",  # Replace with your actual frontend domain
    "http://your-mobile-app-url"        # Replace with your app's URL if applicable
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow specific origins
    allow_credentials=True,      # Allow credentials like cookies, tokens, etc.
    allow_methods=["*"],         # Allow all HTTP methods
    allow_headers=["*"],         # Allow all headers
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# User Endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    The userId is expected to be retrieved from Firebase Authentication and passed by the frontend.
    """
    db_user = crud.get_user_by_id(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get a user by their Firebase userId.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Listing Endpoints
@app.post("/listings/", response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    """
    Create a new listing in the database.
    """
    return crud.create_listing(db=db, listing=listing)


@app.get("/listings/", response_model=List[schemas.Listing])
def get_listings(
    skip: int = 0,
    limit: int = 10,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of listings with optional filtering by user_id and pagination.
    """
    if user_id:
        listings = crud.get_listings_by_user(db, user_id=user_id)
    else:
        listings = crud.get_listings(db)
    return listings[skip: skip + limit]


@app.get("/listings/{listing_id}", response_model=schemas.Listing)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Get a listing by its ID.
    """
    db_listing = crud.get_listing_by_id(db, listing_id=listing_id)
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_listing


@app.delete("/listings/{listing_id}", response_model=schemas.Listing)
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Delete a listing by its ID.
    """
    db_listing = crud.delete_listing(db, listing_id=listing_id)
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_listing


@app.put("/listings/{listing_id}", response_model=schemas.Listing)
def update_listing(
    listing_id: int, listing: schemas.ListingCreate, db: Session = Depends(get_db)
):
    """
    Update a listing by its ID.
    """
    updated_listing = crud.update_listing(db, listing_id=listing_id, listing=listing)
    if not updated_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return updated_listing


# Saved Listings Endpoints
@app.post("/saved/", response_model=schemas.Saved)
def save_listing(saved: schemas.SavedCreate, db: Session = Depends(get_db)):
    """
    Save a listing for a user.
    """
    db_user = crud.get_user_by_id(db, saved.user_id)
    db_listing = crud.get_listing_by_id(db, saved.listing_id)
    if not db_user or not db_listing:
        raise HTTPException(status_code=404, detail="User or Listing not found")
    return crud.save_listing(db=db, saved=saved)


@app.get("/saved/{user_id}", response_model=List[schemas.Listing])
def get_saved_listings(user_id: str, db: Session = Depends(get_db)):
    """
    Get all saved listings for a user.
    """
    saved = crud.get_saved_listings_for_user(db, user_id=user_id)
    if not saved:
        raise HTTPException(status_code=404, detail="No saved listings found")
    return [s.listing for s in saved]


@app.delete("/saved/", response_model=schemas.Saved)
def delete_saved_listing(user_id: str, listing_id: int, db: Session = Depends(get_db)):
    """
    Delete a saved listing for a user.
    """
    deleted_saved = crud.delete_saved_listing(db, user_id=user_id, listing_id=listing_id)
    if not deleted_saved:
        raise HTTPException(status_code=404, detail="Saved listing not found")
    return deleted_saved


@app.get("/users/{user_id}/full_name", response_model=str)
def get_user_full_name(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.full_name
