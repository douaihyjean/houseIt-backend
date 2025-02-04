from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)  # Equivalent to COLUMN_USER_ID
    full_name = Column(String, nullable=False)  # Equivalent to COLUMN_USER_NAME

    # Relationships
    listings = relationship("Listing", back_populates="user")
    saved_listings = relationship("Saved", back_populates="user")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)  # Equivalent to COLUMN_ID
    title = Column(String, nullable=False)  # Equivalent to COLUMN_TITLE
    price = Column(String, nullable=False)  # Equivalent to COLUMN_PRICE
    address = Column(String, nullable=False)  # Equivalent to COLUMN_ADDRESS
    description = Column(Text, nullable=False)  # Equivalent to COLUMN_DESCRIPTION
    image_uri = Column(String, nullable=True)  # Equivalent to COLUMN_IMAGE_URI
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)  # Equivalent to COLUMN_USER_ID
    user_full_name = Column(String, nullable=False)  # Equivalent to COLUMN_USER_FULL_NAME
    area = Column(String, nullable=False)  # Equivalent to COLUMN_AREA
    bedrooms = Column(String, nullable=False)  # Equivalent to COLUMN_BEDROOMS
    bathrooms = Column(String, nullable=False)  # Equivalent to COLUMN_BATHROOMS
    stories = Column(String, nullable=False)  # Equivalent to COLUMN_STORIES
    mainroad = Column(String, nullable=False)  # Equivalent to COLUMN_MAINROAD
    guestroom = Column(String, nullable=False)  # Equivalent to COLUMN_GUESTROOM
    furnishing_status = Column(String, nullable=False)  # Equivalent to COLUMN_FURNISHING_STATUS
    basement = Column(String, nullable=False)  # Equivalent to COLUMN_BASEMENT
    hot_water_heating = Column(String, nullable=False)  # Equivalent to COLUMN_HOT_WATER_HEATING
    air_conditioning = Column(String, nullable=False)  # Equivalent to COLUMN_AIR_CONDITIONING
    parking = Column(Integer, nullable=False)  # Equivalent to COLUMN_PARKING
    preferred_area = Column(String, nullable=False)  # Equivalent to COLUMN_PREF_AREA

    # Relationships
    user = relationship("User", back_populates="listings")
    saved_listings = relationship("Saved", back_populates="listing")


class Saved(Base):
    __tablename__ = "saved"

    saved_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)

    user = relationship("User", back_populates="saved_listings")
    listing = relationship("Listing", back_populates="saved_listings")