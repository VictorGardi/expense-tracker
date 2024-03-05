import streamlit as st
from streamlit_tags import st_tags

from expense_tracker.db import (
    add_category,
    delete_category,
    get_categories,
    update_category,
)
from expense_tracker.login import gatekeeper


def categories():
    data = get_categories()

    if data:
        st.dataframe(
            [{"category": name, "tags": tags} for name, tags in data.items()],
            use_container_width=True,
        )
        categories = sorted(data.keys())
        with st.expander("Update a category"):
            category = st.selectbox("Select a category", categories, key=1)

            tags = st_tags(label="Enter tags", value=data[category])
            if st.button("Update"):
                e = update_category(category, tags)
                if e:
                    st.error(
                        f"Failed to add category {category} to database due to {e}"
                    )
                else:
                    st.success(f"Added category {category} to database")
                    st.experimental_rerun()
        with st.expander("Delete a category"):
            category = st.selectbox("Select a category", categories, key=2)
            if st.button("Delete"):
                e = delete_category(category)
                if e:
                    st.error(f"Failed to delete category {category} due to {e}")
                else:
                    st.success(f"Deleted category {category} to database")
                    st.experimental_rerun()
    else:
        st.write("No categories exist. Please add below.")

    with st.expander("Add a new category"):
        category = st.text_input("Choose a name for your category, for example 'food'")
        tags = st_tags(label="Enter tags")
        if st.button("Save category"):
            e = add_category(category, tags)
            if e:
                st.error(f"Failed to add category {category} to database due to {e}")
            else:
                st.success(f"Added category {category} to database")
                st.experimental_rerun()


if __name__ == "__main__":
    gatekeeper(categories)
