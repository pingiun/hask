from setuptools import setup

des = "Haskell language features and standard library ported to Python"
setup(
    name='hask3',
    version='0.1.1',
    description=des,
    long_description=open('README.rst').read(),
    author='Bill Murphy',
    author_email='billpmurphy92@gmail.com',
    url='https://github.com/billpmurphy/hask',
    packages=['hask', 'hask.lang', 'hask.Python', 'hask.Data',
              'hask.Control'],
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    install_requires=[
        'xoutil>=1.9.4,<2',
    ],
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ),
)
