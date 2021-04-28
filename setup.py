from setuptools import setup

setup(
    name="Note",
    version="1.0",
    py_modules=["Note"],
    install_requires=[
        "typer",
        "sqlalchemy",
    ],
    entry_points="""
        [console_scripts]
        Note=Note.cli.__main__:app
    """,
    python_version="3.9"
)
