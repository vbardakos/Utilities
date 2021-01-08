from Utilities.input.archive.factory import factory
from Utilities.input.archive.archivers import *
from Utilities.input.archive.archivefile import ArchiveFile

factory.register('ZIP', Zipper())

File = ArchiveFile
