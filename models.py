from app import db

class Shows(db.Model):
    """class person"""
    id = db.Column(db.Integer, primary_key=True)
    tvshow = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.tvshow
