from flask_script import Manager, Server
from webapp.app import create_app

app = create_app()
manager = Manager(app)

manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    """
    Makes it possible to run the python shell
    python manage.py shell
    """
    return dict(app=app)


if __name__ == '__main__':
    """
    Call with:
    python manage.py server
    """
    manager.run()
