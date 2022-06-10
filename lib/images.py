from pathlib import Path
import os.path
import requests
import pandas as pd
from tabulate import tabulate


class Images:
    IMAGES_FOLDER = "/../images/"
    IMAGES_EXTENSIONS = ['jpg', 'png', 'jpeg']

    def __init__(self):
        self.dir = str(Path(__file__).parent.absolute()) + self.IMAGES_FOLDER
        self.create_dir()
        self.errors = {}
        self.product_count = 0
        self.images_count = 0
        self.error_count = 0

    def create_dir(self):
        if not os.path.isdir(self.dir):
            Path(self.dir).mkdir(parents=True, exist_ok=True)

    def download_images(self, sku, basename, images):
        img_num = 1
        self.product_count += 1
        images_names = []
        if basename == '':
            basename = sku
        for img_url in images:
            if img_url == '':
                continue
            img_ext, img_url = self.get_image_extension(img_url)
            img_name = f"{basename}-{str(img_num)}.{img_ext}"
            result_ok = self.download_from_url(img_url, img_name)
            images_names.append(img_name)
            if not result_ok:
                if sku not in self.errors:
                    self.errors[sku] = []
                self.errors[sku].append(img_url)
                self.error_count += 1
            img_num += 1
        return images_names

    def get_image_extension(self, img_url):
        original_url = img_url
        img_url = img_url.split('?')[0]
        img_ext = img_url.split(".")[-1]
        if img_ext not in self.IMAGES_EXTENSIONS:
            return 'jpg', original_url
        return img_ext, img_url

    def download_from_url(self, image_url, img_name):
        img_path = self.dir + img_name
        header = self.get_header()
        response = requests.get(image_url, headers=header)
        if response.ok:
            with open(img_path, 'wb') as f:
                f.write(response.content)
                self.images_count += 1
                print("\r", f"Imagens baixadas [{self.images_count}]", end="")
            return True
        return False

    @staticmethod
    def get_header():
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }

    def print_proccess_info(self):
        print(f"\n\n---- Informações")
        df_info = pd.DataFrame(
            [[self.product_count, self.images_count, self.error_count]],
            columns=["SKUs", "Imagens OK", "Imagens com erro"]
        )
        print(tabulate(df_info, headers="keys", tablefmt="psql", showindex=False))
        if self.error_count > 0:
            print(f"\n---- Erros")
            df_errors = pd.DataFrame(list(self.errors.items()), columns=["SKU", "URLs com erro"])
            print(tabulate(df_errors, headers="keys", tablefmt="psql", showindex=False))
        