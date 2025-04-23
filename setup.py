from setuptools import setup, find_packages

setup(
    name="supercash",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PySide6>=6.5.0',
        'psycopg2-binary>=2.9.7',
        'python-dotenv>=1.0.0',
        'qt-material>=2.14',
        'pandas>=2.0.0',
        'openpyxl>=3.1.2',
        'reportlab>=4.0.4',
        'qrcode>=7.4.2',
        'pillow>=9.5.0',
        'passlib>=1.7.4',
        'psutil>=5.9.5',
        'pyinstaller>=5.10.1',
        'PyUpdater>=4.0',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2'
    ],
    entry_points={
        'console_scripts': [
            'supercash=supercash.main:main',
        ],
    },
    package_data={
        'supercash': ['ui/*.ui', 'assets/*'],
    },
    python_requires='>=3.8',
    author='Widley Mayk Santos Silva',
    description='A modern POS system for pet shops',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='pos, petshop, retail, management',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
)