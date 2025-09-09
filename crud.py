from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from models import Animal

def upsert_collection(session: Session, data: Dict[str, Any]) -> Animal:
    stmt = insert(Animal).values(**data)
    update_cols = {k: stmt.inserted[k] for k in data.keys() if k != "id"}
    stmt = stmt.on_duplicate_key_update(**update_cols)

    session.execute(stmt)
    session.commit()

    sci = data["scientific_name"]
    obj = session.query(Animal).filter(Animal.scientific_name == sci).one()
    return obj