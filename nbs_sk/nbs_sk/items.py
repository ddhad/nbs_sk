# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_jsonschema import JsonSchemaItem


class NbsSkItem(JsonSchemaItem):
    jsonschema = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "title": "Article",
        "description": "Article from nbs.sk",
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Published on",
                "format": "date"
            },
            "title": {
                "type": "string",
                "description": "Article title"
            },
            "url": {
                "type": "string",
                "description": "Article url"
            },
            "labels": {
                "type": "array",
                "description": "Tags",
                "items": {
                    "type": "string"
                }
            },
            "content": {
                "type": "string",
                "description": "Article content"
            },
            "urls": {
                "type": "array",
                "description": "Urls from article body",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["date", "title", "url", "labels", "content", "urls"]

    }
