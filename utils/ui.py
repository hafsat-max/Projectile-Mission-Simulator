import streamlit as st


def formula_line(title: str, formula: str, color: str = "#38bdf8") -> None:
    st.markdown(
        f"""
        <p style="margin-bottom: 0.8rem;">
            <strong>{title}:</strong>
            <span style="color: {color}; font-weight: 700;">{formula}</span>
        </p>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, color: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 5px solid {color};">
            <p class="metric-title">{title}</p>
            <h3 style="color: {color};">{value}</h3>
            <p class="metric-note">{note}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )