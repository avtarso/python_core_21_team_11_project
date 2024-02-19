from setuptools import setup, find_namespace_packages

setup(
    name='personal_assistant',
    version='0.0.7',
    packages=find_namespace_packages(),
    license='MIT License',
    #include_package_data=True,
    entry_points={'console_scripts': ['pa=personal_assistant.main:main']},
    url='https://github.com/avtarso/python_core_21_team_11_project/',
    author='Avtarso',
    author_email='t0676352927@gmail.com',
    description='Command line bot personal assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 