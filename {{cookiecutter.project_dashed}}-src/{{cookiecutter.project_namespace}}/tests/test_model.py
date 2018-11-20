from keg_elements.testing import (
    ColumnCheck,
    EntityBase,
)
import pytest
from sqlalchemy.exc import IntegrityError

import {{cookiecutter.project_namespace}}.model.entities as ents


class TestBlog(EntityBase):
    entity_cls = ents.Blog
    column_checks = [
        ColumnCheck('title', unique=True),
        ColumnCheck('posted_utc'),
    ]


class TestComment(EntityBase):
    entity_cls = ents.Comment
    column_checks = [
        ColumnCheck('blog_id', fk='blogs.id'),
        ColumnCheck('author_name'),
        ColumnCheck('author_email', required=False),
        ColumnCheck('comment'),
    ]

    def test_unique_author(self):
        blog = ents.Blog.testing_create()
        ents.Comment.testing_create(blog=blog, author_name='foo')
        with pytest.raises(IntegrityError) as excinfo:
            ents.Comment.testing_create(blog=blog, author_name='foo')

        # postgresql
        assert 'violates unique constraint "uc_comments_unique_author"' in str(excinfo.value) \
            or 'UNIQUE constraint failed' in str(excinfo.value)


class TestUser(EntityBase):
    entity_cls = ents.User
    column_checks = [
        ColumnCheck('is_verified'),
        ColumnCheck('is_enabled'),
        ColumnCheck('is_superuser'),
        ColumnCheck('session_key', unique=True),
        ColumnCheck('email', unique=True),
        ColumnCheck('password', required=False),
        ColumnCheck('name'),
        ColumnCheck('settings', required=False),
        ColumnCheck('last_login_utc', required=False),
    ]
