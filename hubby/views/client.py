from pyramid.renderers import render
from pyramid.response import Response

class BaseView(object):
    def __init__(self, request):
        self.request = request
        self.response = None
        self.data = {}
    
    def __call__(self):
        if self.response is not None:
            return self.response
        else:
            return self.data


    def get_app_settings(self):
        return self.request.registry.settings


class ClientView(BaseView):
    def __init__(self, request):
        super(ClientView, self).__init__(request)
        self.get_main()

    def get_main(self):
        template = 'hubby:templates/mainview.mako'
        settings = self.get_app_settings()
        basecolor = settings.get('default.css.basecolor', 'white-smoke')
        env = dict(appname='frontdoor', basecolor=basecolor)
        content = render(template, env)
        self.response = Response(body=content)
        self.response.encode_content()
        
    
