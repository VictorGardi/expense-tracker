import streamlit_authenticator as stauth


def generate_hashed_pw(unhashed_pw: str) -> str:
    return stauth.Hasher([unhashed_pw]).generate()[0]

if __name__ == "__main__":
    print(generate_hashed_pw("chosen_random_pw"))
