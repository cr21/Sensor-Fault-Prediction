from setuptools import find_packages, setup

from setuptools import setup, find_packages
from typing import List

# Declaring variables for setup functions
PROJECT_NAME = "sensor"
VERSION = "0.0.3"
AUTHOR = "Chirag Tagadiya"
AUTHOR_EMAIL = "cr.tagadiya@gmail.com"
DESRCIPTION = "Project for APS system monitoring"

REQUIREMENT_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = "-e ."

def get_all_requirement_list() -> List[str]:
    """
    Get All Requirements from reading from requirements.txt


    :return: List of requirements
    :rtype: List[str]
    """

    with open(REQUIREMENT_FILE_NAME) as req_files:
        all_raw_requirements = req_files.readlines()
        all_raw_requirements = [req_name.replace("\n", "") for req_name in all_raw_requirements]

        if HYPHEN_E_DOT in all_raw_requirements:
            all_raw_requirements.remove(HYPHEN_E_DOT)

        return all_raw_requirements


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESRCIPTION,
    packages=find_packages(),
    install_requires= get_all_requirement_list()
)


