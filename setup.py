from setuptools import setup

readme = open('README.md').read()

setup(
    name="CDN",
    version="0.0.1",
    description="Implementations of Causal Dynamic Network Analysis of fMRI",
    author="Xuefei Cao, Xi Luo, Björn Sandstede",
    author_email="xcstf01@gmail.com",
    packages=['CDN'],
    long_description=readme,
    install_requires=[
        "matplotlib==1.5.3",
        "numpy==1.11.1",
    ],
    url='https://github.com/xuefeicao/CDN',
    )
