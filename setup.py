from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    description="A maze generation and visualization library",
    author="fathe4wiin & aidbrm",
    packages=find_packages(),
    install_requires=[
        "mlx",
    ],
    python_requires=">=3.8",
)
