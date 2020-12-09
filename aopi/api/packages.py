from aiohttp import web
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View

router = RouteTableDef()


@router.view("/{package_name}/")
class PackageView(View):
    async def get(self) -> web.Response:
        pkg_name = self.request.match_info.get("package_name")
        return web.Response(
            body=f"""
        <a href="http://localhost:5678/{pkg_name}_10.2.wheel">{pkg_name}</a>
        """,
            content_type="text/html",
        )
