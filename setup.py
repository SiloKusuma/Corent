from setuptools import setup, find_packages

setup(
    name="corent",
    version="1.0.0",
    description="Auto-Discussion AI Builder — Synthetic Data Generation",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "corent=main:main",
        ],
    },
    python_requires=">=3.8",
)
