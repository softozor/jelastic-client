import setuptools

install_requires = ["httpx[http2]>=0.18"]
test_requires = [
    "pytest",
]

setuptools.setup(
    name="jelastic_client",
    version="0.0.2",
    author="Laurent Michel",
    author_email="softozor@gmail.com",
    description="A jelastic client library to be used in the softozor projects",
    url="https://gitlab.hidora.com/softozor/jelastic-client",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    extras_require={
        "test": test_requires,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
