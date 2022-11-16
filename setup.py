from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """_summary_

    Returns:
        List[str]: This function returns a list of requirements from requirements.txt file
    """

    requirements_list:List[str] = []
    return requirements_list

setup(
    name = "sensor",
    version = "0.0.1",
    author = "gomathi",
    author_email = "gomathi.murugesan33@gmail.com",
    packages = find_packages(), ##search for the packages in our project folder
    #install_requires =["pymongo==4.2.0"], updating manually to include all the dependencies from that we gave in requirements.txt
    install_requires = get_requirements()
)