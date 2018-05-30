from {{cookiecutter.project_namespace}}.extensions import mail as mail_ext
from {{cookiecutter.project_namespace}}.libs import mail


class TestMail(object):

    def test_hello_compose(self):

        message = mail.HelloMail.compose('Bob', 'bob@example.com')

        assert message.subject == '[{{cookiecutter.project_name}}] Hello There!'
        assert message.recipients == ['bob@example.com']
        assert 'Hello *Bob*!' in message.body
        assert 'Hello <em>Bob</em>!' in message.html

    def test_hello_send(self):
        with mail_ext.record_messages() as outbox:
            mail.HelloMail.send('Bob', 'bob@example.com')

            assert len(outbox) == 1
        assert outbox[0].subject == '[{{cookiecutter.project_name}}] Hello There!'
