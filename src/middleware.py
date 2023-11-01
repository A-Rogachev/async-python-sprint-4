import typing

from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class BlacklistMiddleware:
    """
    Middleware, блокирующий доступ к сервису из запрещённых подсетей.
    За основу взят TrustedHostMiddleware.
    """
    def __init__(
        self,
        app: ASGIApp,
        blacklist: typing.Optional[typing.Sequence[str]] = None,
    ) -> None:
        """
        Инициализация middleware.
        """
        if blacklist is None:
            blacklist = []
        self.app = app
        self.blacklist = list(blacklist)

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope['type'] not in ('http', 'websocket'):
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        host: str = headers.get('host', '').split(':')[0]
        response = None
        if host in self.blacklist:
            response = PlainTextResponse(
                'Sorry, your host in blacklist.',
                status_code=400,
            )
        
        if response is not None:
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)
