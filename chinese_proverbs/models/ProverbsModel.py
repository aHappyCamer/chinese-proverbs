from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProverbsModel(db.Model):
    """
    Defines the Proverbs model
    """

    __tablename__ = "proverbs"

    p_id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    chinese = db.Column("chinese", db.String, unique=True, nullable=False)
    pinyin = db.Column("pinyin", db.String, unique=True, nullable=False)
    p_translation = db.Column("p_translation", db.String, unique=True, nullable=False)

    def __init__(self, chinese, pinyin, p_translation):
        self.chinese = chinese.decode('utf-8')
        self.pinyin = pinyin
        self.p_translation = p_translation
        # self.origin = origin

    def __repr__(self):
        return f"<Proverb {self.chinese}>"

    @property
    def serialize(self):
        """
        Return proverb in serializable format
        """

        return {"chinese": self.chinese, "pinyin": self.pinyin, "translation": self.p_translation}
