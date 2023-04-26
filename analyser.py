import os
import pandas as pd

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n")
product_code = input("Podaj kod produktu: ")