import pandas as pd

def main():
    raw_df = pd.read_json('dataset/custos_importacao.json')
    
    exploded_df = raw_df.explode('historic_data')

    exploded_df['start_date'] = exploded_df['historic_data'].str['start_date']
    exploded_df['usd_price'] = exploded_df['historic_data'].str['usd_price']
    
    exploded_df.drop(columns='historic_data', inplace=True)

    exploded_df.to_csv('dataset/custos_importacao.csv', index=False)

if __name__ == '__main__':
    main()