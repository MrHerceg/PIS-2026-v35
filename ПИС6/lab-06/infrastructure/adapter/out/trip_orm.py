from sqlalchemy import Column, String, Float, Date, JSON
from infrastructure.config.database import Base


class TripORM(Base):
    __tablename__ = "trips"

    id         = Column(String, primary_key=True, index=True)
    owner_id   = Column(String, nullable=False, index=True)
    title      = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date   = Column(Date, nullable=False)
    budget     = Column(Float, nullable=False, default=0.0)
    status     = Column(String, nullable=False, default="PLANNED")
    route_ids  = Column(JSON, nullable=False, default=list)
    notes      = Column(JSON, nullable=False, default=list)

    def __repr__(self):
        return f"<TripORM id={self.id!r} title={self.title!r}>"
