# conan-g3log

Conan package for [g3log](https://github.com/KjellKod/g3log)

The packages generated with this **conanfile** can be found on [bintray](https://bintray.com/conan-community).

## Package Status

| Bintray | Travis | Appveyor |
|---------|--------|----------|
|[![Download](https://api.bintray.com/packages/zimmerk/conan/g3log%3Azimmerk/images/download.svg) ](https://bintray.com/zimmerk/conan/g3log%3Azimmerk/_latestVersion)|[![Build Status](https://travis-ci.org/AtaLuZiK/conan-g3log.svg?branch=release%2F1.3.2.65)](https://travis-ci.org/AtaLuZiK/conan-g3log)|[![Build status](https://ci.appveyor.com/api/projects/status/cudam66ksvjdfmye/branch/release/1.3.2.65?svg=true)](https://ci.appveyor.com/project/AtaLuZiK/conan-g3log/branch/release/1.3.2.65)|

## Reuse the packages

### Basic setup

```
conan install g3log/1.3.2.65@zimmerk/stable
```

### Project setup

```
[requires]
g3log/1.3.2.65@zimmerk/stable

[options]
g3log::shared=True
# Take a look for all avaliable options in conanfile.py

[generators]
cmake
```

Complete the installitation of requirements for your project running:

```
conan install .
```

Project setup installs the library (and all his dependencies) and generates the files conanbuildinfo.txt and conanbuildinfo.cmake with all the paths and variables that you need to link with your dependencies.

Follow the Conan getting started: http://docs.conan.io
