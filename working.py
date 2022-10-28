import json
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    date: str
    title: str
    url: str
    labels: list
    content: str
    urls: list


app = FastAPI()


@app.get("/")
def home():
    return {"Home": "page"}


@app.get("/articles/{article_id}")
def find_item(article_id: int):
    con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM articles WHERE id = {article_id}""")
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


@app.get("/articles/")
def articles_query(label: str = None, date: str = None):
    if label:
        con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM articles WHERE labels LIKE '%{label}%'""", )
        result = cur.fetchall()
        cur.close()
        con.close()
        return result
    elif date:
        con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute("""SELECT * FROM articles WHERE date = ?""", (date,))
        result = cur.fetchall()
        cur.close()
        con.close()
        return result
    else:
        con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute("""SELECT * FROM articles""")
        result = cur.fetchall()
        cur.close()
        con.close()
        return result


@app.delete("/articles/{article_id}")
def delete_item(article_id: int):
    con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute(f"""DELETE FROM articles WHERE id = {article_id}""")
    con.commit()
    cur.close()
    con.close()
    return {"Request sent": 1}


@app.post("/articles/{article_id}")
def update_item(article_id: int, item: Item = None):
    con = sqlite3.connect("nbs_sk/articles.db", check_same_thread=False)
    cur = con.cursor()
    if 'string' != item.date:
        cur.execute("""UPDATE articles SET date = ? WHERE id = ?""", (item.date, article_id))
    if 'string' != item.title:
        cur.execute("""UPDATE articles SET title = ? WHERE id = ?""", (item.title, article_id))
    if 'string' != item.url:
        cur.execute("""UPDATE or REPLACE articles SET url = ? WHERE id = ?""", (item.url, article_id))
    if ['string'] != item.labels:
        cur.execute("""UPDATE articles SET labels = ? WHERE id = ?""", (json.dumps(item.labels), article_id))
    if 'string' != item.content:
        cur.execute("""UPDATE articles SET content = ? WHERE id = ?""", (item.content, article_id))
    if ['string'] != item.urls:
        cur.execute("""UPDATE articles SET urls = ? WHERE id = ?""", (json.dumps(item.urls), article_id))
    con.commit()
    cur.close()
    con.close()
    return {"Request sent": 1}
