import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Customer Segmentation Studio",
    page_icon="🛒",
    layout="wide"
)

st.title(" AI Customer Segmentation Studio")

st.markdown("""
Discover hidden customer groups using
machine learning and interactive visualizations.
""")
st.markdown("### Upload your customer dataset and discover hidden customer groups.")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset Uploaded Successfully")

    st.dataframe(df.head())

    

    with st.sidebar:

        st.header("⚙️ Clustering Settings")

        numeric_columns = df.select_dtypes(
        include=["int64","float64"]
        ).columns.tolist()

        selected_features = st.multiselect(
            "Select Features for Clustering",
            numeric_columns,
            default=[
                "Annual Income (k$)",
                "Spending Score (1-100)"
            ]
        )

        k = st.slider(
            "Select Number of Clusters",
            min_value=2,
            max_value=10,
            value=5
        )

        st.markdown("---")

        st.subheader("📊 About")

        st.write("""
        AI Customer Segmentation Studio

        Built using:
        - KMeans
        - Plotly
        - Streamlit
        - Scikit-Learn
        """)

        run_button = st.button(
            "Generate Segments"
        )

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Customers",
        len(df)
    )

    col2.metric(
        "Features",
        len(df.columns)
    )

    col3.metric(
        "Clusters",
        k
    )

    if run_button:
        X = df[selected_features]

        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        from sklearn.cluster import KMeans

        inertias = []

        for i in range(2,11):

            model = KMeans(
                n_clusters=i,
                random_state=42,
                n_init="auto"
            )

            model.fit(X_scaled)

            inertias.append(
                model.inertia_
            )

        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init="auto"
        )

        clusters = kmeans.fit_predict(X_scaled)

        df["Cluster"] = clusters

        cluster_names = {
            0: "Average Customers 👨‍👩‍👧‍👦",
            1: "Premium Customers 💎",
            2: "Young Spenders 🎯",
            3: "Careful Rich Customers 🏦",
            4: "Budget Customers 💵"
        }

        df["Segment"] = df["Cluster"].map(
            cluster_names
        )

        st.success("Customer Segments Generated Successfully")

        st.subheader("📉 Elbow Method")

        import plotly.graph_objects as go

        fig_elbow = go.Figure()

        fig_elbow.add_trace(
            go.Scatter(
                x=list(range(2,11)),
                y=inertias,
                mode="lines+markers"
            )
        )

        fig_elbow.update_layout(
            title="Optimal Number of Clusters",
            xaxis_title="Number of Clusters (K)",
            yaxis_title="Inertia",
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(
            fig_elbow,
            use_container_width=True
        )

        import plotly.express as px

        fig = px.scatter(
            df,
            x=selected_features[0],
            y=selected_features[1],
            color="Segment",
            title="Customer Segments",
            hover_data=[
                "Segment",
                "Age",
                "Annual Income (k$)",
                "Spending Score (1-100)"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=700
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        st.subheader("🧠 Cluster Insights")

        cluster_summary = df.groupby(
                "Segment"
            ).agg(
                {
                    "Age":"mean",
                    "Annual Income (k$)":"mean",
                    "Spending Score (1-100)":"mean"
                }
            ).round(1)

        cluster_names = {}

        for cluster in cluster_summary.index:

            income = cluster_summary.loc[
                cluster,
                "Annual Income (k$)"
            ]

            spending = cluster_summary.loc[
                cluster,
                "Spending Score (1-100)"
            ]

            if income > 70 and spending > 70:
                cluster_names[cluster] = "Premium Customers 💎"

            elif income > 70 and spending < 40:
                cluster_names[cluster] = "Careful Rich Customers 🏦"

            elif income < 40 and spending > 60:
                cluster_names[cluster] = "Young Spenders 🎯"

            elif income < 40 and spending < 40:
                cluster_names[cluster] = "Budget Customers 💵"

            else:
                cluster_names[cluster] = "Average Customers 👨‍👩‍👧‍👦"
                st.dataframe(cluster_summary)

        for segment in cluster_summary.index:

            age = cluster_summary.loc[
                segment,
                "Age"
            ]

            income = cluster_summary.loc[
                segment,
                "Annual Income (k$)"
            ]

            spending = cluster_summary.loc[
                segment,
                "Spending Score (1-100)"
            ]

            st.markdown("---")

            st.subheader(segment)

            st.write(
                f"Average Age: {age}"
            )

            st.write(
                f"Average Income: ${income}k"
            )

            st.write(
                f"Average Spending Score: {spending}"
            )

            if income > 70 and spending > 70:

                st.success(
                    """
                    Premium high-value customers.

                    Recommended strategy:
                    VIP memberships,
                    exclusive offers,
                    premium products.
                    """
                )

            elif income > 70 and spending < 40:

                st.warning(
                    """
                    Wealthy but cautious customers.

                    Recommended strategy:
                    Personalized promotions
                    and premium bundles.
                    """
                )

            elif income < 40 and spending > 60:

                st.info(
                    """
                    Young impulsive spenders.

                    Recommended strategy:
                    Social media marketing,
                    flash sales,
                    influencer campaigns.
                    """
                )

            elif income < 40 and spending < 40:

                st.error(
                    """
                    Budget-conscious customers.

                    Recommended strategy:
                    Discounts,
                    coupons,
                    value packs.
                    """
                )

            else:

                st.write(
                    """
                    Average customers.

                    Recommended strategy:
                    Retention programs
                    and personalized emails.
                    """
                )

        st.subheader("📊 Customer Distribution")

        cluster_counts = (
            df["Segment"]
            .value_counts()
            .reset_index()
        )

        cluster_counts.columns = [
            "Segment",
            "Customers"
        ]

        fig_distribution = px.bar(
            cluster_counts,
            x="Segment",
            y="Customers",
            color="Segment",
            title="Customer Segment Distribution"
        )

        fig_distribution.update_layout(
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(
            fig_distribution,
            use_container_width=True
        )

        csv = df.to_csv(
            index="False"
        ).encode("utf-8")

        st.download_button(
            "Download Segmented Dataset",
            csv,
            "customer_segments.csv",
            "text/csv"
        )

    st.subheader("Preview")
    st.header(df.head())