from setuptools import setup

setup(
    name='iris-xforce-module',
    python_requires='>=3.9',
    version='0.1.0',
    packages=['iris_xforce_module', 'iris_xforce_module.xforce_handler'],
    url='https://github.com/iris_xforce_module/iris-xforce-module',
    license='GNU GPL v3.0',
    author='iris-xforce-module',
    author_email='hello@cydea.tech',
    description='`iris-xforce-module` is a IRIS pipeline/processor module created with https://github.com/dfir-iris/iris-skeleton-module',
    install_requires=[]
)
