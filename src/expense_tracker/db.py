from typing import Dict, List, Optional, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from expense_tracker.globals import ENGINE
from expense_tracker.models import Category

def get_categories() -> Union[Exception, Dict]:
    try:
        with Session(ENGINE) as session:
            rows = session.scalars(select(Category)).all() 
            return {row.name: row.tags.split(",") for row in rows}
    except Exception as e:
        return e

def add_category(category: str, tags: List[str]) -> None:
    with Session(ENGINE) as session:
        session.add(Category(name=category, tags=",".join(tags)))
        session.commit()


def delete_category(category_name: str) -> Optional[Exception]:
    try:
        with Session(ENGINE) as session:
            session.query(Category).filter(Category.name==category_name).delete()
            session.commit()
    except Exception as e:
        return e

def update_category(category_name: str, tags: list[str]) -> Optional[Exception]:
    try:
        with Session(ENGINE) as session:
            session.query(Category).filter(Category.name == category_name).update({"tags": ",".join(tags)})
            session.commit()
    except Exception as e:
        return e
    
