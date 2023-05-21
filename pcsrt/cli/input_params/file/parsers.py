from pathlib import Path
from .errors import ParseFileError
from .filetype import FileType
from .file import File

def parse_file(file,fileclass=File):
    path = str(file) # Convert to string
    file_extension = Path(file).suffix.lower()
    if file_extension[1:] in ["las","laz","ply"]:
        file_type = FileType[file_extension[1:].upper()]
        #print(file_type)
        return fileclass(path, file_type)
    else:
        error_msg = f"Unsupported file type \"{file_extension}\" of \"{path}\""
        raise ParseFileError(error_msg)
