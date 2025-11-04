from setuptools import setup, find_packages

setup(
    name="taskaty",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "tabulate",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "taskaty=taskaty.code:main"
        ]
    }
)
