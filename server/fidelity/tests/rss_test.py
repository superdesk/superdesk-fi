from ..content_api_rss import get_permalink, PERMALINK


def test_get_permalink():
    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-5b4111",
                "headline": "I can't avoid risk.",
                "profile": "123",
                "extra": {PERMALINK: "I can't avoid risk. How do I take it wisely?"},
                "genre": [
                    {
                        "name": "Article",
                        "qcode": "genre_custom:Article",
                        "translations": {
                            "name": {
                                "it": "Articolo",
                                "ja": "レポート",
                                "de": "Artikel"
                            }
                        },
                        "scheme": "genre_custom"
                    }
                ],
            }
        )
        == (
            "https://www.fidelityinternational.com/editorial/article/"
            "i-cant-avoid-risk-how-do-i-take-it-wisely-5b4111-en5/"
        )
    )

    assert (
        get_permalink(
            {
                "_id": "guid:foo-bar-baz-61c89a",
                "profile": "123",
                "name": "some name",
                "language": "ja",
                "extra": {PERMALINK: None},
                "genre": [
                    {
                        "name": "Article",
                        "qcode": "genre_custom:Article",
                        "translations": {
                            "name": {
                                "it": "Articolo",
                                "ja": "レポート",
                                "de": "Artikel"
                            }
                        },
                        "scheme": "genre_custom"
                    },
                    {
                        "name": "Blog",
                        "qcode": "genre_custom:Blog",
                        "translations": {
                            "name": {
                                "it": "Blog",
                                "ja": "ブログ",
                                "de": "Blog"
                            }
                        },
                        "scheme": "genre_custom"
                    }
                ],
            }
        )
        == "https://www.fidelityinternational.com/editorial/article/some-name-61c89a-en5/"
    )
