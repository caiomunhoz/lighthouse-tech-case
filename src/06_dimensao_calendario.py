import duckdb
import pandas as pd

def main():
    sales_df = pd.read_csv('dataset/vendas_2023_2024.csv')
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'], format='mixed')

    query = """
        WITH date_range AS (
            SELECT *
            FROM generate_series(
                (SELECT MIN(sale_date) FROM sales_df),
                (SELECT MAX(sale_date) FROM sales_df),
                INTERVAL 1 DAY
            ) AS t(date)
        ),

        daily_sales AS (
            SELECT
                sale_date AS date,
                SUM(total) AS total_amount
            FROM sales_df
            GROUP BY sale_date
        ),

        calendar_sales AS (
            SELECT
                d.date,
                COALESCE(s.total_amount, 0) AS total_amount
            FROM date_range d
            LEFT JOIN daily_sales s
                ON s.date = d.date
        )

        SELECT
            CASE strftime(date, '%w')
                WHEN '0' THEN 'Domingo'
                WHEN '1' THEN 'Segunda-feira'
                WHEN '2' THEN 'Terça-feira'
                WHEN '3' THEN 'Quarta-feira'
                WHEN '4' THEN 'Quinta-feira'
                WHEN '5' THEN 'Sexta-feira'
                WHEN '6' THEN 'Sábado'
            END AS dia_semana,
            ROUND(AVG(total_amount), 2) AS avg_daily_sales
        FROM calendar_sales
        GROUP BY dia_semana
        ORDER BY avg_daily_sales ASC
    """

    print(duckdb.sql(query))

if __name__ == '__main__':
    main()

