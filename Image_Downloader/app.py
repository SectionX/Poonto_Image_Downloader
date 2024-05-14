"""
Instantiates the FastAPI object and defines the GET and POST methods
"""

from fastapi import FastAPI #, Request
# from fastapi.responses import Response


# from .manage import controller
# from .manage import parser


app = FastAPI()


@app.post('/images/{supplier_name}')
async def upload_products_worksheet():
    """
    Handles the POST method for the path.
    """


@app.get('/images/{supplier_name}')
async def start_downloader_process():
    """
    Handles the GET method for the path.
    """


# '''
# {'_cookies': {},
#  '_form': None,
#  '_headers': Headers({'host': 'localhost:8080', 'user-agent':
# 'python-requests/2.31.0', 'accept-encoding': 'gzip, deflate',
# 'accept': '*/*', 'connection': 'keep-alive'}),
#  '_is_disconnected': False,
#  '_query_params': QueryParams('action=help'),
#  '_receive': <bound method RequestResponseCycle.receive of <uvicorn.protocols.
# http.httptools_impl.RequestResponseCycle object at 0x7820deae9d50>>,
#  '_send': <function wrap_app_handling_exceptions.<locals>.
# wrapped_app.<locals>.sender at 0x7820deaf09a0>,
#  '_stream_consumed': False,
#  'scope': {'app': <fastapi.applications.FastAPI object at 0x7820dfb95910>,
#            'asgi': {'spec_version': '2.4', 'version': '3.0'},
#            'client': ('127.0.0.1', 58502),
#            'endpoint': <function start_downloader_process at 0x7820deae3c40>,
#            'headers': [(b'host', b'localhost:8080'),
#                        (b'user-agent', b'python-requests/2.31.0'),
#                        (b'accept-encoding', b'gzip, deflate'),
#                        (b'accept', b'*/*'),
#                        (b'connection', b'keep-alive')],
#            'http_version': '1.1',
#            'method': 'GET',
#            'path': '/images/estia',
#            'path_params': {'supplier_name': 'estia'},
#            'query_string': b'action=help',
#            'raw_path': b'/images/estia',
#            'root_path': '',
#            'route': APIRoute(path='/images/{supplier_name}', name='start_down
# loader_process', methods=['GET']),
#            'router': <fastapi.routing.APIRouter object at 0x7820defbae90>,
#            'scheme': 'http',
#            'server': ('127.0.0.1', 8080),
#            'starlette.exception_handlers': ({<class 'starlette.exceptions
# .HTTPException'>: <function http_exception_handler at 0x7820def14ae0>,
#                                              <class 'starlette.exceptions
# .WebSocketException'>: <bound method ExceptionMiddleware.websocket_exception
#  of <starlette.middleware.exceptions.ExceptionMiddleware object at 0x7820deae84d0>>,
#                                              <class 'fastapi.exceptions.WebSocket
# RequestValidationError'>: <function websocket_request_validatio
# n_exception_handler at 0x7820def14c20>,
#                                              <class 'fastapi.exceptions.Request
# ValidationError'>: <function request_validation_exception_handler at 0x7820def14b80>},
#                                             {}),
#            'state': {},
#            'type': 'http'}}'''
