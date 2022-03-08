from aiohttp import web
import aiofiles
import json
from systemd import SystemD
import syslog

routes = web.RouteTableDef()
sd = SystemD()

def render_html_file(file_name):
    with open(f'templates/{file_name}', mode='r') as f:
        text = f.read()
        return web.Response(text=text, content_type='text/html')

async def index_handler(request):
    return render_html_file('index.html')

async def get_status(request):
    status = sd.isActive()
    return web.json_response(
        {
            'status': status
        }, 
        content_type='application/json'
    )

async def set_status(request):
    data = await request.json()
    sd.command(data['command'])
    status = sd.isActive()
    return web.json_response({'status': status}, content_type='application/json')

async def save_setting(request):
    data = await request.json()
    flag = data['flag']
    json_string = {'flag': flag}
    async with aiofiles.open('setting.json', mode='w') as f:
        await f.write(json.dumps(json_string))
    syslog.syslog('Настроки сохранены')
    return web.json_response({'success': True}, content_type='application/json')

async def load_setting(request):
    data = None
    try:
        async with aiofiles.open('setting.json', mode='r') as f:
            data = await f.read()
    except FileNotFoundError:
        syslog.syslog('Файл с настройками "setting.json" не найден.')

    if data:
        data = json.loads(data)
    else:
        data = {'flag': False}

    syslog.syslog('Загрузил настройки')
    return web.json_response(data, content_type='application/json')

async def make_app():
    app = web.Application()
    app.add_routes([
        web.get('/', index_handler),
        web.get('/getStatus', get_status),
        web.post('/setStatus', set_status),
        web.post('/save_setting', save_setting),
        web.get('/load_setting', load_setting),
    ])
    syslog.syslog('Программа запущена')
    return app

web.run_app(make_app())