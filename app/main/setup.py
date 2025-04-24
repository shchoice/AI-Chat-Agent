from setuptools import setup, find_packages

setup(
    name="ai_agent",  # 프로젝트 이름
    version="0.1.0",
    author="Seohwan Choi",
    author_email="shchoice7140@gmail.com",
    description="AI Agent system using FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shchoice/AI-Chat-Agent",  # Optional
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.11,<3.12",
    install_requires=[
        "fastapi>=0.115.0,<1.0.0",
        "uvicorn>=0.34.0,<1.0.0",
        "PyYAML>=6.0.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
