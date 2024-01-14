import sys
import os
import re
import shutil
from pathlib import Path


def processing_folder(path):

    for directory in path.iterdir():

        if directory.is_dir():

            if directory.name in extensions:
                continue
            try:
                os.rmdir(directory)
                continue
            except OSError:
                processing_folder(directory)
                continue
        files.append(directory)

    return files


def processing_file(files):
    for file in files:
        if file.suffix in extensions["archives"]:
            archives(file)
            continue
        elif file.suffix in extensions["images"]:
            images(file,)
            continue
        elif file.suffix in extensions["audio"]:
            audio(file)
            continue
        elif file.suffix in extensions["documents"]:
            documents(file)
            continue
        elif file.suffix in extensions["video"]:
            video(file)
            continue
        elif file.suffix == "":
            continue
        else:
            categor["unknown"].append(file.name)
            unknown.add(file.suffix)


def root_dir():
    if len(sys.argv) != 2:
        print("No argument")
        return sys.exit(1)
    elif not Path(sys.argv[1]).exists():
        print("Does not exist")
        return sys.exit(1)

    return sys.argv[1]


def normalize(name):
    maps = {

        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
        'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia',

        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E',
        'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya',

    }
    names = name.split(".")

    if len(names) < 2:
        name_join = names[0]
    else:
        name_join = ".".join(names[:-1])

    translate_name = name_join.translate(name_join.maketrans(maps))
    re_name = re.sub(r'[^a-zA-Z0-9.]', '_', translate_name)
    if len(names) >= 2:
        normalize_name = ".".join([re_name, names[-1]])
    else:
        normalize_name = re_name
    return normalize_name


def archives(file):
    famous.add(file.suffix)
    categor["archives"].append(file.name)
    remove_extension = os.path.splitext(file.name)[0]
    shutil.unpack_archive(file.name, 'archives/' + remove_extension)
    os.remove(file)


def images(file):
    famous.add(file.suffix)
    norma = normalize(file.name)
    categor["images"].append(norma)
    os.rename(file, norma)
    shutil.move(norma, "images")


def audio(file):
    famous.add(file.suffix)
    norma = normalize(file.name)
    categor["audio"].append(norma)
    os.rename(file, norma)
    shutil.move(norma, "audio")


def documents(file):
    famous.add(file.suffix)
    norma = normalize(file.name)
    categor["documents"].append(norma)
    os.rename(file, norma)
    shutil.move(norma, "documents")


def video(file):
    famous.add(file.suffix)
    norma = normalize(file.name)
    categor["video"].append(norma)
    os.rename(file, norma)
    shutil.move(norma, "video")


def main(file_path):
    path = Path(file_path)
    os.chdir(path)

    for dir in extensions:
        try:
            os.mkdir(dir)
        except FileExistsError:
            continue

    processing_folder(path)
    processing_file(files)
    processing_folder(path)

    print(f"Файли з відомим розширенням:\n\
          images: {categor['images']}\n\
          video: {categor['video']}\n\
          documents: {categor['documents']}\n\
          audio: {categor['audio']}\n\
          archives: {categor['archives']}\n")
    print(f"Відомі розширення: {famous}")
    print(f"Невідомі розширення: {unknown}")


extensions = {

    "images": ('.jpeg', '.png', '.jpg', '.svg'),
    "video": ('.avi', '.mp4', '.mov', '.mkv'),
    "documents": ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    "audio": ('.vp3', '.ogg', '.wav', '.amr'),
    "archives": ('.zip', '.gz', '.tar'),

    }

categor = {

    "images": [],
    "video": [],
    "documents": [],
    "audio": [],
    "archives": [],
    "unknown": [],

    }

famous = set()
unknown = set()
files = []

if __name__ == "__main__":
    file_path = root_dir()
    main(file_path)
