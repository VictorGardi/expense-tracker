import sqlite3
from typing import Dict, List, Optional


def connect_to_db(uri: str):
    conn = sqlite3.connect(uri)
    return conn


def create_category_table(conn) -> None:
    cursor = conn.cursor()
    if not cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='category';"
    ):
        cursor.execute("CREATE TABLE category (name TEXT, tags TEXT)")
        conn.commit()


def get_categories(conn) -> Dict[str, list]:
    cursor = conn.cursor()
    rows = cursor.execute("SELECT name, tags FROM category").fetchall()
    return {category: tags.split(",") for category, tags in rows}


def add_category(conn, category: str, tags: List[str]) -> Optional[Exception]:
    cursor = conn.cursor()
    data = {"name": category, "tags": ",".join(tags)}
    sql = "INSERT INTO category (name, tags) VALUES (:name, :tags)"
    try:
        cursor.execute(sql, data)
        conn.commit()
        return None
    except Exception as e:
        return e


def delete_category(conn, category: str) -> Optional[Exception]:
    cursor = conn.cursor()
    sql = f"DELETE FROM category WHERE name = '{category}';"
    try:
        cursor.execute(sql)
        conn.commit()
        return None
    except Exception as e:
        return e


if __name__ == "__main__":
    cursor = connect_to_db("sqlite.db")
