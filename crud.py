from models import Episode
from sqlalchemy.orm import Session

def create_episode(db: Session, title: str, story: str, image_data: bytes,user_id:int):
    ep = Episode(title=title, story=story, image_data=image_data,user_id=user_id)
    db.add(ep)
    db.commit()
    db.refresh(ep)
    return ep

def get_all_episodes(db: Session ,user_id:int):
     return db.query(Episode).filter_by(user_id=user_id).order_by(Episode.date.asc()).all()

def get_recent_episodes(db:Session,user_id:int, limit=3):
    return db.query(Episode).filter_by(user_id=user_id).order_by(Episode.date.desc()).limit(limit).all()

def delete_all_episodes(db: Session,user_id: int):
    db.query(Episode).filter_by(user_id=user_id).delete()
    db.commit()

def get_latest_episode(db: Session, user_id: int):
    return db.query(Episode).filter_by(user_id=user_id).order_by(Episode.id.desc()).first()

def delete_this_episode(db: Session, episode_id: int, user_id: int):
    episode = db.query(Episode).filter_by(id=episode_id, user_id=user_id).first()
    if episode:
        db.delete(episode)
        db.commit()
        return True
    return False

def get_episode_by_id(db: Session, episode_id: int, user_id: int):
    return db.query(Episode).filter_by(id=episode_id, user_id=user_id).first()