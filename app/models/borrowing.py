from datetime import datetime

from app.extensions import db


class Borrowing(db.Model):
    """One borrow/return record linking a user to a book."""

    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer,
                         db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('Borrowed', 'Returned', 'Overdue', name='borrowing_status'),
                        nullable=False, default='Borrowed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Borrowing user={self.user_id} book={self.book_id} status={self.status}>'
