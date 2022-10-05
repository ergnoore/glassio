from setuptools import find_packages
from setuptools import setup


install_requires = [
    "aioamqp==0.15.0",
    "pydantic==1.9.0",
    "ujson==5.2.0",
]


test_requires = [
    *install_requires,
    "pytest==7.1.1",
    "pytest-asyncio==0.18.3",
]


setup(
    name='glassio',
    version='0.0.6',
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=install_requires,
    tests_require=test_requires,
    url='https://github.com/ergnoore/glassio',
    license='MIT',
    author='Aleksandr Filippov',
    author_email='alexneonium@gmail.com',
    description='Framework for developing microservices on Python.'
)
