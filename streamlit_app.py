from typing import Optional, Dict, Any

import streamlit as st
from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)


def api_post(
    path: str,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    files: Any = None,
):
    token = st.session_state.get("token")
    headers: Dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.post(path, json=json, data=data, files=files, headers=headers)


def do_register(email: str, password: str, full_name: str) -> None:
    payload = {"email": email, "password": password, "full_name": full_name}
    resp = api_post("/auth/register", json=payload)
    if resp.status_code != 200:
        st.error(f"Register failed: {resp.text}")
        return
    st.success("Registration successful. You can now log in.")


def do_login(email: str, password: str) -> None:
    data = {"username": email, "password": password}
    resp = api_post("/auth/login", data=data)
    if resp.status_code != 200:
        st.error(f"Login failed: {resp.text}")
        return
    token = resp.json().get("access_token")
    if not token:
        st.error("No access token returned")
        return
    st.session_state["token"] = token
    st.success("Logged in successfully.")


def do_logout() -> None:
    try:
        api_post("/auth/logout")
    except Exception:
        pass
    st.session_state["token"] = None
    st.success("Logged out.")


def do_ocr(file) -> None:
    if not file:
        st.warning("Please upload a file first.")
        return
    files = {"file": (file.name, file.getvalue(), file.type)}
    resp = api_post("/api/ocr/routed", files=files)
    if resp.status_code != 200:
        st.error(f"OCR failed: {resp.text}")
        return
    data = resp.json()
    st.subheader("OCR Result")
    st.json(data)


def main() -> None:
    st.set_page_config(page_title="DocVision AI OCR", layout="wide")

    if "token" not in st.session_state:
        st.session_state["token"] = None

    st.markdown(
        """
        <style>
        .auth-card {
            max-width: 800px;
            margin: 3rem auto;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.12);
            overflow: hidden;
            display: flex;
            min-height: 420px;
            background: #ffffff;
        }
        .auth-left {
            flex: 1;
            padding: 40px 48px;
            background: #ffffff;
        }
        .auth-right {
            flex: 1;
            padding: 40px 48px;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            text-align: left;
        }
        .auth-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 24px;
        }
        .auth-subtitle {
            font-size: 14px;
            color: #777;
            margin-bottom: 16px;
        }
        .auth-input label {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 4px;
            display: block;
        }
        .auth-input input {
            width: 100%;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 14px;
        }
        .auth-button-primary {
            border-radius: 50px;
            padding: 10px 32px;
            border: none;
            background: #ff4b2b;
            color: #ffffff;
            font-weight: 600;
            font-size: 14px;
        }
        .auth-button-primary:hover {
            background: #ff416c;
        }
        .auth-right button {
            border-radius: 50px;
            padding: 10px 32px;
            border: 2px solid #ffffff;
            background: transparent;
            color: #ffffff;
            font-weight: 600;
            font-size: 14px;
        }
        .auth-right button:hover {
            background: rgba(255,255,255,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align: center; margin-top: 1rem;'>DocVision AI OCR</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #666;'>Sign in to your account or create a new one to continue.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-left'>", unsafe_allow_html=True)

        st.markdown("<div class='auth-title'>Sign in</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Use your email and password to sign in.</div>",
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            st.markdown("<div class='auth-input'>", unsafe_allow_html=True)
            log_email = st.text_input("Email", key="log_email")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='auth-input'>", unsafe_allow_html=True)
            log_password = st.text_input("Password", type="password", key="log_password")
            st.markdown("</div>", unsafe_allow_html=True)

            submitted_login = st.form_submit_button("Sign in")
            if submitted_login:
                do_login(log_email, log_password)

        if st.session_state.get("token"):
            if st.button("Logout"):
                do_logout()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='auth-right'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:26px;font-weight:700;margin-bottom:12px;'>Hello, Friend!</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:14px;opacity:0.9;margin-bottom:24px;'>Enter your personal details and start your journey with us.</p>",
            unsafe_allow_html=True,
        )
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Full name", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            submitted = st.form_submit_button("Sign up")
            if submitted:
                do_register(reg_email, reg_password, reg_name)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("Upload and OCR")
        if not st.session_state.get("token"):
            st.info("You must login before uploading documents.")
            return

        file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if st.button("Run OCR"):
            do_ocr(file)

    with upload_tab:
        if not st.session_state.get("token"):
            st.info("You must login before uploading documents.")
            return

        st.subheader("Upload Document")
        file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if st.button("Run OCR"):
            do_ocr(file)


if __name__ == "__main__":
    main()
