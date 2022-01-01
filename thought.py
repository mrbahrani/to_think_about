from datetime import date

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class Thought(Base):
    __tablename__ = 'thought'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_to_alarm = Column(Date)
    deleted = Column(Integer, default=0)


if __name__ == "__main__":
    engine = create_engine('sqlite:///xxx.db')
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    t = Thought(id=15, name="worst_idea", date_to_alarm=date.today())
    s.add(t)
    x = s.query(Thought).filter_by(date_to_alarm=date.today()).all()
    s.commit()
    pass

