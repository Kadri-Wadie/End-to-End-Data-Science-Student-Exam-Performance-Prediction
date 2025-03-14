"""
Package configuration file for distributing the Student Exam Performance Prediction project.
Enables pip installation of the project and management of dependencies.
"""

from setuptools import find_packages, setup
from typing import List

# Constant to handle editable installation flag ("-e .") in requirements
# Note: Currently empty string, might need to be set to "-e ." if used in requirements
HYPEN_E_DOT = ''

def get_requirements(file_path: str) -> List[str]:
    """
    Reads requirements from a file and processes them for package installation.
    
    Args:
        file_path (str): Path to requirements file
        
    Returns:
        List[str]: Cleaned list of required packages
        
    Note:
        - Removes newline characters from each requirement
        - Filters out empty strings (if HYPEN_E_DOT is properly configured)
    """
    requirements = []
    
    with open(file_path) as file_obj:
        # Read all lines and remove newline characters
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        
        # Remove any occurrence of HYPEN_E_DOT (typically "-e ." for editable install)
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

# Package configuration using setuptools
setup(
    name='End-to-End-Data-Science-Student-Exam-Performance-Prediction',
    version='0.01',
    author='Wadie',
    author_email='kdata.sc@gmail.com',
    # Automatically discover all packages in the project
    packages=find_packages(),
    # Install dependencies from requirements file
    install_requires=get_requirements('requirements.txt')
)