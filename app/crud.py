import logging
from sqlalchemy.orm import Session
from . import models, schemas


# CRUD operations for Users
def get_user_by_id(db: Session, user_id: str):
    """Retrieve a user by Firebase user_id."""
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user in the database."""
    db_user = models.User(user_id=user.user_id, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# CRUD operations for Listings
def get_listings(db: Session):
    """Retrieve all listings from the database."""
    return db.query(models.Listing).all()


def get_listing_by_id(db: Session, listing_id: int):
    """Retrieve a listing by its ID."""
    return db.query(models.Listing).filter(models.Listing.id == listing_id).first()


def create_listing(db: Session, listing: schemas.ListingCreate):
    """Create a new listing in the database."""
    db_listing = models.Listing(
        title=listing.title,
        price=listing.price,
        address=listing.address,
        description=listing.description,
        image_uri=listing.image_uri,
        user_id=listing.user_id,  # Retrieved from Firebase
        user_full_name=listing.user_full_name,
        area=listing.area,
        bedrooms=listing.bedrooms,
        bathrooms=listing.bathrooms,
        stories=listing.stories,
        mainroad=listing.mainroad,
        guestroom=listing.guestroom,
        furnishing_status=listing.furnishing_status,
        basement=listing.basement,
        hot_water_heating=listing.hot_water_heating,
        air_conditioning=listing.air_conditioning,
        parking=listing.parking,
        preferred_area=listing.preferred_area,
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


def delete_listing(db: Session, listing_id: int):
    """Delete a listing by its ID."""
    try:
        logging.info(f"Querying listing with ID: {listing_id}")
        db_listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
        if not db_listing:
            logging.warning(f"Listing with ID {listing_id} not found in database.")
            return None
        db.delete(db_listing)
        db.commit()
        logging.info(f"Listing with ID {listing_id} deleted successfully.")
        return db_listing
    except Exception as e:
        logging.error(f"Error during deletion: {str(e)}")
        raise


def update_listing(db: Session, listing_id: int, listing: schemas.ListingCreate):
    """Update an existing listing with new details."""
    db_listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not db_listing:
        return None

    for key, value in listing.dict().items():
        setattr(db_listing, key, value)

    db.commit()
    db.refresh(db_listing)
    return db_listing


# CRUD operations for Saved Listings
def get_saved_listings_for_user(db: Session, user_id: str):
    """Retrieve all saved listings for a specific user."""
    return db.query(models.Saved).filter(models.Saved.user_id == user_id).all()


def save_listing(db: Session, saved: schemas.SavedCreate):
    """Save a listing to the saved listings table."""
    db_saved = models.Saved(user_id=saved.user_id, listing_id=saved.listing_id)
    db.add(db_saved)
    db.commit()
    db.refresh(db_saved)
    return db_saved


def delete_saved_listing(db: Session, user_id: str, listing_id: int):
    """Delete a saved listing for a user."""
    db_saved = (
        db.query(models.Saved)
        .filter(models.Saved.user_id == user_id, models.Saved.listing_id == listing_id)
        .first()
    )
    if db_saved:
        db.delete(db_saved)
        db.commit()
    return db_saved

def save_listing(db: Session, saved: schemas.SavedCreate):
    """
    Save a listing for a user in the database.
    """
    db_saved = models.Saved(user_id=saved.user_id, listing_id=saved.listing_id)
    db.add(db_saved)
    db.commit()
    db.refresh(db_saved)
    return db_saved

