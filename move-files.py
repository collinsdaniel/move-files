import fnmatch
import os
import re
import shutil
from pathlib import Path
from zipfile import ZipFile
import resizeimage
import cv2
from PIL import Image, ImageStat

xml_files_pattern = '*.xml'
zip_files_pattern = '*.zip'

initial_path = ''
zip_files_processed_path = ''
unzip_files_path = ''
selected_files_path = ''
renamed_files_path = ''
# resized_images_path = ''
cured_files_path = ''


def create_dirs(zip_files_path):
    print('')

    # diretório onde serão criados os subdiretórios
    global initial_path
    initial_path = Path(zip_files_path / 'images_to_cure')
    initial_path.mkdir(exist_ok=True, parents=True)
    print('Initial path created: {}'.format(initial_path))

    # diretório de cópia dos arquivos zip
    global zip_files_processed_path
    zip_files_processed_path = Path(initial_path / '00_zipped')
    zip_files_processed_path.mkdir(exist_ok=True, parents=True)
    print('Zip files processed path created: {}'.format(zip_files_processed_path))

    # diretório dos arquivos descompactados
    global unzip_files_path
    unzip_files_path = Path(initial_path / '01_unzipped')
    unzip_files_path.mkdir(exist_ok=True, parents=True)
    print('Unzip files path created: {}'.format(unzip_files_path))

    # diretório dos arquivos selecionados (arquivos limpos - só imagens sem gif e svg)
    global selected_files_path
    selected_files_path = Path(initial_path / '02_selected')
    selected_files_path.mkdir(exist_ok=True, parents=True)
    print('Selected files path created: {}'.format(selected_files_path))

    # diretório dos arquivos renomeados
    global renamed_files_path
    renamed_files_path = Path(initial_path / '03_renamed')
    renamed_files_path.mkdir(exist_ok=True, parents=True)
    print('Selected files path created: {}'.format(selected_files_path))

    # diretório das imagens (arquivos selecionados) redimensionadas
    # global resized_images_path
    # resized_images_path = Path(initial_path / '03_resized')
    # resized_images_path.mkdir(exist_ok=True, parents=True)
    # print('Resized images path created: {}'.format(resized_images_path))

    # diretório dos arquivos curados
    global cured_files_path
    cured_files_path = Path(initial_path / '04_cured')
    cured_files_path.mkdir(exist_ok=True, parents=True)
    print('Cured files path created: {}'.format(cured_files_path))


def descompact_file(file):
    print('')
    print('descompact file: {}'.format(file))
    zipped = ZipFile(file)
    zipped.extractall(unzip_files_path)


def select_files_to_cure():
    print('')

    print('Select files to cure...')
    files_to_cure = [file for file in os.listdir(unzip_files_path) if re.match(r'^.*\.(?:png|PNG|jpg|JPG|jpeg|JPEG)$', file)]
    for file in files_to_cure:
        shutil.move(os.path.join(unzip_files_path, file), selected_files_path)


# def resize_images():
#     print('')
#
#     dir1 = '/Users/collins/Documentos/QwertAI/labs/faceDetect/curadoria/face/02_selected'
#     dir2 = '/Users/collins/Documentos/QwertAI/labs/faceDetect/curadoria/face/03_resized'
#
#     for file in os.listdir(dir1):
#         resized_file = 'resised_{}'.format(file)
#         resizeimage.resize_image(os.path.join(dir1, file), (256, 256), os.path.join(dir2, resized_file))
#         print('resize image: {} -> {}'.format(file, resized_file))


# def discard_duplicate_files():
#     print('')
#
#     print('Discard duplicate files...')
#
#     duplicate_files = []
#
#     for file in os.listdir(selected_files_path):
#         if file not in duplicate_files:
#             print('check duplicate file: {}'.format(file))
#             image_file = Image.open(os.path.join(selected_files_path, file))
#             image_mean1 = ImageStat.Stat(image_file).mean
#
#             for file_check in os.listdir(selected_files_path):
#                 if file_check != file:
#                     image_check = Image.open(os.path.join(selected_files_path, file_check))
#                     image_mean2 = ImageStat.Stat(image_check).mean
#
#                     if image_mean1 == image_mean2:
#                         duplicate_files.append(file_check)
#
#     for dup_file in duplicate_files:
#         os.remove(os.path.join(selected_files_path, dup_file))
#         print('duplicated removed: {}'.format(dup_file))


def discard_files_miniature():
    print('')

    print('Discard files miniature...')
    qtd = 0
    for file in os.listdir(selected_files_path):
        image = cv2.imread(os.path.join(selected_files_path, file))
        if image.shape[1] < 500:
            qtd += 1
            print('miniature file detected: {}'.format(file))
            shutil.move(os.path.join(selected_files_path, file), unzip_files_path)


def get_xml_files():
    return [os.path.splitext(file)[0] for file in os.listdir(selected_files_path) if fnmatch.fnmatch(file, xml_files_pattern)]


def move():
    all_files = sorted(os.listdir(selected_files_path))
    print("all files len: {}".format(len(all_files)))

    for file in all_files:
        if os.path.splitext(file)[0] in get_xml_files():
            shutil.move(selected_files_path + file, cured_files_path)

    choosed_files = sorted(os.listdir(cured_files_path))
    print("choosed files len: {}".format(len(choosed_files) / 2))


def rename_files(zip_name):
    print('')
    print('Rename files...')
    qtd = 0
    for file in os.listdir(selected_files_path):
        qtd += 1
        new_file = '{}_{}.{}'.format(zip_name, qtd, os.path.splitext(file)[1])
        os.rename(os.path.join(selected_files_path, file), os.path.join(renamed_files_path, new_file))
        print('file: {} -> {}'.format(file, new_file))


# def locate():
#     files = sorted(os.listdir(destination_folder))
#     print("files: ", files)
#     for file in files:
#         # print("file: {}".format(file))
#         if os.path.splitext(file)[0] not in get_xml_files():
#             print("file not exist xml: {}".format(file))


def main():
    zip_files_path = Path(input('Zipped files directory: '))

    # Passo 01: Criar novos diretórios partindo do informado
    create_dirs(zip_files_path)

    # Passo 02: Mover os arquivos zipados para o diretório
    zip_files = [file for file in os.listdir(zip_files_path) if fnmatch.fnmatch(file, zip_files_pattern)]
    print('')
    for file in zip_files:
        print('Move zip file: {}'.format(file))
        shutil.move(os.path.join(zip_files_path, file), zip_files_processed_path)

    # Passo 03: Descompactar os arquivos zipados
    print('')
    for file in os.listdir(zip_files_processed_path):
        descompact_file(os.path.join(zip_files_processed_path, file))

        # Passo 04: Selecionar arquivos necessários
        select_files_to_cure()

        # Passo 05: Redimensionar as imagens
        # resize_images()

        # Passo 05: Remover arquivos duplicados
        # discard_duplicate_files()

        # Passo 06: Remover miniaturas de imagens
        discard_files_miniature()

        # Passo 07: Renomear arquivos para facilitar reconhecimento
        rename_files(os.path.splitext(file)[0])


if __name__ == '__main__':
    main()
