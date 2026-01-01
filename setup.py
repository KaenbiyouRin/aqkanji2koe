from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aqkanji2koe",
    version="0.1.0",
    author="KaenbiyouRin",
    description="Python wrapper for AquesTalk AqKanji2Koe library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aqkanji2koe",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[],
    project_urls={
        "Source": "https://github.com/yourusername/aqkanji2koe",
    },
)