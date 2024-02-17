from setuptools import setup, find_packages

setup(
    name='personal_assistant',
    version='1.0.0',
    packages=find_packages(),
    license='MIT License',
    entry_points={
        'console_scripts': [
            'personal-assistant=main:main',
            'notes=notes:main',
        ],
    },
    url='https://github.com/avtarso/python_core_21_team_11_project/tree/main',
    author='',
    author_email='',
    description='Command line bot personal assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

) 