from flask import Flask, jsonify
from ingestionpack.controller.auth import auth
from ingestionpack.controller.example_table import get_example_table

#- INICIALIZACION DE LA APLICACION -#
app = Flask(__name__)
#-  DEFINICION DE ENDPOINTS -#

PREFIX = "/ingestion_data/v1"

@auth.login_required()
@app.route(f"{PREFIX}/example_table", methods=['GET'])
def example_table():
    try:
        result = get_example_table()
        return jsonify(result)
    except Exception as e:
        print(e)
        return e

if __name__ == '__main__':
    app.run('0.0.0.0', 5000,debug=True )

