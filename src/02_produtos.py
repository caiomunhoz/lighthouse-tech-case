import pandas as pd
from thefuzz import process

def main():
    raw_products = pd.read_csv('dataset/produtos_raw.csv')
    
    clean_products = raw_products.drop_duplicates(subset='code')

    clean_products['price'] = (
        clean_products['price']
        .str.replace('R$ ', '')
        .astype(float)
    )

    clean_products['actual_category'] = clean_products['actual_category'].apply(
        lambda x: process.extractOne(x, ['eletrônicos', 'propulsão', 'ancoragem'])[0]
    )

    clean_products.to_csv('dataset/produtos_clean.csv', index=False)


if __name__ == '__main__':
    main()