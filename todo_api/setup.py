from setuptools import setup

setup(
    name='todo_api',
    version='0.3',
    packages=['todo_api'],
    url='https://github.com/Gosha20/tinloff/tree/master/todo_api',
    author='gosha',
    author_email='gosha3548@gmail.com',
    install_requires=['flask', 'flask_sqlalchemy', 'pytz', 'flask_httpauth']
)