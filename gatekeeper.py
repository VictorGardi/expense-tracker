from typing import Callable

import streamlit as st

from login import login


def gatekeeper(func: Callable):
    authenticator = login()
    if st.session_state["authentication_status"]:
        #authenticator.logout("Logout", "main")
        func()
    elif not st.session_state["authentication_status"]:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
