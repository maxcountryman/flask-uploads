"""Extension presets and extension configuration."""
import os
from typing import Iterable

# This contains archive and compression formats (.gz, .bz2, .zip, .tar,
# .tgz, .txz, and .7z).
ARCHIVES = tuple('gz bz2 zip tar tgz txz 7z'.split())


# This contains audio file types (.wav, .mp3, .aac, .ogg, .oga, and .flac).
AUDIO = tuple('wav mp3 aac ogg oga flac'.split())

# This is for structured data files (.csv, .ini, .json, .plist, .xml, .yaml,
# and .yml).
DATA = tuple('csv ini json plist xml yaml yml'.split())

# This contains various office document formats (.rtf, .odf, .ods, .gnumeric,
# .abw, .doc, .docx, .xls, .xlsx and .pdf). Note that the macro-enabled
# versions of Microsoft Office 2007 files are not included.
DOCUMENTS = tuple('rtf odf ods gnumeric abw doc docx xls xlsx pdf'.split())

# This contains shared libraries and executable files (.so, .exe and .dll).
# Most of the time, you will not want to allow this - it's better suited for
# use with `AllExcept`.
EXECUTABLES = tuple('so exe dll'.split())

# This contains basic image types that are viewable from most browsers (.jpg,
# .jpe, .jpeg, .png, .gif, .svg, .bmp and .webp).
IMAGES = tuple('jpg jpe jpeg png gif svg bmp webp'.split())

# This contains various types of scripts (.js, .php, .pl, .py .rb, and .sh).
# If your Web server has PHP installed and set to auto-run, you might want to
# add ``php`` to the DENY setting.
SCRIPTS = tuple('js php pl py rb sh'.split())

# This contains nonexecutable source files - those which need to be
# compiled or assembled to binaries to be used. They are generally safe to
# accept, as without an existing RCE vulnerability, they cannot be compiled,
# assembled, linked, or executed. Supports C, C++, Ada, Rust, Go (Golang),
# FORTRAN, D, Java, C Sharp, F Sharp (compiled only), COBOL, Haskell, and
# assembly.
SOURCE = tuple(
    (
        'c cpp c++ h hpp h++ cxx hxx hdl '  # C/C++
        'ada '  # Ada
        'rs '  # Rust
        'go '  # Go
        'f for f90 f95 f03 '  # FORTRAN
        'd dd di '  # D
        'java '  # Java
        'hs '  # Haskell
        'cs '  # C Sharp
        'fs '  # F Sharp compiled source (NOT .fsx, which is interactive-ready)
        'cbl cob '  # COBOL
        'asm s '  # Assembly
    ).split()
)

# This just contains plain text files (.txt).
TEXT = ('txt',)

# The default allowed extensions - `TEXT`, `DOCUMENTS`, `DATA`, and `IMAGES`.
DEFAULTS = TEXT + DOCUMENTS + IMAGES + DATA


class All:
    """
    This type can be used to allow all extensions. There is a predefined
    instance named `ALL`.
    """
    def __contains__(self, item: str) -> bool:
        return True


#: This "contains" all items. You can use it to allow all extensions to be
#: uploaded.
ALL = All()


class AllExcept:
    """
    This can be used to allow all file types except certain ones. For example,
    to ban .exe and .iso files, pass::

        AllExcept(('exe', 'iso'))

    to the `UploadSet` constructor as `extensions`. You can use any container,
    for example::

        AllExcept(SCRIPTS + EXECUTABLES)
    """
    def __init__(self, items: Iterable[str]) -> None:
        self.items = items

    def __contains__(self, item: str) -> bool:
        return item not in self.items


def extension(filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        # os.path.splitext retains . separator
        ext = ext[1:]
    return ext


def lowercase_ext(filename: str) -> str:
    """
    This is a helper used by UploadSet.save to provide lowercase extensions for
    all processed files, to compare with configured extensions in the same
    case.

    .. versionchanged:: 0.1.4
       Filenames without extensions are no longer lowercased, only the
       extension is returned in lowercase, if an extension exists.

    :param filename: The filename to ensure has a lowercase extension.
    """
    if '.' in filename:
        main, ext = os.path.splitext(filename)
        return main + ext.lower()
    # For consistency with os.path.splitext,
    # do not treat a filename without an extension as an extension.
    # That is, do not return filename.lower().
    return filename
