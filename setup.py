from setuptools import setup, find_packages

setup(
    name='HackCommerce',
    version='0.0.1',
    python_requires='>=2.7, <3',
    packages=find_packages(),
    tests_require=['pytest==3.0.3'],
    install_requires=['pymongo==3.6.1',
                      'Flask==0.12.2',
                      'flask_cors==3.0.3',
                      'requests==2.18.4']

)
