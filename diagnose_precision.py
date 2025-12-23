from lxml import html
import pandas as pd

def diagnose():
    with open('input/salida_pp.xls', 'rb') as f:
        content = f.read()

    tree = html.fromstring(content)
    rows = tree.xpath('//tr')

    data = []
    for row in rows:
        tds = row.xpath('./td|./th')
        data.append([td.text_content().strip() for td in tds])

    df = pd.DataFrame(data)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    print(df)

if __name__ == "__main__":
    diagnose()
