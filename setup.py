import os
import subprocess
import sys

import setuptools
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py


def _find_libgraphqlparser_artifact():
    if os.path.exists("./libgraphqlparser/libgraphqlparser.so"):
        return "./libgraphqlparser/libgraphqlparser.so"

    if os.path.exists("./libgraphqlparser/libgraphqlparser.dylib"):
        return "./libgraphqlparser/libgraphqlparser.dylib"

    return None


def _build_libgraphqlparser():
    os.chdir("./libgraphqlparser/.")
    subprocess.run(["cmake", "."], stdout=subprocess.PIPE)
    subprocess.run(["make"], stdout=subprocess.PIPE)
    os.chdir("..")

    artifact_path = _find_libgraphqlparser_artifact()

    if not artifact_path:
        print("Libgraphqlparser compilation has failed")
        sys.exit(-1)

    os.rename(
        artifact_path,
        "tartiflette/language/parsers/libgraphqlparser/cffi/%s"
        % os.path.basename(artifact_path),
    )


class BuildExtCmd(build_ext):
    def run(self):
        _build_libgraphqlparser()
        # build_ext.run(self)


class BuildPyCmd(build_py):
    def run(self):
        _build_libgraphqlparser()
        # build_py.run(self)


_TEST_REQUIRE = [
    "pytest==5.3.0",
    "pytest-cov==2.8.1",
    "pytest-asyncio==0.10.0",
    "pytest-xdist==1.30.0",
    "pylint==2.4.4",
    "black==19.10b0",
    "isort==4.3.21",
]

_BENCHMARK_REQUIRE = ["pytest-benchmark==3.2.2"]

_VERSION = "1.1.4"

_PACKAGES = find_packages(exclude=["tests*"])


def _read_file(filename):
    with open(filename) as afile:
        return afile.read()


setup(
    name="tartiflette-test-with-wheels",
    version=_VERSION,
    description="GraphQL Engine for Python",
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/tartiflette/tartiflette",
    author="Dailymotion Core API Team",
    author_email="team@tartiflette.io",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="api graphql protocol api rest relay tartiflette dailymotion",
    packages=_PACKAGES,
    install_requires=["cffi>=1.0.0,<2.0.0", "lark-parser==0.7.8", "pytz"],
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE, "benchmark": _BENCHMARK_REQUIRE},
    cmdclass={"build_ext": BuildExtCmd, "build_py": BuildPyCmd},
    include_package_data=True,
    ext_modules=[
        # force the creation of platform specific wheels
        setuptools.Extension(name="libgraphqlparser", sources=[])
    ],
)
