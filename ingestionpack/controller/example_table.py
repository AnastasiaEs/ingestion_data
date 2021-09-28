from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from ingestionpack.utils.log import Log, init_tracer
from ingestionpack.utils.config import get_config
import traceback

APP_NAME= get_config().get('APP_NAME','NAME')
class_name = "MyClass.get_example_table" #TODO: obtener nombre de la classe
conf = SparkConf().setAppName(APP_NAME)
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
jaeger_tracer = init_tracer('service_name')
#jaeger_tracer.start_span('myclass_span').span_id
tracer = jaeger_tracer.start_span('myclass_span').context
log = Log(log_name="process_name", app_name=APP_NAME, class_name=class_name, spanContext=tracer, stdout=True)

def get_example_table():
    try:
        log.debug(f"Texto de prueba de mi log antes")
        csv_file = './ingestionpack/test/test.csv'
        df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(csv_file)
        log.debug(f"Texto de prueba de mi log")
        log.info(f"Texto de prueba de mi log")
        log.warning("Texto de prueba de mi log")
        log.error("Texto de prueba de mi log")
        result = df.select('dateRep', 'countriesAndTerritories').limit(10).collect()
        return result
    except Exception as e:
        log.error(traceback.format_exc())
        return e
    finally:
        pass
        #sc.stop()


if __name__ == '__main__':
    pass
