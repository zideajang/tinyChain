from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here,"README.md"),encoding='utf-8') as f:
    long_description = f.read()

# with open(path.join(here,"requirements.txt"),encoding='utf-8') as f:
#     requirements = [line.strip() for line in f if line]

setup(
    name='tinychain',
    version='1.0.0',
    author='zidea',
    author_email='',
    description='A tiny agent based on LLM framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="agentframework muliti-agents llm",
    url="https://github.com/zideajang/tinyChain",
    # install_requires=requirements,
    packages=find_packages(exclude=["examples","docs","data"]),
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "tinychain=tinychain.cli:app",
        ],
    },
)