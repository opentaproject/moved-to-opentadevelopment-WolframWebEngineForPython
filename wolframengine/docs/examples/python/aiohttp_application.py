# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.evaluation import WolframEvaluatorPool
from wolframengine.web import aiohttp_wl_view
from wolframclient.language import wl

from aiohttp import web

session = WolframEvaluatorPool(poolsize = 4)

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello from aiohttp")

@routes.get('/form')
@aiohttp_wl_view(session)
async def form_view(request):
    return wl.FormFunction({"x": "String"}, wl.Identity, AppearanceRules = {"Title": "Hello from WL!"})

@routes.get('/api')
@aiohttp_wl_view(session)
async def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity)

@routes.get('/app')
@aiohttp_wl_view(session)
async def app_view(request):
    return wl.Once(wl.Get("path/to/my/complex/wl/app.wl"))

app = web.Application()
app.add_routes(routes)
web.run_app(app)