from Utilities.input.archive.factory import factory
from Utilities.input.archive.archivers import *
from Utilities.input.archive.archivefile import ArchiveFile


factory.register(None, ArchiveFinder(factory))
factory.register('GZIP', GZipper(factory))
factory.register('ZIP', Zipper())
factory.register('TAR', TarZipper())

File = ArchiveFile
