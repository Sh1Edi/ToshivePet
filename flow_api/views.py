from django.shortcuts import render
import hmac
import requests
from hashlib import sha256

# Esta aplicación, Flow_API, ha sido diseñada según las especificaciones de la API de
# Flow. Junto a cada función definida en este archivo se describe la función, los parámetros
# que toma y su significado, y la estructura de la respuesta que el servicio retorna en caso
# de que la solicitud se cumpla de manera exitosa.
# En caso de que el servicio retorne un error, la estructura estándar de este es un objeto JSON
# con las siguientes llaves:
#
#  code     number  Código de error. Valores comunes son 400 (error de la API), 401 (error interno del negocio)
#  message  string  Mensaje del error.


#Estas llaves se generaron para un entorno de Sandbox
secrKey  = "" # Agregar SecrKey de flow
fApiKey  = "" # Agregar Api Key de Flow
flowUrl  = "https://sandbox.flow.cl/api"

# Crea una "firma".
# Una "firma" es una cadena de texto encriptada utilizada por Flow para verificar la integridad
# de una soicitud. Esta función es llamada por las otras funciones de este archivo.
#
# Parámetros:
#   params  dict{}  Diccionario de parámetros a codificar
def makeSignature(params):
    s = ""
    keys = list(params.keys())
    keys.sort()
    for key in keys:
        s+=key+str(params[key])
    return hmac.new(secrKey.encode("UTF-8"),s.encode("UTF-8"),sha256).hexdigest()

# Retorna un texto de error para mostrar al usuario final según el error de una peticiión.
#
# Parámetros:
#   response  JSON  La respuesta de una solicitud que resultó en error.
#
# Retorna  un string para ser mostrado al usuario final
def clientifyErrorMessage(response):
    if "message" in response:
        if response["message"] == "Internal Server Error - email is not valid":
            return "Email inválido"
        else:
            return response["message"]

# Permite obtener la lista paginada de pagos recibidos en un día.
# Los objetos pagos de la lista tienen la misma estructura de los retornados en los servicios payment/getStatus
#
# Parámetros:
#   date   string  Fecha con formato "YYYY-MM-DD"
#   start  int     Opcional (def 0). Indica el primer pago que la solicitud debería retornar
#   limi   int     Opcional (def 10). Máximo de pagos que la solicitud debería retornar
#
# Retorna (JSON):
#   total    number         El número total de registros encontrados
#   hasMore	 bool           "1" si existen más páginas, "0" si es la última página
#   data	 Array[Object]  Arreglo de registros de la página. Cada Object del arreglo tiene la estructura
#                           indicada en la función getPaymentStatus [22-06: la función no existe aún]
def getPayments(date, start=0, limit=10):
    fullHook = flowUrl + "/payments/getPayments"
    params={"apiKey":fApiKey,"date":str(date)}
    if start != 0:
        params["start"]=str(start)
    if limit != 10:
        params["limit"]=str(limit)
    params["s"] = makeSignature(params)
    return requests.get(fullHook,params).json()

# Permite crear un nuevo cliente. El servicio retorna el objeto cliente creado.
#
# Parámetros:
#   name        string  Nombre del cliente
#   email       string  Dirección de correo electrónico del cliente
#   externalId  string  ID que el sistema local usa para identificar al cliente
#
# Retorna (JSON):
#   customerId	     string  Identificador del cliente
#   created	         string  Fecha de cración del cliente. El formato es [YYYY-MM-DD HH:MM:SS]
#   email	         string  Dirección email del cliente
#   name	         string  Nombre del cliente
#   pay_mode	     string  Modo de pago del cliente: "auto" (cargo automático), o "manual" (cobro manual)
#   creditCardType	 string  La marca de la tarjeta de crédito registrada
#   last4CardDigits	 string  Los últimos 4 dígitos de la tarjeta de crédito registrada
#   externalId	     string  El identificador del cliente en su negocio
#   status	         string  El estado del cliente: "0" (Eliminado), o "1" (Activo)
#   registerDate	 string  Fecha en que el cliente registro su tarjeta de crédito. El formato es [YYYY-MM-DD HH:MM:SS>]
def createCustomer(name, email, externalId):
    fullHook = flowUrl + "/customer/create"
    params={"apiKey":fApiKey,"name":str(name),"email":str(email),"externalId":str(externalId)}
    params["s"] = makeSignature(params)
    return requests.post(fullHook,params).json()

# Permite obtener la lista de clientes paginada de acuerdo a los parámetros de paginación.
# Además, se pueden definir los siguientes filtros para buscar clientes específicos, según
# nombre y/o estado
#
# Parámetros:
#   start   int     Opcional (def 0). Indica el primer cliente que la solicitud debería retornar
#   limit   int     Opcional (def 10). Máximo de clientes que la solicitud debería retornar
#   filter  string  Opcional (def ""). Filtro por nombre de cliente.
#   status  string  Opcional (def ""). Filtro por estado de cliente.
#
# Retorna (JSON):
#   total    int            El número total de registros encontrados
#   hasMore	 bool           "1" si existen más páginas, "0" si es la última página
#   data	 Array[Object]  Arreglo de registros de la página. Es posible que la estructura de cada objeto
#                           sea la indicada en la función getCustomer [22-06: la función no existe aún]
def listCustomers(start=0, limit=10, filter="", status=""):
    fullHook = flowUrl + "/customer/list"
    params = {"apiKey":fApiKey}
    if start != 0:
        params["start"]=str(start)
    if limit != 10:
        params["limit"]=str(limit)
    if filter != "":
        params["filter"]=str(filter)
    if status != "":
        params["status"]=str(status)
    params["s"] = makeSignature(params)
    return requests.get(fullHook,params).json()

# Permite crear una orden de pago a Flow y recibe como respuesta la URL para redirigir el browser del
# pagador y el TOKEN que identifica la transacción. La url de redirección se debe formar concatenando
# los valores recibidos en la respuesta, de la forma [URL + "?token=" + TOKEN].
# Una vez que el pagador efectúe el pago, Flow notificará el resultado a la página del comercio que se
# envió en el parámetro urlConfirmation.
#
# Parámetros:
#   commerceOrder    string  Orden del comercio. Identificador creado por el negocio.
#   subject          string  Descripción de la orden.
#   currency	     string  Opcional. Moneda de la orden.
#   amount           number  Monto de la orden
#   email            string  Dirección email del pagador
#   paymentMethod    int     Opcional. Identificador del medio de pago. Si se envía el identificador, el pagador será
#                            redireccionado directamente al medio de pago que se indique, de lo contrario Flow
#                            le presentará una página para seleccionarlo. El medio de pago debe haber sido
#                            previamente contratado. Podrá ver los identificadores de sus medios de pago en la
#                            sección "Mis Datos" ingresando a Flow con sus credenciales. Para indicar todos los
#                            medios de pago utilice el identificador "9"
#   urlConfirmation  string  URL callback del comercio, donde Flow confirmará el pago
#   urlReturn        string  URL de retorno del comercio donde Flow redirigirá al pagador
#   optional	     string  Opcional. Datos opcionales en formato JSON
#   timeout	         int     Opcional. Tiempo en segundos para que una orden expire después de haber sido creada. Si no se
#                            envía este parámetro, la orden no expirará y estará vigente para pago por tiempo
#                            indefinido. Si la orden expira, no podrá ser pagada.
#   merchantId	     string  Opcional. Id de comercio asociado. Solo aplica si usted es comercio integrador.
#   payment_currency string  Opcional. Moneda en que se espera se pague la orden
#
# Retorna (JSON):
#   url    string  URL de la página donde el pagador realizará el pago. Debe añadírsele el valor de token
#                  como parámetro URL "token="
#   token  string  Token de autenticación para el pago a realizar.
def createPayment(commerceOrder, subject, amount, email, urlConfirmation, urlReturn, currency="", paymentMethod=0, optional="", timeout=300, merchantId="", payment_currency=""):
    fullHook = flowUrl + "/payment/create"
    params = {"apiKey":fApiKey, "commerceOrder":str(commerceOrder), "subject":str(subject),"amount":str(amount),"email":str(email),"urlConfirmation":str(urlConfirmation),"urlReturn":str(urlReturn)}
    if currency != "":
        params["currency"]=str(currency)
    if paymentMethod != 0:
        params["paymentMethod"]=str(paymentMethod)
    if optional != "":
        params["optional"]=str(optional)
    if timeout != 300:
        params["timeout"]=str(timeout)
    if merchantId != "":
        params["merchantId"]=str(merchantId)
    if payment_currency != "":
        params["payment_currency"]=str(payment_currency)
    params["s"] = makeSignature(params)
    return requests.post(fullHook,params).json()