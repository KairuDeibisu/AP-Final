from setuptools import setup

setup(
    name="Note",
    version="1.0",
    py_modules=["Note", "tests"],
    install_requires=[
        "typer",
        "python-dotenv",
        "Sphinx",
        "sphinx-rtd-theme",
        "sqlalchemy",
        "Faker"
    ],
    entry_points="""
        [console_scripts]
        Note=Note.cli.__main__:app
    """,
)
