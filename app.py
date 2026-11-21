
import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    initialize_database,
    get_connection,
    add_customer,
    add_ticket
)
from support_engine import find_faq_answer, categorize_ticket

st.set_page_config(
    page_title="SupportIQ | Customer Support",
    page_icon="🎧",
    layout="wide"
)

# Initialize database
initialize_database()

# Styling

# Styling
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FC;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stAppViewContainer"] {
    background-color: #F4F7FC;
}

[data-testid="stSidebar"] {
    background-color: #172B4D;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #FFFFFF;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #172B4D;
}

.stButton button {
    border-radius: 8px;
}

/* Dashboard metric visibility */
[data-testid="stMetricLabel"] p {
    color: #64748B !important;
}

[data-testid="stMetricValue"] div {
    color: #172B4D !important;
}

/* Dashboard descriptions */
[data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}

/* Main page labels and descriptions */
[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stWidgetLabel"] p,
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}

/* Text input backgrounds */
[data-testid="stMain"] div[data-baseweb="input"] > div,
[data-testid="stMain"] div[data-baseweb="textarea"] > div,
[data-testid="stMain"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

/* Input text */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea,
[data-testid="stMain"] div[data-baseweb="select"] * {
    color: #172B4D !important;
    background-color: transparent;
}

/* Placeholder text */
[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #94A3B8 !important;
}

/* FIX: Make typed text clearly visible */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    caret-color: #172B4D !important;
}

/* Input placeholders */
[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

/* Dropdown selected value */
[data-testid="stMain"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
}

/* Make Support Assistant answers readable */
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
}

/* Keep captions readable */
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}


</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎧 SupportIQ")
st.sidebar.caption("Customer Support Management")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Support Assistant", "Create Ticket", "Manage Tickets"]
)

# Database helpers
def load_data():
    conn = get_connection()
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    tickets = pd.read_sql_query("""
        SELECT tickets.*, customers.name AS customer_name,
        customers.email AS customer_email
        FROM tickets
        LEFT JOIN customers ON tickets.customer_id = customers.id
        ORDER BY tickets.created_at DESC
    """, conn)
    conn.close()
    return customers, tickets


customers, tickets = load_data()

# Dashboard
if page == "Dashboard":
    st.title("Customer Support Dashboard")
    st.caption("Monitor customer requests and support performance.")

    total = len(tickets)
    open_count = len(tickets[tickets["status"] == "Open"])
    progress_count = len(tickets[tickets["status"] == "In Progress"])
    resolved_count = len(tickets[tickets["status"] == "Resolved"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", total)
    c2.metric("Open Tickets", open_count)
    c3.metric("In Progress", progress_count)
    c4.metric("Resolved", resolved_count)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Tickets by Status")
        if total:
            status_data = tickets["status"].value_counts().reset_index()
            status_data.columns = ["Status", "Count"]
            fig = px.pie(
                status_data,
                names="Status",
                values="Count",
                hole=0.55
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No tickets available yet.")

    with right:
        st.subheader("Tickets by Category")
        if total:
            category_data = tickets["category"].value_counts().reset_index()
            category_data.columns = ["Category", "Count"]
            fig = px.bar(
                category_data,
                x="Category",
                y="Count",
                color="Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Category analytics will appear here.")

    st.subheader("Recent Support Tickets")
    if total:
        st.dataframe(
            tickets[[
                "id", "customer_name", "subject",
                "category", "priority", "status", "created_at"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Create your first support ticket to see dashboard activity.")

# Support Assistant
elif page == "Support Assistant":
    st.title("Support Assistant")
    st.caption("Find answers to common customer questions.")

    question = st.text_input(
        "How can we help you?",
        placeholder="Example: How do I reset my password?"
    )

    if st.button("Find Answer", type="primary"):
        if question.strip():
            result = find_faq_answer(question)

            if result["matched"]:
                st.success("Suggested answer found!")
            else:
                st.warning("No suitable FAQ match found.")

            st.write(result["answer"])
            st.caption(
                f"Suggested category: {result['category']} | "
                f"Match confidence: {result['confidence']}"
            )
        else:
            st.warning("Please enter a question.")

# Create Ticket
elif page == "Create Ticket":
    st.title("Create Support Ticket")
    st.caption("Register a new customer issue.")

    with st.form("ticket_form"):
        name = st.text_input("Customer Name")
        email = st.text_input("Customer Email")
        subject = st.text_input("Ticket Subject")
        description = st.text_area("Describe the Issue")

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Urgent"]
        )

        submitted = st.form_submit_button(
            "Submit Ticket",
            type="primary"
        )

        if submitted:
            if not all([
                name.strip(),
                email.strip(),
                subject.strip(),
                description.strip()
            ]):
                st.error("Please complete all fields.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                category = categorize_ticket(description)

                try:
                    add_customer(name.strip(), email.strip())

                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT id FROM customers WHERE email = ?",
                        (email.strip(),)
                    )
                    customer = cursor.fetchone()
                    conn.close()

                    if customer:
                        add_ticket(
                            customer[0],
                            subject.strip(),
                            description.strip(),
                            category,
                            priority
                        )
                        st.success(
                            f"Ticket created successfully! "
                            f"Suggested category: {category}"
                        )
                        st.rerun()
                    else:
                        st.error("Unable to register customer.")
                except Exception as error:
                    st.error(f"Could not create ticket: {error}")

# Manage Tickets
elif page == "Manage Tickets":
    st.title("Manage Support Tickets")
    st.caption("Review and update customer support requests.")

    if tickets.empty:
        st.info("No support tickets have been created yet.")
    else:
        search = st.text_input("Search by customer or ticket subject")

        filtered = tickets.copy()

        if search.strip():
            filtered = filtered[
                filtered["customer_name"].str.contains(
                    search, case=False, na=False
                )
                | filtered["subject"].str.contains(
                    search, case=False, na=False
                )
            ]

        st.dataframe(
            filtered[[
                "id", "customer_name", "subject",
                "category", "priority", "status", "created_at"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("Update Ticket Status")

        ticket_ids = filtered["id"].tolist()

        if ticket_ids:
            selected_id = st.selectbox("Select Ticket ID", ticket_ids)

            current_status = filtered.loc[
                filtered["id"] == selected_id, "status"
            ].iloc[0]

            statuses = ["Open", "In Progress", "Resolved", "Closed"]

            new_status = st.selectbox(
                "New Status",
                statuses,
                index=statuses.index(current_status)
                if current_status in statuses else 0
            )

            if st.button("Update Status", type="primary"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE tickets SET status = ? WHERE id = ?",
                    (new_status, selected_id)
                )
                conn.commit()
                conn.close()

                st.success("Ticket status updated successfully!")
                st.rerun()

            st.divider()
            st.subheader("Add Resolution Notes")

            existing_notes = filtered.loc[
                filtered["id"] == selected_id,
                "resolution_notes"
            ].iloc[0]

            resolution_notes = st.text_area(
                "Describe the solution provided",
                value=existing_notes if pd.notna(existing_notes) else "",
                placeholder="Enter how the customer's issue was resolved..."
            )

            if st.button("Save Resolution Notes"):
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE tickets SET resolution_notes = ? WHERE id = ?",
                    (resolution_notes, selected_id)
                )

                conn.commit()
                conn.close()

                st.success("Resolution notes saved successfully!")
                st.rerun()

