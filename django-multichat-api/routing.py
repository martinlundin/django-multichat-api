from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import ChatConsumer
from chat.token_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            re_path(r'^chat/(?P<chatid>[^/]+)/$', ChatConsumer),
        ]),
    ),
})
