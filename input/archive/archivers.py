import zipfile
from Utilities.types import ArchiverType, ArchiveFileType


class Zipper(ArchiverType):

    def _extract_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, 'r') as f:
            f.extractall(path=archive.new, members=archive.mbr, pwd=archive.pwd)

    def _inspect_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, 'r') as f:
            return f.namelist()

    def _size_method(self, archive: ArchiveFileType):
        pass

    def _is(self, archive: ArchiveFileType):
        return zipfile.is_zipfile(archive.pth)
