from setuptools import setup, find_packages

setup(
    name="process",
    packages=find_packages(),
    entry_points={"console_scripts": ["process = process.__main__:main"]},
)
