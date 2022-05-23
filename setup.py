import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='atomsk',
    version='0.0.1',
    author='Théo Bequet',
    author_email='theo.bequet@etu.univ-poitiers.fr',
    description='Toolbox for atomistic simulation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/theobqt/python_toolbox',
    project_urls = {
        "Bug Tracker": "https://github.com/theobqt/python_toolbox/issues"
    },
    license='',
    packages=['atomsk'],
    install_requires=['requests'],
)