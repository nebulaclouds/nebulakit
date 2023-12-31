import pip
from setuptools import setup
from setuptools.command.develop import develop

PLUGIN_NAME = "dolt"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = ["nebulakit", "dolt_integrations>=0.1.5", "networkx<3.2; python_version<'3.9'"]
dev_requires = ["pytest-mock>=3.6.1"]

__version__ = "1.0.0"


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        pip.main(["install"] + dev_requires)


setup(
    name=microlib_name,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="Dolt plugin for nebulakit",
    namespace_packages=["nebulakitplugins"],
    packages=[f"nebulakitplugins.{PLUGIN_NAME}"],
    install_requires=plugin_requires,
    extras_resquire=dict(
        dev=dev_requires,
    ),
    cmdclass=dict(develop=PostDevelopCommand),
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
    scripts=["scripts/nebulakit_install_dolt.sh"],
)
