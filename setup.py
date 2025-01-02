from setuptools import setup, find_packages

setup(
    name='my_django_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
    ],
    license='MIT',
    description='A Django app for XYZ functionality.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_django_app',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
