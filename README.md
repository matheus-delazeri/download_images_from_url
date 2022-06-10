# Download product images from URL 
Using a spreadsheet with product's SKUs + images URLs (separated with `;`) the script will download all images and store it in a folder.
It's also possible to download images using [Dooca](https://dooca.com.br/) or [Bling](https://www.bling.com.br/) API (in this case only the SKU is necessary).

## Requirements
Install libraries:
```
> pip install pandas requests tabulate
```

## Basic usage
To download images from URL, you will need to create a .CSV spreadsheet with the following columns:
|sku|basename|images|
| --- | --- | --- |
|product-sku|basename-for-images|https://link-to-image/1.jpg;https://link-to-image/2.jpg|

Where:
**sku**: product's SKU. Will be used in case the basename is empty;

**basename**: will be used to name the images being downloaded. E.g.: if the basename is 'product' and the product have 3 images to be downloaded, their names will be:
- product-1.jpg
- product-2.jpg
- product-3.jpg

**images**: images URL (separated by `;`);

After that, paste the .CSV file in the same folder as the file `main.py` and run:
```
> python3 main.py
```
The path of the .CSV file will be asked. If it is already in the same folder as the `main.py` file you only need to type it (without the .csv extension) and the process will start.
A new folder named `images` will be created in the same place where all images will be stored.

## How to download images from Dooca?
You will need to access your Dooca Store plataform and get an API Token in `Aplicativos -> API`. After that, you only need to create a spreadsheet with the following columns:
|sku|basename|
| --- | --- |
|product-sku|basename-for-images|

Where:
**sku**: product's SKU from Dooca. Will be used to make APIs request;

**basename**: will be used to name the images being downloaded. E.g.: if the basename is 'product' and the product have 3 images to be downloaded, their names will be:
- product-1.jpg
- product-2.jpg
- product-3.jpg

After that, paste the .CSV file in the same folder as the file `main.py` and run:
```
> python main.py -i dooca
```
The path of the .CSV file and Dooca's API token will be asked. After typing it the process will start and all images will be put in the folder `images` (in the same path as the main file)

## How to download images from Bling?
You will need to access your Bling plataform and get an API Key following the step by step: [API Key Bling](https://ajuda.bling.com.br/hc/pt-br/articles/360046937853-Introdu%C3%A7%C3%A3o-para-a-API-do-Bling-para-desenvolvedores-). After that, you only need to create a spreadsheet with the following columns:
|sku|basename|
| --- | --- |
|product-sku|basename-for-images|

Where:
**sku**: product's SKU from Bling. Will be used to make APIs request;

**basename**: will be used to name the images being downloaded. E.g.: if the basename is 'product' and the product have 3 images to be downloaded, their names will be:
- product-1.jpg
- product-2.jpg
- product-3.jpg

After that, paste the .CSV file in the same folder as the file `main.py` and run:
```
> python main.py -i bling
```
The path of the .CSV file and Bling's API key will be asked. After typing it the process will start and all images will be put in the folder `images` (in the same path as the main file)
