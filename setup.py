from setuptools import setup


setup(
    name='tksqla',
    version='0.1',
    description='A bunch of tests for Tk and SQLAlchemy',
    author='Ryan Jackson',
    packages=['tksqla'],
    install_requires=['sqlalchemy', 'alembic']
)
