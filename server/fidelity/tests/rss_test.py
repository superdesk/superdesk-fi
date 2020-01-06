from ..content_api_rss import get_permalink, PERMALINK


def test_get_permalink():
    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-5b4111",
                "extra": {PERMALINK: "I can't avoid risk. How do I take it wisely?"},
            }
        )
        == "https://www.fidelityinstitutional.com/en/i-cant-avoid-risk-how-do-i-take-it-wisely-5b4111/"
    )

    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-61c89a",
                "language": "ja",
                "extra": {PERMALINK: None},
            }
        )
        == "https://www.fidelityinstitutional.com/ja/61c89a/"
    )
