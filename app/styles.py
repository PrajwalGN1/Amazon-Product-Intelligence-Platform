"""Custom CSS for the executive Streamlit application."""

from __future__ import annotations

import streamlit as st


def inject_global_styles() -> None:
    """Apply an Amazon-inspired enterprise design system."""

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --amazon-orange: #FF9900;
            --amazon-blue: #232F3E;
            --accent-blue: #146EB4;
            --soft-bg: #FAFAFA;
            --light-gray: #F6F7F9;
            --card: #FFFFFF;
            --text: #1F2937;
            --muted: #667085;
            --success: #2E7D32;
            --warning: #F9A825;
            --danger: #C62828;
            --border: #E6E8EC;
            --shadow: 0 18px 45px rgba(35, 47, 62, 0.10);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 0%, rgba(255, 153, 0, 0.10), transparent 28%),
                linear-gradient(180deg, #FFFFFF 0%, var(--soft-bg) 34%, #F8FAFC 100%);
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.2rem;
            max-width: 1480px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #F7F9FC 100%);
            border-right: 1px solid var(--border);
            box-shadow: 12px 0 40px rgba(35, 47, 62, 0.06);
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] label {
            color: var(--amazon-blue);
            font-weight: 600;
        }

        div[data-testid="stSelectbox"] > div,
        div[data-testid="stSlider"],
        div[data-testid="stTextInput"] > div > div,
        div[data-testid="stNumberInput"] > div > div {
            border-radius: 12px;
        }

        .top-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.15rem;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
            margin-bottom: 1rem;
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .brand-mark {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--amazon-blue), #31465C);
            color: #FFFFFF;
            display: grid;
            place-items: center;
            font-weight: 800;
            position: relative;
        }

        .brand-mark::after {
            content: "";
            position: absolute;
            bottom: 9px;
            width: 25px;
            height: 4px;
            border-radius: 999px;
            background: var(--amazon-orange);
        }

        .brand-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--amazon-blue);
            margin: 0;
            line-height: 1.1;
        }

        .brand-subtitle {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.2rem;
        }

        .status-strip {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.55rem;
        }

        .status-pill, .badge {
            border-radius: 999px;
            padding: 0.35rem 0.65rem;
            font-size: 0.74rem;
            font-weight: 700;
            border: 1px solid var(--border);
            background: #FFFFFF;
            color: var(--amazon-blue);
        }

        .status-ok {
            color: var(--success);
            background: rgba(46, 125, 50, 0.08);
            border-color: rgba(46, 125, 50, 0.20);
        }

        .hero {
            border-radius: 22px;
            padding: 1.7rem;
            background:
                linear-gradient(135deg, rgba(35, 47, 62, 0.96), rgba(20, 110, 180, 0.88)),
                linear-gradient(45deg, rgba(255, 153, 0, 0.16), transparent);
            color: #FFFFFF;
            box-shadow: var(--shadow);
            overflow: hidden;
            position: relative;
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: auto -8% -45% auto;
            width: 460px;
            height: 460px;
            border-radius: 50%;
            background: rgba(255, 153, 0, 0.16);
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1;
            letter-spacing: 0;
            margin: 0.2rem 0 0.75rem;
            max-width: 920px;
            color: #FFFFFF;
        }

        .hero p {
            max-width: 780px;
            color: rgba(255, 255, 255, 0.86);
            font-size: 1rem;
            line-height: 1.7;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 1.25rem;
        }

        .hero-chip {
            padding: 0.8rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.20);
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: 0 12px 30px rgba(35, 47, 62, 0.07);
            padding: 1rem;
            color: var(--text);
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
        }

        .card,
        .card div,
        .card p,
        .card span,
        .card li {
            color: var(--text);
        }

        .card p {
            color: #475467;
            font-weight: 500;
            line-height: 1.65;
        }

        .card b,
        .card strong,
        .card h1,
        .card h2,
        .card h3,
        .card h4 {
            color: var(--amazon-blue);
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 45px rgba(35, 47, 62, 0.12);
            border-color: rgba(255, 153, 0, 0.40);
        }

        .metric-card {
            min-height: 158px;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 5px;
            background: linear-gradient(90deg, var(--amazon-orange), var(--accent-blue));
        }

        .metric-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.75rem;
        }

        .metric-icon {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            color: var(--amazon-blue);
            background: rgba(255, 153, 0, 0.14);
            font-weight: 800;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-top: 0.85rem;
        }

        .metric-value {
            color: var(--amazon-blue);
            font-size: 1.85rem;
            font-weight: 800;
            margin: 0.15rem 0;
        }

        .metric-change {
            color: var(--success);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .sparkline {
            display: flex;
            align-items: end;
            gap: 3px;
            height: 26px;
            margin-top: 0.65rem;
        }

        .sparkline span {
            display: block;
            width: 8px;
            border-radius: 999px 999px 2px 2px;
            background: linear-gradient(180deg, var(--amazon-orange), var(--accent-blue));
            opacity: 0.78;
            animation: rise 520ms ease both;
        }

        @keyframes rise {
            from { transform: scaleY(0.45); opacity: 0.35; }
            to { transform: scaleY(1); opacity: 0.78; }
        }

        .section-title {
            margin: 1.25rem 0 0.55rem;
            color: var(--amazon-blue);
            font-weight: 800;
            font-size: 1.28rem;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.75rem;
        }

        .insight-card {
            border-left: 5px solid var(--amazon-orange);
        }

        .insight-card p {
            color: #475467;
            opacity: 1;
        }

        .insight-card p b {
            color: var(--amazon-blue);
        }

        .card .badge {
            color: var(--amazon-blue);
            background: #FFFFFF;
            border-color: var(--border);
        }

        .card .status-ok {
            color: var(--success);
            background: rgba(46, 125, 50, 0.08);
            border-color: rgba(46, 125, 50, 0.20);
        }

        .card .priority-high {
            color: var(--danger);
            background: rgba(198, 40, 40, 0.08);
            border-color: rgba(198, 40, 40, 0.18);
        }

        .card .priority-medium {
            color: #9A6700;
            background: rgba(249, 168, 37, 0.12);
            border-color: rgba(249, 168, 37, 0.24);
        }

        .priority-high {
            color: var(--danger);
            background: rgba(198, 40, 40, 0.08);
            border-color: rgba(198, 40, 40, 0.18);
        }

        .priority-medium {
            color: #9A6700;
            background: rgba(249, 168, 37, 0.12);
            border-color: rgba(249, 168, 37, 0.24);
        }

        .product-card {
            display: grid;
            grid-template-columns: 92px 1fr;
            gap: 0.85rem;
            align-items: center;
            color: var(--text);
        }

        .product-card img {
            width: 92px;
            height: 92px;
            object-fit: contain;
            border-radius: 14px;
            background: var(--light-gray);
            border: 1px solid var(--border);
        }

        .progress-track {
            height: 9px;
            border-radius: 999px;
            background: #EEF2F6;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--amazon-orange), var(--accent-blue));
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.35rem;
            box-shadow: 0 8px 24px rgba(35, 47, 62, 0.06);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 0.65rem 0.95rem;
            color: var(--amazon-blue);
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(255, 153, 0, 0.14);
            color: var(--amazon-blue);
        }

        .stDataFrame {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 10px 24px rgba(35, 47, 62, 0.05);
        }

        .sidebar-card {
            padding: 0.9rem;
            border-radius: 16px;
            border: 1px solid var(--border);
            background: #FFFFFF;
            margin-bottom: 0.85rem;
            box-shadow: 0 8px 24px rgba(35, 47, 62, 0.06);
            color: var(--text);
        }

        .sidebar-card,
        .sidebar-card div,
        .sidebar-card p,
        .sidebar-card b {
            color: var(--text);
            opacity: 1;
        }

        .sidebar-card b {
            color: var(--amazon-blue);
        }

        .sidebar-card div {
            color: #475467;
        }

        .footer-note {
            margin-top: 1.5rem;
            padding: 0.9rem 1rem;
            color: var(--muted);
            border-top: 1px solid var(--border);
            font-size: 0.8rem;
            text-align: center;
        }

        @media (max-width: 900px) {
            .top-nav, .status-strip {
                align-items: flex-start;
                justify-content: flex-start;
                flex-direction: column;
            }
            .hero-grid {
                grid-template-columns: 1fr;
            }
            .product-card {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
