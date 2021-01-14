import os
import zipfile
import tarfile
import gzip
from typing import List
from Utilities.base import ArchiverType, ArchiveFileType, ArchiveFindType


class ArchiveFinder(ArchiveFindType):
    """ It finds the proper ArchiverType class in ArchiveFactory """

    def get_val(self, archive: ArchiveFileType) -> ArchiverType:
        return self.factory[self.get_key(archive)]

    def get_key(self, archive: ArchiveFileType) -> str:
        for item, func in self.factory.items():
            if func.combatible_with(archive):
                return item
        else:
            raise KeyError(f"{archive.pth} Format is not compatible")


class GZipper(ArchiveFindType):

    def get_val(self, archive: ArchiveFileType):
        for func in self.factory.values():
            if func.compatible_with(archive):
                return func
        else:
            raise ValueError(f"Format is not compatible")

    def get_key(self, _ignore: ArchiveFileType):
        for key in self.factory:
            if self.factory[key] == self:
                return key

    def warning_decorator(func):
        def wrapper(self, _ignore, *args, **kwargs):
            import warnings

            key = self.get_key(_ignore)
            warnings.warn(f"'{key}' DOES NOT support '{func.__name__}()' method. "
                          f"Try 'extract()' method first.",
                          RuntimeWarning, stacklevel=4)
        return wrapper

    @warning_decorator
    def _size_method(self, archive: ArchiveFileType) -> None: ...

    @warning_decorator
    def _inspect_method(self, archive: ArchiveFileType) -> None: ...

    def _extract_method(self, archive: ArchiveFileType):
        import gzip
        import shutil

        compressed = '.'.join(archive.pth.split('.')[:-1])
        with gzip.open(archive.pth, self._r) as f_in:
            with open(compressed, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        archive.pth = compressed
        try:
            super(GZipper, self)._extract_method(archive)
            os.remove(compressed)
        except ValueError:
            if os.path.dirname(archive.pth) != archive.new:
                new_path = os.path.join(archive.new, os.path.basename(archive.pth))
                shutil.move(archive.pth, new_path)

    def _is(self, archive: ArchiveFileType):
        with gzip.GzipFile(archive.pth, self._r) as f:
            try:
                f.read(1)
                return True
            except gzip.BadGzipFile:
                return False


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


class TarZipper(ArchiverType):

    def _size_method(self, archive: ArchiveFileType):
        result = dict()
        with tarfile.TarFile(archive.pth, self._r) as f:
            for mbr in f.getmembers():
                if mbr.isfile():
                    result[mbr.name] = {'size': mbr.size}
        return result

    def _inspect_method(self, archive: ArchiveFileType):
        with tarfile.TarFile(archive.pth, self._r) as f:
            return f.getnames()

    def _extract_method(self, archive: ArchiveFileType):
        if archive.pwd:
            import warnings

            warnings.warn(f"{self.__class__.__name__} does not use password",
                          RuntimeWarning, stacklevel=4)

        members = self._mbr_to_tar(archive.mbr)
        with tarfile.TarFile(archive.pth, self._r) as f:
            f.extractall(path=archive.new, members=list(members))

    def _is(self, archive: ArchiveFileType):
        return tarfile.is_tarfile(archive.pth)

    @staticmethod
    def _mbr_to_tar(members) -> List[tarfile.TarInfo]:
        if isinstance(members, (list, tuple)):
            for m in members:
                yield tarfile.TarInfo(m)
        else:
            return None
