from setuptools import setup

des = "Haskell language features and standard library ported to Python"
setup(
    name='hask3',
    version='0.2.0',
    description=des,
    long_description=open('README.rst').read(),
    author='Merchise Autrement',
    author_email='med@merchise.org',
    url='https://gitlab.merchise.org/merchise/hask',
    packages=['hask3', 'hask3.lang', 'hask3.Python', 'hask3.Data',
              'hask3.Control'],
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'xoutil>=1.9.4',
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
