from sqlalchemy import Column, String, BigInteger, Boolean, Integer, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from venue_vendue.data_models.base_meta import Base


class TopArtistsDataModel(Base):
    __tablename__ = 'top_artists'
    id = Column(String, primary_key=True)
    time_range = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    popularity = Column(BigInteger, nullable=False)
    rank = Column(BigInteger, nullable=False)

    UniqueConstraint(id, time_range)

    def __repr__(self):
        return f"<TopArtistsDataModel {self.name} {self.time_range} #{self.rank}>"
