from setuptools import setup

PLUGIN_NAME = "polars"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = [
    "nebulakit",
    "polars>=0.8.27,<0.17.0",
]

__version__ = "1.0.0"

setup(
    name=microlib_name,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="Polars plugin for nebulakit",
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
    entry_points={"nebulakit.plugins": [f"{PLUGIN_NAME}=nebulakitplugins.{PLUGIN_NAME}"]},
)
