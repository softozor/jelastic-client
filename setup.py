import setuptools

setuptools.setup(
    name="jelastic_client",
    version="0.0.1",
    author="Laurent Michel",
    author_email="softozor@gmail.com",
    description="A jelastic client library to be used in the softozor projects",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)