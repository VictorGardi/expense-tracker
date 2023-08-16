import os

import streamlit as st
from streamlit_tags import st_tags

from expense_tracker.db import (
    add_category,
    connect_to_db,
    create_category_table,
    delete_category,
    get_categories,
)
from expense_tracker.login import gatekeeper


def categories():
    conn = connect_to_db(os.environ.get("SQLITE_URI"))
    create_category_table(conn)

    data = get_categories(conn)

    if data:
        st.dataframe(
            [{"category": key, "tags": data[key]} for key, vals in data.items()],
            use_container_width=True,
        )
        with st.expander("Edit a category"):
            category = st.selectbox("Select a category", sorted(data.keys()))
            tags = st_tags(label="Enter tags", value=data[category])
            col1, col2 = st.columns(2)
            if col1.button("Update category"):
                e = delete_category(conn, category)
                add_category(conn, category, tags)
                if e:
                    st.error(
                        f"Failed to add category {category} to database due to {e}"
                    )
                else:
                    st.success(f"Added category {category} to database")
                    st.experimental_rerun()

            elif col2.button("Delete category"):
                e = delete_category(conn, category)
                if e:
                    st.error(f"Failed to delete category {category} due to {e}")
                else:
                    st.success(f"Deleted category {category} to database")
                    st.experimental_rerun()
    else:
        st.write("No categories exist. Please add below.")

    with st.expander("Add a category"):
        category = st.text_input("Choose a name for your category, for example 'food'")
        tags = st_tags(label="Enter tags")
        if st.button("Save category"):
            e = add_category(conn, category, tags)
            if e:
                st.error(f"Failed to add category {category} to database due to {e}")
            else:
                st.success(f"Added category {category} to database")
                st.experimental_rerun()


if __name__ == "__main__":
    gatekeeper(categories)
