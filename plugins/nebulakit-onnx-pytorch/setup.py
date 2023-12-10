from setuptools import setup

PLUGIN_NAME = "onnxpytorch"

microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"

plugin_requires = ["nebulakit>=1.3.0b2,<2.0.0", "torch>=1.11.0", "onnx-pytorch", "networkx<3.2; python_version<'3.9'"]

__version__ = "0.0.0+develop"

setup(
    name=f"nebulakitplugins-{PLUGIN_NAME}",
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="ONNX PyTorch Plugin for Nebulakit",
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
