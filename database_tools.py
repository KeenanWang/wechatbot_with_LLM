import time

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/wechatbot?charset=utf8mb4", echo=True)

DBSession = sessionmaker(bind=engine)


# 签到表
class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, name='id', primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, comment='姓名')
    assignment = Column(String(200), nullable=False, comment='任务')
    date = Column(Date, nullable=False)

    def __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment
        self.date = time.strftime('%Y-%m-%d', time.localtime())


class Advice(Base):
    __tablename__ = 'advice'
    id = Column(Integer, name='id', primary_key=True, autoincrement=True)
    advice = Column(String(200), nullable=False, comment='建议')
    time = Column(Date, nullable=False)

    def __init__(self, advice):
        self.advice = advice
        self.time = time.strftime('%Y-%m-%d', time.localtime())


Base.metadata.create_all(engine)


def getSession():
    return DBSession()


def checkAttendance(session, person):
    attendance = session.query(Attendance).filter_by(name=person,
                                                     date=time.strftime('%Y-%m-%d', time.localtime())).first()
    return True if attendance else False


def attendanceSubmit(session, person, msg):
    session.add(Attendance(name=person, assignment=msg))
    session.commit()


def adviceSubmit(session, msg):
    session.add(Advice(msg))
    session.commit()


if __name__ == '__main__':
    session = getSession()
    all_attendance = session.query(Attendance).filter_by(name='').all()
    print(all_attendance)
