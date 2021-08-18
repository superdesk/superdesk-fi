import flask
import logging
import superdesk

from flask import request
from eve.utils import ParsedRequest
from settings import PUBLIC_TOKEN
from .content_api_rss import get_authors, get_content_type

logger = logging.getLogger(__name__)
blueprint = flask.Blueprint("csv", __name__)

MAX_ITEMS = 200
SEPARATOR = ';'
FILENAME = 'bi.csv'


def get_content(item):
    try:
        return item["extra"]["Summary"] or ""
    except (KeyError, TypeError):
        pass
    return item.get("description_html") or ""


def get_csv(items):
    output = [SEPARATOR.join([
        'Package',
        'Title',
        'Guid',
        'Published',
        'Updated',
        'Author',
        'Language',
        'Article Type',
        'Keyword',
    ])]
    packages = get_packages()
    for item in items:
        name = item.get("headline") or item.get("name")
        if not name:
            continue
        authors = get_authors(item) or ['']
        keywords = item.get("keywords") or ['']
        for author in authors:
            for keyword in keywords:
                output.append(SEPARATOR.join([
                    packages.get(item['_id'], {'name': ''}).get('name') or '',
                    name,
                    item['_id'],
                    item['firstpublished'].strftime("%d/%m/%Y"),
                    item['versioncreated'].strftime("%d/%m/%Y"),
                    author,
                    item['language'].upper(),
                    get_content_type(item),
                    keyword,
                ]))
    logger.info("len %d %d", len(items), len(output) - 1)
    return '\n'.join(output)


def get_packages():
    packages = {}
    packages_list = superdesk.get_resource_service("packages").find({"type": "composite"})
    for package in packages_list:
        for assoc in package.get("associations", {}).values():
            if assoc and assoc.get("guid"):
                packages[assoc["guid"]] = {"name": package.get("headline") or package.get("slugline")}
    return packages


@blueprint.route("/bi")
def index():
    token = request.args.get("token", "")
    if PUBLIC_TOKEN and token != PUBLIC_TOKEN:
        flask.abort(401)
    items_service = superdesk.get_resource_service("rss_items")
    req = ParsedRequest()
    req.args = {k: request.args.get(k) for k in request.args if k != "token"}
    req.max_results = MAX_ITEMS
    items = list(items_service.get(req, {}))
    content = get_csv(items)
    return flask.Response(content, mimetype="text/csv", headers={
        "Content-Disposition": f"attachment; filename={FILENAME}",
    })


def init_app(_app):
    _app.register_blueprint(blueprint, url_prefix="/contentapi")
