import dash
import dash_table
import pandas as pd
import dash_html_components as html

try:
    from google.cloud import firestore
except ModuleNotFoundError:
    pass


def read_data(path):
    client = firestore.Client()
    query = client.collection(path['collection']).document(path['document'])
    data = query.get().to_dict()
    return data


def pos_stats(path):
    try:
        data = read_data(path)
    except NameError:
        data = {
            'data': {
                'stock': ['AAPL', 'MSFT'],
                'delta': [100, 110],
                'theta': [50, 60]
            },
            'timestamp': '2021-02-12T15:57:54-0500'
        }
        pass

    df = pd.DataFrame.from_dict(data['data'])
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'stock'})

    el = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )

    return el