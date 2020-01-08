import flask
import superdesk

from lxml import etree
from feedgen import feed
from flask import request
from eve.utils import ParsedRequest
from content_api.search import SearchResource, SearchService
from fidelity.utils import slugify
from urllib.parse import urljoin

blueprint = flask.Blueprint("rss", __name__)
parser = etree.HTMLParser(recover=True)

AUTHOR_ROLE = "Primary Author"
FEATUREMEDIA = "featuremedia"
WEB_RENDITION = "baseImage"
CATEGORIES = ("subject_custom",)
PERMALINK = "Perma_URL"
BASE_URL = "https://www.fidelityinstitutional.com/"


def get_permalink(item):
    code = item["_id"][-6:]
    try:
        title = item["extra"][PERMALINK] or ""
        slug = slugify(title)
    except (KeyError, AttributeError):
        slug = ""
    return urljoin(
        BASE_URL,
        "/{lang}/{code}/".format(
            lang=item.get("language", "en"), code="-".join(filter(bool, [slug, code])),
        ),
    )


def get_content(item):
    html = item.get("body_html", "<p></p>").replace("<figcatpion>", "<figcaption>")
    return html


def generate_feed(items):
    fg = feed.FeedGenerator()
    fg.load_extension("dc")
    fg.title("Superdesk")
    fg.id(flask.url_for("rss.index", _external=True))
    fg.link(href=flask.url_for("rss.index", _external=True), rel="self")
    fg.description("Fidelity RSS")
    for item in items:
        if not item.get("headline") and not item.get("name"):
            continue  # no title no rss
        entry = fg.add_entry()
        entry.guid(item["_id"])
        entry.link({"href": get_permalink(item)})
        entry.title(item.get("headline", item.get("name", item.get("slugline", ""))))
        entry.published(item.get("firstpublished"))
        entry.updated(item["versioncreated"])
        entry.content(get_content(item), type="CDATA")
        entry.description(item.get("description_text") or "")

        if item.get("source"):
            entry.source(title=item["source"])

        if item.get("subject"):
            category = [
                {"term": s.get("name")}
                for s in item["subject"]
                if s.get("scheme") in CATEGORIES
            ]
            if category:
                entry.category(category)

        if item.get("authors"):
            authors = [
                author["name"]
                for author in item["authors"]
                if author.get("role") and author["role"].lower() == AUTHOR_ROLE.lower()
            ]
            if authors:
                entry.dc.dc_creator(", ".join(authors))

        if item.get("associations") and item["associations"].get(FEATUREMEDIA):
            media = item["associations"][FEATUREMEDIA]
            if media.get("renditions") and media["renditions"].get(WEB_RENDITION):
                entry.enclosure(
                    media["renditions"][WEB_RENDITION]["href"],
                    type=media["renditions"][WEB_RENDITION].get("mimetype"),
                )

    return fg.rss_str(pretty=True)


@blueprint.route("/rss")
def index():
    items_service = superdesk.get_resource_service("rss_items")
    req = ParsedRequest()
    req.args = request.args
    req.max_results = 200
    items = list(items_service.get(req, {}))
    content = generate_feed(items)
    return flask.Response(content, mimetype="application/rss+xml")


class RSSResource(SearchResource):
    datasource = {
        key: val
        for key, val in SearchResource.datasource.items()
        if key != "aggregations"
    }


def init_app(_app):
    _app.register_blueprint(blueprint, url_prefix="/contentapi")
    superdesk.register_resource("rss_items", RSSResource, SearchService, _app=_app)
