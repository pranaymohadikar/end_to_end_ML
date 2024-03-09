#responsible to create an app as a package

from setuptools import find_packages, setup
from typing import List

HYPHEN = "-e ."
def get_requirements(file_path:str)->List[str]:
    '''
        function will return the list of libraries     
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

        if HYPHEN in requirements:
            requirements.remove(HYPHEN)
    
    return requirements


setup(
    name='end to end project',
    version='0.0.1',
    author='pranay',
    author_email='pmohadikar.94@gmail.com',
    packages=find_packages(),   #whereever __init__.py file present considerend as a package
    install_requires=get_requirements('requirements.txt'),
)