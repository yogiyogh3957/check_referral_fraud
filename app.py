from flask import Flask, send_file, make_response, render_template_string
from markupsafe import Markup
from main.models import Models
import io

app = Flask(__name__)

model = Models()
df = model.get_validation_referral()
@app.route('/')
def landing_page():

    # df = model.get_validation_referral()
    df_html = df.to_html(classes='table table-striped', index=False)

    html_template = '''
    <html>
    <head>
        <title>Data Table</title>
    </head>
    <body>
        <br>
        <a href="/download_csv">Download CSV</a>
        <br>
        {{ table_html|safe }}
    </body>
    </html>
    '''

    return render_template_string(html_template, table_html=Markup(df_html))

@app.route('/download_csv')
def download_csv() :

    # df = model.get_validation_referral()
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Create a response with the CSV file
    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=final_table.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == "__main__":
    app.run(debug=True)