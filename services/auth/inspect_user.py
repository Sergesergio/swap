from repository.database import engine
from sqlmodel import Session, select
from models import UserAuth

with Session(engine) as s:
    res = s.exec(select(UserAuth).where(UserAuth.email=='user2@test.com'))
    user = res.one()
    print('TYPE', type(user))
    print('ID', user.id)
    print('USERNAME', user.username)
    print('EMAIL', user.email)
