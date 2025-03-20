from sqlalchemy import Column, Integer, String, Float, DateTime #, ForeignKey
from database import Base
"""
from datatime import datatime
from sqlalchemy.orm import relationship

"""

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    youtube_url = Column(String, unique=True, nullable=False)
    mentor_email = Column(String, nullable=False)
    category = Column(String, nullable=False)
    stars = Column(Float, default=0.0)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    publication_date = Column(DateTime)# , default= datatime.utcnow
    title = Column(String) #nullable = True
    description = Column(String) # nullable = True

    """
    Selon mes analyses c'est possible qu'il ait une relation avec Progress

    progress = relationship("Progress", back_populates = "video", cascade = "all.delete-orphin")
    """
    
class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=False, #ForeignKey("videos.id", ondelete = "Cascade"))
    mentee_email = Column(String, nullable=False)
    watched = Column(Integer, default=0)

    # Et aussi uje relation avec Vidéo
    video = relationship("video", back_populates = "progresses")
