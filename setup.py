from setuptools import find_packages, setup
from typing import List

HYPEN_e_DOT='-e .'
def get_reuqirements(filepath:str)->List[str]:
    '''
    This function will return the list of requirements

    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n"," ") for req in requirements]
        
        if HYPEN_e_DOT in requirements:
            requirements.remove('HYPEN_e_DOT')

    return requirements


setup(
name='
End-to-End-Data-Science-Student-Exam-Performance-Prediction',
version='0.1',
author='Wadie',
author_email='dir.gfe@gmail.com',
packages=findpackages(),
install_requires=get_requirements('requirements.txt')



)