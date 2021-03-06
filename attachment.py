import os
import tarfile
import zipfile

from blessings import Terminal
term = Terminal()

TAR_EXTENSION = '.tar.gz'
ZIP_EXTENSION = '.zip'
PY_EXTENSION = '.py'
TXT_EXTENSION = '.txt'

ALLOWED_ARCHIVE_EXTENSIONS = (TAR_EXTENSION,
                              ZIP_EXTENSION,
                              )

ALLOWED_CODE_EXTENSIONS = (PY_EXTENSION,
                           TXT_EXTENSION,
                           )

def archive_extension(filename):
    for extension in ALLOWED_ARCHIVE_EXTENSIONS:
        if extension in filename:
            return extension

def archive_basename(filename):
    ext = archive_extension(filename)
    if ext:
        basename = filename.split(ext)[0]
        return basename

def _archive_filter(members, name_func):
    for member in members:
        name = name_func(member)
        if ('..' in name or
                name.startswith('/')):
            continue

        if os.path.splitext(name)[1] in ALLOWED_CODE_EXTENSIONS:
            yield member


def decompress_archives(path):
    archives = os.listdir(path)

    for archive in archives:
        ext = archive_extension(archive)
        if not ext:
            continue

        print('Decompressing {}'.format(term.blue(archive)))
        full_path = os.path.join(path, archive)

        basename = archive_basename(archive)
        new_dir = os.path.join(path, basename)

        if os.path.exists(new_dir):
            print(term.yellow('{} already exists! Continuing...'.format(new_dir)))
            continue

        os.mkdir(new_dir)

        new_full_path = os.path.join(new_dir, archive)
        os.rename(full_path, new_full_path)

        if ext is TAR_EXTENSION:
            tar_file = tarfile.open(new_full_path, 'r')
            tar_file.extractall(path=new_dir, members=_archive_filter(tar_file, lambda x: x.name))
            tar_file.close()
        elif ext is ZIP_EXTENSION:
            zip_file = zipfile.ZipFile(new_full_path, 'r')
            zip_file.extractall(path=new_dir, members=_archive_filter(zip_file.namelist(), lambda x: x))
