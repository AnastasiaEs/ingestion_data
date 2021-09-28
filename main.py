import traceback
from waitress import serve
from ingestionpack.app import rest
try:
    print('[INFO] Inicializando aplicación')
    print('[OK] Aplicación inicializada correctamente')
    # Servimos la aplicacion
    serve(rest.app, host='0.0.0.0', port=6200)

except:
    print(traceback.format_exc())

