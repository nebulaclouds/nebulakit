from setuptools import setup

PLUGIN_NAME = "dask"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = [
    "nebulaidl",
    "nebulakit",
    "dask[distributed]>=2022.10.2",
]

__version__ = "1.0.0"

setup(
    name=microlib_name,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="Dask plugin for nebulakit",
    url="https://github.com/nebulaclouds/nebulakit/tree/master/plugins/nebulakit-dask",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    namespace_packages=["nebulakitplugins"],
    packages=[f"nebulakitplugins.{PLUGIN_NAME}"],
    install_requires=plugin_requires,
    license="apache2",
    python_requires=">=3.8",  # dask requires >= 3.8
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
