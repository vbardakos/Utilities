GENERAL INFO
------------
```yaml
Package:  Utilities
Author:   vbar
Version:  0.1.2
Created:  08.02.2021
Abstract: Integration and Simplification of Various Utilities
```

EXAMPLE
-------
```python
from Utilities.input.archive import File


my_path = 'data/archive.zip'
my_file = File(my_path)
 
my_file.format 
# `data/archive.zip` format (i.e. 'ZIP')

my_file.supported_formats
# File() class supported formats

my_file.inspect
# `data/archive.zip` member files' inspection

my_file.size
# `data/archive.zip` member files' size

my_file.extract()
# extracts to current path

files_to_extract = ['file1.txt', 'path/file2.csv']
my_file.extract(members=files_to_extract, to_path='new_data/')
# extracts archive members to new_data/
```

HISTORY
------
```
# VERSION 0.1.0
---------------
New Object Factory base class
- FactoryType

New ./archive classes
- Base Classes
    1. ArchiveFileType
    2. ArchiverType
- Subclasses
    1. ArchiveFile
    2. Zipper
    3. ArchiveFinder

Supported Formats: zip


# VERSION 0.1.1
---------------
New ./archive classes
- Base
    1. ArchiveFindType(ArchiverType)
- Subclasses
    1. GZipper(ArchiveFindType)
    2. TarZipper(ArchiverType)

Refactored Classes
- Subclasses
    1. ArchiveFinder(ArchiveFindType)
    2. ArchiveFile(_ArchFileFormat)

Supported Formats: zip, tar, gunzip


# VERSION 0.1.2
---------------
Full support:
- gunzip format & recursive extraction of files

Refactored:
- ArchiverType

Update methods:
- TarZipper(ArchiverType)
- GZipper(ArchiveFindType)


# VERSION 0.1.3
---------------
Replace
- __conf.py with .config.ini includes read/write info
