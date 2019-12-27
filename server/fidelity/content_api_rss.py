import flask
import superdesk

from lxml import etree
from feedgen import feed
from flask import current_app as app, request
from eve.utils import ParsedRequest


blueprint = flask.Blueprint("rss", __name__)
parser = etree.HTMLParser(recover=True)

AUTHOR_ROLE = "Primary Author"
FEATUREMEDIA = "featuremedia"
WEB_RENDITION = "baseImage"
CATEGORIES = ("subject_custom",)


def get_permalink(item):
    return "{}/{}".format(
        flask.url_for("rss.index", _external=True).rstrip("/"), item["_id"]
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
    auth = app.auth
    if not auth.authorized([], "items", request.method):
        return auth.authenticate()
    items_service = superdesk.get_resource_service("items")
    req = ParsedRequest()
    req.args = request.args
    items = list(items_service.get(req, {}))
    content = generate_feed(items)
    return flask.Response(content, mimetype="application/rss+xml")


def init_app(_app):
    _app.register_blueprint(blueprint, url_prefix="/contentapi")
