from setuptools import setup

PLUGIN_NAME = "whylogs"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = ["nebulakit>=1.3.0b2,<2.0.0", "whylogs[viz]>=1.1.16"]

__version__ = "0.0.0+develop"

setup(
    name=microlib_name,
    version=__version__,
    author="whylabs",
    author_email="support@whylabs.ai",
    description="Enable the use of whylogs profiles to be used in nebula tasks to get aggregate statistics about data.",
    url="https://github.com/nebulaclouds/nebulakit/tree/master/plugins/nebulakit-whylogs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
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
