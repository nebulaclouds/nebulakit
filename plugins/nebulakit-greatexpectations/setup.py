from setuptools import setup

PLUGIN_NAME = "great_expectations"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = [
    "nebulakit",
    "nebulakitplugins-spark",
    "great-expectations>=0.13.30",
    "sqlalchemy>=1.4.23,<2.0.0",
    "pyspark==3.3.1",
    "s3fs<2023.6.0",
]

__version__ = "1.0.0"

setup(
    name=microlib_name,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="Great Expectations Plugin for Nebulakit",
    namespace_packages=["nebulakitplugins"],
    packages=[f"nebulakitplugins.{PLUGIN_NAME}"],
    install_requires=plugin_requires,
    license="apache2",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
