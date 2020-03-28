import setuptools

with open('README.rst', 'r') as fh:
    readme = fh.read()

with open('HISTORY.rst', 'r') as f:
    history = f.read()


requires = [
    'requests>=2.20.0',
    'token-bucket>=0.2.0'
]

setuptools.setup(
    name='pytau',
    version='0.0.1',
    description='A Python functional reactive framework.',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    license='MIT',
    author='Kyle F. Downey',
    author_email='kyle.downey@gmail.com',
    url='https://github.com/cloudwall/pytau',
    packages=setuptools.find_packages(),
    python_requires='>=3.7.x',
    install_requires=requires,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ),
)
