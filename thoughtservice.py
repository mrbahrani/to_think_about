from datetime import date, timedelta
from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from thought import Thought
from thought import Base


def db_exists(file_name):
    if not isfile(file_name):
        return False
    return True


class ThoughtService:
    def __init__(self, file_name="main.db"):
        self.engine = create_engine('sqlite:///{}'.format(file_name))
        if not db_exists(file_name):
            Base.metadata.create_all(self.engine)
            
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_thought(self, thought):
        self.session.add(thought)
        self.session.commit()

    def get_thoughts_of_the_day(self, date):
        return self.session.query(Thought).filter(Thought.date_to_alarm == date, Thought.deleted == 0).all()

    def update_thought(self, update_dict):
        pass

    def proceed_thought(self, identity):
        print("iddddd", identity)
        t: Thought = self.session.query(Thought).filter(Thought.id == identity).first()
        t.date_to_alarm = date.today() + timedelta(days=2)
        self.session.commit()

    def delete_thought(self, identity):
        t: Thought = self.session.query(Thought).filter(Thought.id == identity).first()
        t.deleted = 1
        self.session.commit()

    def review_all(self):
        return self.session.query(Thought).filter(Thought.deleted == 0).all()


if __name__ == "__main__":
    ts = ThoughtService()
    th = Thought(id=2, name="ass2", date_to_alarm=date.today())
    ts.add_thought(th)
    x = ts.get_thoughts_of_the_day(date.today())
    pass
