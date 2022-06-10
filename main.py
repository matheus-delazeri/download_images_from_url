import os.path
from pathlib import Path
from lib.file_handler import FileHandler
from lib.images import Images
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="dooca - Dooca Images, bling - Bling Images,  0 - Default")
args = parser.parse_args()

CURRENT_DIR = str(Path(__file__).parent) + "/"

sheetDir = CURRENT_DIR + input("- Digite o nome da planilha a ser lida: ") + ".csv"
products = {}
if os.path.isfile(sheetDir):
    fileHandler = FileHandler(sheetDir)
    image = Images()
    imagesDict = {}
    if not args.i:
        products = fileHandler.get_products_images()
    elif args.i == 'dooca':
        products = fileHandler.get_dooca_images()
    elif args.i == 'bling':
        products = fileHandler.get_bling_images()
    for sku in products:
        product = products[sku]
        imagesDict[sku] = image.download_images(sku, product['basename'], product['images'])

    image.print_proccess_info()
    fileHandler.create_csv_from_dict(imagesDict)
else:
    print("Planilha não encontrada!")
