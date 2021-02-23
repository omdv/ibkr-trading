import dash
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


def ptf_stats(path):
    try:
        data = read_data(path)
    except NameError:
        data = {
            'delta': 1000,
            'theta': 500,
            'timestamp': '2021-02-12T15:57:54-0500'
        }
        pass

    el = html.Div([
        html.P(data['timestamp']),
        html.P('Theta: {}'.format(data['theta'])),
        html.P('Delta: {}'.format(data['delta']))
    ])

    return el