from setuptools import setup

PLUGIN_NAME = "vaex"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

# vaex doesn't support pydantic 2.0 yet. https://github.com/vaexio/vaex/issues/2384
plugin_requires = [
    "nebulakit",
    "vaex-core>=4.13.0,<4.14; python_version < '3.10'",
    "vaex-core>=4.16.0; python_version >= '3.10'",
    "pydantic<2.0",
]

__version__ = "1.0.0"

setup(
    name=microlib_name,
    version=__version__,
    author="admin@nebula.org",
    description="Vaex plugin for nebulakit",
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
