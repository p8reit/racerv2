from setuptools import setup, find_packages

setup(
    name='racerv2',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'Pillow',
        
    ],
    license='MIT',
    description='Racer AA Auth Feature',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/p8reit/racerv2',
    author='p8reit',
    author_email='p8reit@yahoo.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
