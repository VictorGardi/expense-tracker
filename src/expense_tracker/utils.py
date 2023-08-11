import streamlit_authenticator as stauth


def generate_hashed_pw(unhashed_pw: str) -> str:
    return stauth.Hasher([unhashed_pw]).generate()
