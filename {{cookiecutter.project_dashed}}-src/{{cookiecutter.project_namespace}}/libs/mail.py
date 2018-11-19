from collections import namedtuple

from blazeutils.strings import normalizews
import commonmark
import flask
import flask_mail

from {{cookiecutter.project_namespace}}.extensions import mail as mail_ext

MailParts = namedtuple('MailParts', 'subject text html')


def mail_template(template_name_or_list, **kwargs):
    multi_part_content = flask.render_template(template_name_or_list, **kwargs)
    parts = multi_part_content.split('---multi-part:xFE+Ab7j+w,mdIL%---')
    subject, markdown = map(lambda p: p.strip(), parts)

    return MailParts(
        normalizews(subject),
        markdown,
        commonmark.commonmark(markdown)
    )


class HelloMail:

    @classmethod
    def compose(cls, to_name, to_email):
        parts = mail_template('mail/hello.j2', name=to_name)

        return flask_mail.Message(parts.subject, [to_email], parts.text, parts.html)

    @classmethod
    def send(cls, to_name, to_email):
        msg = cls.compose(to_name, to_email)
        mail_ext.send(msg)
