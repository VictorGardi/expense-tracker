from typing import Callable

import streamlit as st
import streamlit_authenticator as stauth
import yaml


def login() -> stauth.Authenticate:
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    name, authentication_status, username = authenticator.login("Login", "main")
    st.session_state["authentication_status"] = authentication_status
    st.session_state["name"] = name
    st.session_state["username"] = username
    return authenticator


def gatekeeper(func: Callable):
    _ = login()
    # authenticator = login()
    if st.session_state["authentication_status"]:
        # authenticator.logout("Logout", "main")
        func()
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
    elif not st.session_state["authentication_status"]:
        st.error("Username/password is incorrect")
