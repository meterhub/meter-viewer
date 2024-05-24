from meterviewer.models.littledb import get_session, Item
from pathlib import Path as P
from sqlalchemy import select


def get_first_item(dbpath: P) -> Item:
    session = get_session(str(dbpath))
    stmt = select(Item).where(Item.id == 1)
    result = session.execute(stmt)
    return result.scalar_one()
