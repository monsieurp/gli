from cx_Freeze import Executable
from cx_Freeze import setup

setup(
    name = "gli",
    version = "0.1",
    description = "GLI - Gentoo Linux Installer",
    executables = [Executable("gli.py")],
)
