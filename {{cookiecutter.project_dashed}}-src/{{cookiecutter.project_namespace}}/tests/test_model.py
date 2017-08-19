import pytest
from sqlalchemy.exc import IntegrityError

from {{cookiecutter.project_namespace}}.libs.testing import ModelBase
import {{cookiecutter.project_namespace}}.model.entities as ents


class TestBlog(ModelBase):
    orm_cls = ents.Blog
    constraint_tests = [
        # column name, is FK?, is required?
        ('title', False, True),
        ('posted_utc', False, True),
    ]


class TestComment(ModelBase):
    orm_cls = ents.Comment
    constraint_tests = [
        # column name, is FK?, is required?
        ('blog_id', True, True),
        ('author_name', False, True),
        ('author_email', False, False),
        ('comment', False, True),
    ]

    def test_unique_author(self):
        blog = ents.Blog.testing_create()
        ents.Comment.testing_create(blog=blog, author_name='foo')
        with pytest.raises(IntegrityError) as excinfo:
            ents.Comment.testing_create(blog=blog, author_name='foo')
        assert 'violates unique constraint "uc_comments_unique_author"' in str(excinfo.value)


class TestUser(ModelBase):
    orm_cls = ents.User
    constraint_tests = [
        # column name, is FK?, is required?
        ('is_verified', False, True),
        ('is_enabled', False, True),
        ('email', False, True),
        ('password', False, True),
        ('token', False, False),
        ('token_created_utc', False, False),
        ('name', False, True),
    ]
