# coding: utf-8

from __future__ import unicode_literals, print_function

from flask_api_app.manage import Manager
from flask_migrate import MigrateCommand, Migrate
from flask_script import Server
from flask_script.commands import Shell, ShowUrls

from todayiate import create_app
from todayiate.database import db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


# Turn on debugger by default and reloader
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True,
                                        host='0.0.0.0'))

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('show_urls', ShowUrls)

# extra commands
# from influence.core.accounts.commands import *
# from influence.modules.media.commands import *

import flask_api_app.core.accounts.commands

if __name__ == "__main__":
    manager.run()
