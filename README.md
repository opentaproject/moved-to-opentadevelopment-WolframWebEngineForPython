# Wolfram Web Engine for Python

Wolfram Web Engine for Python allows you to use a Wolfram Kernel during a web request.

This cli serves files from the current directory and below, directly mapping the directory structure to HTTP requests.

## Getting Started

### Prerequisites

1. Python 3.5 or higher
2. Wolfram Language 11.3 or higher
3. [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython)

### Install Using pip (Recommended)
Recommended for most users. It installs the latest stable version released by Wolfram Research.

Evaluate the following command in a terminal:

```
>>> pip3 install wolframengineforpython
```

### Install Using Git

Recommended for developers who want to install the library along with the full source code.
Clone the library’s repository:

```
>>> git clone git://github.com/WolframResearch/WolframWebEngineForPython
```

Install the library in your site-package directory:

```
>>> cd WolframWebEngineForPython
>>> pip3 install .
```

### Start a demo server

Start a demo server by doing:

```
python3 -m wolframwebengine --demo
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop/wolframengineforpython/wolframwebengine/examples/demoapp
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Now you can open your web browser at the address http://localhost:18000/

![image](https://stash.wolfram.com/projects/LCL/repos/wolframengineforpython/raw/docs/assets/image1.png?at=refs%2Fheads%2Ffeature%2Fdocs)

## Two different ways of structuring an application:

1. Use a single file with URLDispatcher
2. Use multiple files in a directory layout

## Single file with URLDispatcher

One way to run your server is to direct all requests to a single file
that runs a Wolfram Language [URLDispatcher](https://reference.wolfram.com/language/ref/URLDispatcher.html) function.

Write the following content in a file called `dispatcher.m`:

```
URLDispatcher[{
    "/api" -> APIFunction["x" -> "String"], 
    "/form" -> FormFunction["x" -> "String"], 
    "/" -> "hello world!"
}]
```

From the same location run:

```
>>> python3 -m wolframwebengine dispatcher.m
----------------------------------------------------------------------
Address         http://localhost:18000/
File            /Users/rdv/Desktop/dispatcher.m
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

All incoming requests will now be routed to the `URLDispatcher` function in `dispatcher.m`.
You can now open the following urls in your browser:

```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api
```

For more information about `URLDispatcher` please refer to the [online documentation](https://reference.wolfram.com/language/ref/URLDispatcher.html).

## Multiple files in a directory layout

Another way to write an application is to create a directory structure that is served by the server. The url for each file will match the file's directory path.

The server will serve content with the following rules:

1. All files with extensions '.m', '.mx', '.wxf', '.wl' will be evaluated in the Kernel using [GenerateHTTPResponse](https://reference.wolfram.com/language/ref/GenerateHTTPResponse.html) on the content of the file.
2. Any other file will be served as static content.
3. If the request path corresponds to a directory on disk, the server will search for a file named index.wl in that directory. This convention can be changed with the --index option.

Create an application by running the following code in your current location:

```
mkdir testapp
mkdir testapp/form
mkdir testapp/api
echo 'ExportForm[{"hello", UnixTime[]}, "JSON"]' >  testapp/index.wl
echo 'FormFunction["x" -> "String"]'             >  testapp/form/index.wl
echo 'APIFunction["x" -> "String"]'              >  testapp/api/index.wl
echo 'HTTPResponse["hello world"]'               >  testapp/api/response.wl
echo '["some", "static", "JSON"]'                >  testapp/static.json
```

Start the application by running:

```
>>> python3 -m wolframwebengine testapp
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop/testapp
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Then open the browser at the following locations:

```
http://localhost:18000/
http://localhost:18000/form
http://localhost:18000/api
http://localhost:18000/static.json
```

One advantage of a multi-file application structure is that is very easy to extend the application. You can simply place new files into the appropriate location in your application directory and they will automatically be served.


### Options

```
>>> python3 -m wolframwebengine --help
usage: __main__.py [-h] [--port PORT] [--domain DOMAIN] [--kernel KERNEL]
                   [--poolsize POOLSIZE] [--cached] [--lazy] [--index INDEX]
                   [path]

positional arguments:
  path

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Insert the port.
  --domain DOMAIN      Insert the domain.
  --kernel KERNEL      Insert the kernel path.
  --poolsize POOLSIZE  Insert the kernel pool size.
  --cached             The server will cache the WL input expression.
  --lazy               The server will start the kernels on the first request.
  --index INDEX        The file name to search for folder index.
```

#### path

The first argument can be a folder or a single file.

Write a file on your current folder:

```
>>> echo 'ExportForm[{"hello", "from", "Kernel", UnixTime[]}, "JSON"]' >  index.wl
```

then from CLI Run

```
>>> python3 -m wolframwebengine
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

If the first argument is a file, all request path will be routed to the same expression.
If the first argument is a folder, requests will be redirected to the kernel if the url extension ends with '.m', '.mx', '.wxf', '.wl'.

If the request path is a folder the server will search for an index.wl in the same folder.

```
>>> python3 -m wolframwebengine
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```


#### --index

Specify the default file name for folder index.
Defaults to index.wl

```
python3 -m wolframwebengine --index index.wxf
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wxf
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```


#### --cached

If --cached is present then every request will run the source code once

```
>>> python3 -m wolframwebengine --cached
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

Visit the browser and refresh the page.


#### --port PORT

Allows you to specify the PORT of the webserver. Defaults to 18000.

```
>>> python3 -m wolframwebengine --port 9090
----------------------------------------------------------------------
Address          http://localhost:9090/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --kernel KERNEL

Allows you to specify the Kernel path

```
>>> python3 -m wolframwebengine --kernel '/Applications/Mathematica11.3.app/Contents/MacOS/WolframKernel'
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit) 
```

#### --poolsize SIZE

Allows you to change the default pool size for kernels. Defaults to 1.

```
>>> python3 -m wolframwebengine --poolsize 4
----------------------------------------------------------------------
Address          http://localhost:18000/
Folder          /Users/rdv/Desktop
Index           index.wl
----------------------------------------------------------------------
(Press CTRL+C to quit)
```

#### --lazy 

If the option is present the server will wait for the first request to spawn the kernels, instead of spawning them immediately.


## Integrating an existing application

Wolfram Web Engine for Python can be used to augment an existing python application instead of creating a new one.
We currently support the following frameworks:

### Django

If you have an existing [Django](!https://www.djangoproject.com/) application you can use the `django_wl_view` decorator to evaluate Wolfram Language code during a web request.

```python
from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.urls import path

from wolframclient.language import wl
from wolframclient.evaluation import WolframLanguageSession
from wolframwebengine.web import django_wl_view

session = WolframLanguageSession()

def django_view(request):
    return HttpResponse("hello from django")

@django_wl_view(session)
def form_view(request):
    return wl.FormFunction({"x": "String"}, wl.Identity, "JSON")


@django_wl_view(session)
def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity, "JSON")


urlpatterns = [
    path("", django_view, name="home"),
    path("form", form_view, name="form"),
    path("api", api_view, name="api"),
]
```

The decorator can be used with any kind of syncronous evaluator exposed and documented in [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython).

### Aiohttp

If you have an existing [Aiohttp](!https://docs.aiohttp.org/en/stable/web_reference.html) server running you can use the `aiohttp_wl_view` decorator to evaluate Wolfram Language code during a web request.

```python
from aiohttp import web

from wolframclient.evaluation import WolframEvaluatorPool
from wolframclient.language import wl
from wolframwebengine.web import aiohttp_wl_view

session = WolframEvaluatorPool(poolsize=4)
routes = web.RouteTableDef()


@routes.get("/")
async def hello(request):
    return web.Response(text="Hello from aiohttp")


@routes.get("/form")
@aiohttp_wl_view(session)
async def form_view(request):
    return wl.FormFunction(
        {"x": "String"}, wl.Identity, AppearanceRules={"Title": "Hello from WL!"}
    )


@routes.get("/api")
@aiohttp_wl_view(session)
async def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity)


@routes.get("/app")
@aiohttp_wl_view(session)
async def app_view(request):
    return wl.Once(wl.Get("path/to/my/complex/wl/app.wl"))


app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
```

The decorator can be used with any kind of asyncronous evaluator exposed and documented in [WolframClientForPython](!https://github.com/WolframResearch/WolframClientForPython).

