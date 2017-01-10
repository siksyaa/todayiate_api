from flask_api_app.database import RoleMixin, UserMixin, BaseMixin
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from ...database import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    foo = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(20), unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.CHAR(1))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)
    dummy = db.Column(db.Integer)


class Relationship(db.Model, BaseMixin):
    __tablename__ = 'relationships'
    __table_args__ = (
        (UniqueConstraint("user_id", "followed_by_id", name="unique_idx_user_id_followed_by_id")),
    )

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    followed_by_id = db.Column(db.Integer, ForeignKey('users.id'))

    user = relationship('User', foreign_keys=user_id, backref='followed_by')
    followed_by = relationship('User', foreign_keys=followed_by_id, backref='follows')

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.followed_by_id} to {self.user_id}>'.format(self=self)
