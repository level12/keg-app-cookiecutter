import logging

from keg.db import db
from keg_elements.db.mixins import DefaultColsMixin, MethodsMixin
from keg_auth import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as saorm
from sqlalchemy_utils import ArrowType, EmailType


log = logging.getLogger(__name__)

# Default cascade setting for parent/child relationships.  Should get set on parent side.
# More info: https://level12.atlassian.net/wiki/spaces/devs/blog/2015/06/17/14286861/Proper+Configuration+of+SQLAlchemy+Parent+Child+Relationships  # noqa
_rel_cascade = 'all, delete-orphan'


class EntityMixin(DefaultColsMixin, MethodsMixin):
    pass


class Blog(db.Model, EntityMixin):
    __tablename__ = 'blogs'

    title = sa.Column(sa.Unicode(250), nullable=False, unique=True)
    posted_utc = sa.Column(ArrowType, nullable=False)

    comments = saorm.relationship('Comment', cascade=_rel_cascade, passive_deletes=True,
                                  foreign_keys='Comment.blog_id')


class Comment(db.Model, EntityMixin):
    __tablename__ = 'comments'
    __table_args__ = (
        sa.UniqueConstraint('blog_id', 'author_name', name='uc_comments_unique_author'),
    )

    # FK and parent relationship
    blog_id = sa.Column(sa.ForeignKey(Blog.id, ondelete='cascade'), nullable=False)
    blog = saorm.relationship(Blog, foreign_keys=blog_id)

    author_name = sa.Column(sa.Unicode(250), nullable=False)
    author_email = sa.Column(EmailType)
    comment = sa.Column(sa.Unicode, nullable=False)

    @classmethod
    def testing_create(cls, **kwargs):
        if 'blog' not in kwargs and 'blog_id' not in kwargs:
            kwargs['blog'] = Blog.testing_create(_commit=False)
        return super().testing_create(**kwargs)


class User(db.Model, UserMixin, EntityMixin):
    """ Make sure EntityMixin is after UserMixin or testing_create() is wrong.  """
    __tablename__ = 'users'

    name = sa.Column(sa.Unicode(250), nullable=False)