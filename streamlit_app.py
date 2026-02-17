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
        body {
            background-color: #0B0F19;
            color: #F8FAFC;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
        }
        .main .block-container {
            max-width: 1100px;
            padding-top: 2.5rem;
            padding-bottom: 2.5rem;
        }
        .auth-panel {
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(148, 163, 184, 0.35);
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.9);
            padding: 28px 30px;
            backdrop-filter: blur(24px);
        }
        .auth-panel-gradient {
            background: radial-gradient(circle at 0% 0%, rgba(216, 180, 254, 0.25), transparent 55%),
                        radial-gradient(circle at 100% 100%, rgba(134, 239, 172, 0.18), transparent 55%),
                        linear-gradient(135deg, #6366F1, #8B5CF6);
            border-color: rgba(99, 102, 241, 0.6);
        }
        .auth-heading {
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
            color: #F9FAFB;
        }
        .auth-text {
            font-size: 14px;
            color: #94A3B8;
            margin-bottom: 16px;
        }
        .auth-text-light {
            color: rgba(248, 250, 252, 0.78);
        }
        .auth-input {
            margin-bottom: 14px;
        }
        .auth-input label {
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #94A3B8;
            margin-bottom: 6px;
        }
        .auth-input input {
            width: 100%;
            border-radius: 0.55rem;
            border: 1px solid rgba(148, 163, 184, 0.5);
            background: rgba(15, 23, 42, 0.85);
            color: #E5E7EB;
            font-size: 14px;
            padding: 9px 11px;
        }
        .auth-input input:focus {
            outline: none;
            border-color: #6366F1;
            box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.5);
        }
        .upload-panel {
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.96);
            border: 1px dashed rgba(148, 163, 184, 0.6);
            box-shadow: 0 24px 50px rgba(15, 23, 42, 0.9);
            padding: 20px 22px;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.6rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])

    with center_col:
        st.markdown(
            "<h1 style='text-align:center; margin-top:0.25rem; font-size:2.3rem; font-weight:700; letter-spacing:-0.04em; color:#F9FAFB;'>DocVision AI OCR</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#94A3B8; margin-bottom:1.5rem;'>Securely sign in to manage and extract intelligence from your documents.</p>",
            unsafe_allow_html=True,
        )

        main_left, main_right = st.columns([2, 1])

        with main_left:
            left_col, right_col = st.columns(2)

            with left_col:
                st.markdown("<div class='auth-panel'>", unsafe_allow_html=True)
                st.markdown("<div class='auth-heading'>Welcome back</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='auth-text'>Sign in with your DocVision AI account to access uploads and results.</div>",
                    unsafe_allow_html=True,
                )

                with st.form("login_form"):
                    st.markdown("<div class='auth-input'><label>Email</label>", unsafe_allow_html=True)
                    log_email = st.text_input("", key="log_email")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div class='auth-input'><label>Password</label>", unsafe_allow_html=True)
                    log_password = st.text_input("", type="password", key="log_password")
                    st.markdown("</div>", unsafe_allow_html=True)

                    submitted_login = st.form_submit_button("Sign in")
                    if submitted_login:
                        do_login(log_email, log_password)

                if st.session_state.get("token"):
                    if st.button("Logout", key="logout_btn"):
                        do_logout()

                st.markdown("</div>", unsafe_allow_html=True)

            with right_col:
                st.markdown("<div class='auth-panel auth-panel-gradient'>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='auth-heading'>New to DocVision?</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<div class='auth-text auth-text-light'>Create an account to start extracting structured data from invoices, forms, and more.</div>",
                    unsafe_allow_html=True,
                )

                with st.form("register_form"):
                    st.markdown("<div class='auth-input'><label>Full name</label>", unsafe_allow_html=True)
                    reg_name = st.text_input("", key="reg_name")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div class='auth-input'><label>Email</label>", unsafe_allow_html=True)
                    reg_email = st.text_input("", key="reg_email")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div class='auth-input'><label>Password</label>", unsafe_allow_html=True)
                    reg_password = st.text_input("", type="password", key="reg_password")
                    st.markdown("</div>", unsafe_allow_html=True)

                    submitted = st.form_submit_button("Create account")
                    if submitted:
                        do_register(reg_email, reg_password, reg_name)

                st.markdown("</div>", unsafe_allow_html=True)

        with main_right:
            st.markdown("<div class='upload-panel'>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size:18px;font-weight:600;color:#E5E7EB;margin-bottom:0.5rem;'>Upload and OCR</div>",
                unsafe_allow_html=True,
            )
            if not st.session_state.get("token"):
                st.markdown(
                    "<div class='auth-text' style='margin-bottom:0;'>You must log in before uploading documents.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
                return

            file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
            if st.button("Run OCR"):
                do_ocr(file)
            st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
