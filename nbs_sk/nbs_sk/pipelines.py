# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import json
import sqlite3


class NbsSkPipeline:
    def __init__(self):
        self.con = sqlite3.connect("articles.db")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY,
        date TEXT,
        title TEXT,
        url UNIQUE,
        labels BLOB,
        content TEXT,
        urls BLOB
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO articles VALUES (NOT NULL,?,?,?,?,?,?)""", (
            item['date'],
            item['title'],
            item['url'],
            json.dumps(item['labels']),
            item['content'],
            json.dumps(item['urls'])
        ))
        self.con.commit()
        return item
