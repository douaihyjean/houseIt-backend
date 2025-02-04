from pydantic import BaseModel
from typing import Optional, List


# Schema for Listings
class ListingBase(BaseModel):
    title: str
    price: str
    address: str
    description: str
    image_uri: Optional[str]
    user_id: str  # Retrieved from Firebase Authentication
    user_full_name: str
    area: str
    bedrooms: str
    bathrooms: str
    stories: str
    mainroad: str
    guestroom: str
    furnishing_status: str
    basement: str
    hot_water_heating: str
    air_conditioning: str
    parking: int
    preferred_area: str


class ListingCreate(ListingBase):
    pass


class Listing(ListingBase):
    id: int  # Auto-incremented ID for the listing

    class Config:
        orm_mode = True


# Schema for Users
class UserBase(BaseModel):
    user_id: str  # Retrieved from Firebase Authentication
    full_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    listings: List[Listing] = []  # List of listings created by the user
    saved_listings: List["Saved"] = []  # List of saved listings for the user

    class Config:
        orm_mode = True


# Schema for Saved Listings
class SavedBase(BaseModel):
    user_id: str  # Retrieved from Firebase Authentication
    listing_id: int  # ID of the listing being saved


class SavedCreate(SavedBase):
    pass


class Saved(SavedBase):
    saved_id: int  # Auto-incremented ID for the saved entry
    user: Optional[User]  # The user who saved the listing
    listing: Optional[Listing]  # The saved listing

    class Config:
        orm_mode = True
