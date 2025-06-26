from setuptools import setup,find_packages
from typing import List

def get_requirements(file_path:str)->List[str]:
    requires = []
    dot_E = "-e ."
    with open(file_path) as file_obj:
        requires = file_obj.readlines()
        requires = [req.replace("\n","") for req in requires]

    if dot_E in requires:
        requires.remove(dot_E)

setup(
    name="Breast Cancer Ml Project",
    version="0.0.1",
    author="Naseeb Ali",
    author_email="mirzanaseebali327@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements("requirements.txt")
)