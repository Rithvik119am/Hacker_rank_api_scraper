from flask import Flask, render_template, request, send_file
from cdc_scraper import linker
app = Flask(__name__)

@app.route('/')
def home():
    """
    This function is used to render the home page of the application.
    It uses the 'index.html' template to render the home page.
    """    
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """
    This function is used to convert the URL to an excel file.
    It gets the URL from the form data, passes it to the 'linker' function to get the excel file name,
    and then sends the excel file as a download.
    """
    url = request.form['url']
    excel_file = linker(url)+'.xlsx'
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)