from datetime import datetime

from app.extensions import db


class Book(db.Model):
    """A book title held by the library, with a quantity of physical copies."""

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category_id = db.Column(db.Integer,
                             db.ForeignKey('categories.id', ondelete='SET NULL'))
    description = db.Column(db.Text)
    published_year = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    available_quantity = db.Column(db.Integer, nullable=False, default=1)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One book can have many borrowing records over time.
    borrowings = db.relationship('Borrowing', backref='book', lazy=True,
                                  cascade='all, delete-orphan')

    @property
    def is_available(self):
        return self.available_quantity > 0

    def __repr__(self):
        return f'<Book {self.title}>'
