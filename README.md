# Dune II — The Maker RU/HD Remaster

Hi everyone! I made a small remaster of the game. I did not change any of the mechanics; I simply updated the visuals, added support for high-resolution displays, refreshed the music while avoiding copyright infringement, and redesigned the interface.

The entire project was created with the help of Codex and Suno. I made it for my father, who has been playing Dune for almost his entire life. I originally had no plans to release it online, but a friend of mine, after seeing the results, strongly encouraged me to do so. And here we are.

## Downloads

Ready-to-run builds are published on the [GitHub Releases page](https://github.com/PavelSlaven/DUNE/releases) for Windows x64, Linux x64, macOS Apple Silicon and macOS Intel.

Download the `common-assets` archive and one archive for your operating system, then extract both into the same folder. Platform-specific requirements are included in each archive.

The Russian interface uses **Sangyo Regular** by GGBotNet. The font is
distributed under the SIL Open Font License 1.1; its supplied copyright and
license notices are included in [`resources/bin/data/licenses`](resources/bin/data/licenses).

---

Dune II - The Maker
===================
A.k.a. D2TM. Is a [Dune 2](http://en.wikipedia.org/wiki/Dune_II) remake.

> **AI agents and maintainers of the local RU/HD build:** start with
> [`README_AI.md`](README_AI.md). It documents the actual architecture,
> toolchain, runtime layout, tests, resources, and safe change workflow.

[![Latest](https://img.shields.io/github/downloads/stefanhendriks/Dune-II---The-Maker/latest/total)]()
[![All](https://img.shields.io/github/downloads/stefanhendriks/Dune-II---The-Maker/total.svg)]()
[![Build & Release](https://github.com/stefanhendriks/Dune-II---The-Maker/actions/workflows/build_master.yml/badge.svg)](https://github.com/stefanhendriks/Dune-II---The-Maker/actions/workflows/build_master.yml)
<span class="badge-buymeacoffee">
<a href="https://ko-fi.com/dune2themaker" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a>
</span>

![GitHub repo size](https://img.shields.io/github/repo-size/stefanhendriks/Dune-II---The-Maker?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/stefanhendriks/Dune-II---The-Maker?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/stefanhendriks/Dune-II---The-Maker?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/stefanhendriks/Dune-II---The-Maker?color=red&style=plastic)

This project uses [Deleaker](https://www.deleaker.com/) to find memory leaks and more.

- Website: [https://dune2themaker.fundynamic.com](https://dune2themaker.fundynamic.com)
- Discord: [https://dune2themaker.fundynamic.com/discord](https://dune2themaker.fundynamic.com/discord)
- Twitter: [https://twitter.com/dune2themaker](https://twitter.com/dune2themaker)

Report bugs via Discord, Twitter or add one in Github.

Read [the wiki](https://github.com/stefanhendriks/Dune-II---The-Maker/wiki) for more information about startup params, controls, and more.

## Compiling

### Prerequisites
- `CMake` version 3.21 or higher
- `GCC` version 11 or higher

Make sure you can run `make` (or `ninja`) from command line.

### Windows (MinGW)
It currently depends on MinGW32. Make sure you also have GCC 11 installed,
which you can do via MSYS2 (using `pacman`). GCC 11 is not installed by
default in MinGW32!

- git clone this project
- create a `build` dir
```
    mkdir build
    cd build
    cmake .. -G "MinGW Makefiles"
    cmake --build . --target all -- -j 6
```

If you use `ninja` you can use `cmake .. -G Ninja` instead.

Once compilation is done you'll end up with a `d2tm.exe` file and several DLL's.

### Ubuntu
- git clone this project
- run `./install_dependencies_ubuntu.sh` (only required once)
- create a `build` dir
```
    mkdir build
    cd build
    cmake ..
    make -j4
```

### MacOS
- git clone this project
- run `./install_dependencies_macosx.sh` (only required once)
- create a `build` dir
```
    mkdir build
    cd build
    cmake ..
    make -j4
```

### Clion
#### Mac OS
Make sure you set up your toolchain to use `gcc-15` and `g++-15`. Ie, change your default toolchain
OR create a new one (and make sure CMake points to that one), with the following values:

| Field        | Value                    |
|--------------|--------------------------|
| C-Compiler   | /opt/homebrew/bin/gcc-15 |
| C++-Compiler | /opt/homebrew/bin/g++-15 |

Then make sure to (re)load `CmakeLists.txt`

## Running
Easiest is to run the executable from the root. Shared libraries that are required are: libalfont.dll, alleg42.dll, libwinpthread-1.dll and mscvr70.dll.
The required pre-built library (Allegro 4) is in the [dll folder](https://github.com/stefanhendriks/Dune-II---The-Maker/tree/master/dll/mingw32).
The library that is built with the project (AlFont) is copied to the build directory.
libwinpthread-1.dll Could be on your MinGW path. If it is not on the path, copy it from your mingw32 installation.

## Project status
See the [Project Board](https://github.com/stefanhendriks/Dune-II---The-Maker/projects/1) what's going on.

## Binaries
You have various options:
- Grab the [latest release from Github](https://github.com/stefanhendriks/Dune-II---The-Maker/releases)
- Grab a version from [D2TM's homepage](https://www.dune2themaker.com)
- Compile this project yourself

## Topics
In the code there are several known concepts; see below for extra information
about them:

- [Angles: how to calculate and use them to draw things](resources/doc/convertAngleToDrawIndex.md)
