import zipfile
import gzip
from Utilities.base import ArchiverType, ArchiveFileType


class Zipper(ArchiverType):

    def _extract_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, self._r) as f:
            f.extractall(path=archive.new, members=archive.mbr, pwd=archive.pwd)

    def _inspect_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, self._r) as f:
            return f.namelist()

    def _size_method(self, archive: ArchiveFileType):
        result = dict()
        with zipfile.ZipFile(archive.pth) as f:
            for mbr in f.infolist():
                result[mbr.filename] = {'size': mbr.file_size,
                                        'compress': mbr.compress_size}
        return result

    def _is(self, archive: ArchiveFileType):
        return zipfile.is_zipfile(archive.pth)


class GZipper(ArchiverType):

    def _size_method(self, archive: ArchiveFileType):
        pass

    def _inspect_method(self, archive: ArchiveFileType):
        pass

    def _extract_method(self, archive: ArchiveFileType):
        with gzip.open(archive.pth, 'r') as f:
            pass

    def _is(self, archive: ArchiveFileType):
        pass