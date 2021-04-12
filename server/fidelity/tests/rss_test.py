from ..content_api_rss import get_permalink, PERMALINK


def test_get_permalink():
    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-5b4111",
                "headline": "I can't avoid risk. How do I take it wisely?",
                "profile": "123",
                "extra": {PERMALINK: "I can't avoid risk. How do I take it wisely?"},
            }
        )
        == "https://www.fidelityinternational.com/editorial/123/i-cant-avoid-risk-how-do-i-take-it-wisely-5b4111-en5/"
    )

    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-61c89a",
                "profile": "123",
                "name": "some name",
                "language": "ja",
                "extra": {PERMALINK: None},
            }
        )
        == "https://www.fidelityinternational.com/editorial/123/some-name-61c89a-en5/"
    )
