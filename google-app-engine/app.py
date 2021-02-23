import dash
import dash_core_components as dcc
import dash_html_components as html

from template_ptf_stats import ptf_stats
from template_pos_stats import pos_stats


app = dash.Dash("Options trading")
server = app.server

app.layout = html.Div(
    children=[
        ptf_stats({
            'collection': 'options',
            'document': 'ptf_stats'
        }),
        pos_stats({
            'collection': 'options',
            'document': 'pos_stats'
        })
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)
