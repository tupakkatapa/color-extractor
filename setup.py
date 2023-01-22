from setuptools import setup
setup(
    name = 'color_extractor',
    version = '0.1.0',
    description = 'Simple command-line tool for extracting colors from image',
    author = 'tupakkatapa',
    packages = ['color_extractor'],
    entry_points = {
        'console_scripts': [
            'color-extractor = color_extractor.__main__:main' ]},
    python_requires = '>= 3.10.9',
    install_requires = [
        'codetiming >= 1.4.0',
        'numpy >= 1.24.1',
        'Pillow >= 9.4.0',
        'pyTextColor >= 1.0.1',
        'scipy >= 1.10.0',
    ]
)
