from setuptools import setup, find_packages, Extension

extensions = [
    # The MBTR C++ extension, wrapped with cython
    Extension(
        "test.libmbtr.cmbtrwrapper",
        [
            "test/libmbtr/cmbtrwrapper.cpp",
        ],
        include_dirs=["test/libmbtr"],
        extra_compile_args=['-std=c++11'],
    ),
]

if __name__ == "__main__":
    setup(name='test',
        version='0.1.0',
        url="https://singroup.github.io/dscribe/",
        description='A Python package for creating feature transformations in applications of machine learning to materials science.',
        long_description='A Python package for creating feature transformations in applications of machine learning to materials science.',
        packages=find_packages(),
        install_requires=[
        ],
        include_package_data=True,  # This ensures that files defined in MANIFEST.in are included
        ext_modules=extensions,
        license="Apache License 2.0",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Physics',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        keywords='descriptor machine learning atomistic structure materials science',
        python_requires='>=2.6, <4',
    )
