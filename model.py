from sqlalchemy import (Column, Integer, String, Float,
                        ForeignKey, ARRAY, create_engine, MetaData, JSON)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from dotenv import dotenv_values
from json import dumps


def load_connection_info():
    config = dotenv_values(".env")
    return config


Base = declarative_base()


def db_init():
    conn_info = load_connection_info()

    engine = create_engine(
        f"{conn_info['dialect']}://{conn_info['user']}:{conn_info['password']}@{conn_info['host']}:{conn_info['port']}/{conn_info['database']}",
        echo=False)
    # meta = MetaData(engine)
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        # Connect the database if exists.
        engine.connect()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def insert_image(session, input_image):
    # sample input:
    #     input_image = {
    # "url": "./shaas.png",
    # "avg_color": [240, 150, 100],
    # "histogram": [[22, 88], [1, 2]],
    # "objects_freq": { "flower": 2, "sea": 1},
    # "objects_count": 3,
    # }
    image = Image(url=input_image.get("url"),
                  avg_color=input_image.get("avg_color"),
                  histogram=input_image.get("histogram"),
                  objects_freq=dumps(input_image.get("objects_freq")),
                  objects_count=input_image.get("objects_count"),
                  )
    try:
        session.add(image)
    except Exception as e:
        session.rollback()
        return {"success": False, "message": type(e).__name__}
    else:
        session.commit()
        return {"success": True, "image": image}


def insert_video(session, input_video):
    # sample_input:
    # input_video = {
    #         "url": "./Titan.mp4",
    #         "key_frames": [ {
    #             "url": "./Reiner.png",
    #             "avg_color": [1,2,3],
    #             "histogram": [[1,2], [3,4]],
    #             "objects_freq": { "flower": 2, "sea": 1},
    #             "objects_count": 3
    #         },]
    #     }

    video = Video(url=input_video.get("url"))
    try:
        session.add(video)
    except Exception as e:
        session.rollback()
        return {"success": False, "message": type(e).__name__}
    else:
        session.commit()
        video = session.query(Video).filter_by(url=input_video["url"]).one()
        try:
            for frame in input_video["key_frames"]:
                frame["video_id"] = video.id
                image = Image(url=frame["url"],
                              avg_color=frame["avg_color"],
                              histogram=frame["histogram"],
                              objects_freq=dumps(frame["objects_freq"]),
                              objects_count=frame["objects_count"],
                              video_id=frame["video_id"]
                              )

                session.add(image)
        except Exception as e:
            session.rollback()
            return {"success": False, "message": type(e).__name__}
        else:
            session.commit()
            print("committed!")
            return {"success": True, "video": video}
        


# ----------------------------------------------------------------------------------------


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    avg_color = Column(ARRAY(Integer), nullable=False)
    histogram = Column(ARRAY(Float, dimensions=2), nullable=False)
    objects_freq = Column(JSON, nullable=False)
    objects_count = Column(Integer, nullable=False)
    video_id = Column(Integer, ForeignKey("video.id", ondelete="cascade"))

    def __repr__(self):
        return f"""
        Image:
           - id: {self.id}
           - url: {self.url}
           - avg_color: RGB({self.avg_color[0]},{self.avg_color[1]},{self.avg_color[2]})
           - objects_freq: {self.objects_freq}
           - objects_count: {self.objects_count}
           - video_id: {self.video_id}
        """


class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    images = relationship("Image", backref=backref("image"))

    def __repr__(self):
        return f"""
        Video:
           - id: {self.id}
           - url: {self.url}
        """
# ----------------------------------------------------------------------------------------
