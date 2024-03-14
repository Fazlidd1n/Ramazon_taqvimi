import requests
from sqlalchemy import BIGINT, select, insert
from sqlalchemy.orm import mapped_column, Mapped
from bs4 import BeautifulSoup
from db.config import engine, Base, session

engine.connect()


class BotUser(Base):
    __tablename__ = 'bot_users'
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(__type_pos=BIGINT, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)

    def insert_user(self, user_id, fullname, username):
        user_data = {
            'user_id': user_id,
            'fullname': fullname,
            'username': username,
        }
        user: BotUser | None = session.execute(select(BotUser).where(BotUser.user_id == user_id)).fetchone()
        if not user:
            session.execute(insert(BotUser).values(**user_data))
            session.commit()

    def select_user(self):
        users_datas = session.execute(select(BotUser.user_id, BotUser.fullname, BotUser.user_id)).fetchall()
        return users_datas


class RamadanCalendar(Base):
    __tablename__ = 'ramadan_calendar'
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, autoincrement=True, primary_key=True)
    day: Mapped[int] = mapped_column(unique=True, nullable=True)
    day_name: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=True)
    s_time: Mapped[str] = mapped_column(nullable=True)
    i_time: Mapped[str] = mapped_column(nullable=True)

    def insert_data(self, x: dict):
        s = list(x.keys())
        for i in range(len(s)):
            datas = {
                "day": s[i],
                "day_name": x.get(s[i])[0],
                "date": x.get(s[i])[1],
                "s_time": x.get(s[i])[2],
                "i_time": x.get(s[i])[3]
            }
            data: RamadanCalendar | None = session.execute(
                select(RamadanCalendar).where(RamadanCalendar.day == x.get('day'))).fetchone()
            if not data:
                session.execute(insert(RamadanCalendar).values(**datas))
                session.commit()

    def select_data(self, x):
        datas = session.execute(select(RamadanCalendar).where(RamadanCalendar.date == x)).fetchone()
        return datas

    def select_time(self):
        response = requests.get("https://namozvaqti.uz/ramazon/toshkent")
        soup = BeautifulSoup(response.text, 'html.parser')
        currencies = {}
        for i in soup.find_all("tr"):
            datas_elements = i.find_all('td')
            if datas_elements:
                day = int(datas_elements[0].text)
                day_name = datas_elements[1].text
                date = datas_elements[2].text
                s_time = datas_elements[3].text
                i_time = datas_elements[4].text
                currencies[day] = [day_name, date, s_time, i_time]

        return currencies


Base.metadata.create_all(engine)
if not session.execute(select(RamadanCalendar.day)).fetchall():
    RamadanCalendar.insert_data(Base, RamadanCalendar.select_time(Base))
