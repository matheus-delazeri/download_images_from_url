import pandas as pd
import requests
import time


class FileHandler:

    def __init__(self, filedir):
        self.df = pd.read_csv(filedir, dtype=str, keep_default_na=False)
        self.df.columns = [x.lower() for x in self.df.columns]
        self.columns = list(self.df.columns.values)
        if "sku" not in self.columns:
            print("Coluna 'sku' não encontrada na planilha.")
            quit(0)

    def get_bling_images(self):
        products = {}
        payload = self.get_bling_payload()
        print("\n")
        for index, row in self.df.iterrows():
            product_id = row['sku']
            products[product_id] = {
                'basename' : row['basename'],
                'images' : []
            }
            url = f"https://bling.com.br/Api/v2/produto/{product_id}/json"
            response = requests.get(url, params=payload)
            if response.ok:
                product_data = response.json()['retorno']['produtos'][0]['produto']
                images = product_data['imagem']
                for image in images:
                    products[product_id]['images'].append(image['link'])
            else:
                print(f"[Erro] Não foi possível requisitar as imagens do produto [{product_id}]")
            print("\r", f"Produtos requisitados [{len(products)}/{self.df.size}]", end="")
            time.sleep(0.5)
        print("\n")
        return products

    @staticmethod
    def get_bling_payload():
        api_key = input("- Digite a API Key do Bling: ")
        return {
            'apikey': api_key,
            'imagem': 'S'
        }

    def get_dooca_images(self):
        products = {}
        header = self.get_dooca_header()
        data = {'app': 'aaaaa'}
        print("\n")
        for index, row in self.df.iterrows():
            product_id = row['sku']
            products[product_id] = {
                'basename' : row['basename'],
                'images' : []
            }
            url = f"https://api.dooca.store/products/{product_id}/images"
            response = requests.get(url, json=data, headers=header)
            if response.ok:
                images = response.json()
                for image in images:
                    products[product_id]['images'].append(image['src'])
            else:
                print(f"[Erro] Não foi possível requisitar as imagens do produto [{product_id}]")
            print("\r", f"Produtos requisitados [{len(products)}]", end="")
        print("\n")
        return products

    @staticmethod
    def get_dooca_header():
        auth_token = input("- Digite o Token de acesso da API Dooca: ")
        return {
            'Authorization': 'Bearer ' + auth_token,
            'Content-Type': 'application/json'
        }

    def get_products_images(self):
        products = {}

        for index, row in self.df.iterrows():
            products[row['sku']] = {
                'basename' : row['basename'],
                'images' : []
            }
            for column in self.columns:
                if "image" in column.lower():
                    products[row['sku']]['images'].append(str(row[column]).split(";"))

        return products

    @staticmethod
    def create_csv_from_dict(images_dict):
        file_name = input("- Nome da planilha a ser gerada: ")
        for sku in images_dict:
            images_dict[sku] = ";".join(images_dict[sku])
        df = pd.DataFrame(list(images_dict.items()), columns=["SKU", "Imagens"])
        df.to_csv(file_name + ".csv", index=False)
        print(f"Arquivo [{file_name + '.csv'}] gerado com sucesso!")
