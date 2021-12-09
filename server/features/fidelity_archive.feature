Feature: Fidelity Specific Archive Behaviour

    @auth
    Scenario: Create new text item and get internal id
        Given empty "archive"
        Given "desks"
        """
        [
            {"name": "test"}
        ]
        """
        Given "content_types"
        """
        [{"_id": "test_profile", "schema": {
            "headline": {"default": "default_headline"},
            "internal_id" : {
                    "type" : "text",
                    "required" : false,
                    "enabled" : true,
                    "nullable" : true
            },
            "disclaimer" : {
                    "type" : "text",
                    "required" : false,
                    "enabled" : true,
                    "nullable" : true
            }
        }}]
        """
        When we post to "/archive"
        """
        {"type": "text", "profile": "test_profile", "body_html": "<p>content</p>", "task": {"desk": "#desks._id#"}}
        """
        Then we get new resource
        """
        {
        	"_id": "__any_value__",
            "guid": "__any_value__",
            "type": "text",
            "extra": {
                "internal_id": "__any_value__",
                "disclaimer": "__any_value__"
            },
            "original_creator": "__any_value__",
            "word_count": 1,
            "operation": "create",
            "sign_off": "abc"
        }
        """
