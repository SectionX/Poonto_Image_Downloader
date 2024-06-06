import importlib
import sys

def main():
    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        print('''Poonto Downloader:
    Usage:
    poonto-downloader 'suppliername' 'path/to/file'

    It's good practice to enclose arguments with '' to avoid problems with spaces.
    Example
    poonto-downloader 'kentia' 'C:\\My Downloads\\estia diff.xlsx'

    The following formats are supported:
    kentia: xlsx (Searches for columns Title, ProductCode, ProductURL)
    vamvax: xlsx (Searches for columns Title, ProductCode, ProductURL)
    estia: xlsx (Searches for columns Title, ProductCode, ProductURL)
    artelibre: xml (Searches for the 'product' list)
            
    Images are automatically transformed to 740x740
    A zip will be created in the directory with the naming scheme [suppliername]-[date].zip
            ''')
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: poonto-downloader 'suppliername' 'path/to/file'\nType poonto-downloader --help for more info.")
        sys.exit(1)
    if len(sys.argv) > 3:
        print("Too many arguments. Make sure to enclose names or paths with spaces with ''. For example 'path/folder with space/file.ext'\nType poonto-downloader --help for more info.")
        sys.exit(1)

    supplier_module = importlib.import_module(f'.suppliers.{sys.argv[1]}.__main__', 'Image_Downloader')
    supplier_module.main()


if __name__ == "__main__":
    main()