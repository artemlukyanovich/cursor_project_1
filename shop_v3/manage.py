# from app import app, db
# from app.models import Users
from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app

manager = Manager(create_app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': Users}

