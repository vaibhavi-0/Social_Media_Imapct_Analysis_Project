import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  PAGE SETTINGS
st.set_page_config(page_title="Social Media Addiction Analysis", layout="wide")

# LOAD DATA 
df = pd.read_csv("Cleaned_Social_Media_Addiction.csv")

# SIDEBAR 
st.sidebar.title("Social Media Analysis")

section = st.sidebar.radio(
   "Pick Analysis",
    [
        "Introduction",
        "Exploratory Data Analysis (EDA)",
        "Social Media Usage",
        "Platform Usage",
        "Usage vs Mental Health",
        "Age Group vs Addiction Score",
        "Academic Impact",
        "Academic Impact vs Usage",
        "Conflicts vs Mental Health",
        "Key Insights",
        "Final Conclusion"
    ]
)

# INTRODUCTION 
if section == "Introduction":
    st.title("📊 Social Media Addiction Impact Analysis")
    st.markdown("""
    Social media plays a major role in students’ daily lives for communication,
    learning, and entertainment. However, **excessive usage can lead to addiction**,
    which may negatively affect **mental health, sleep patterns, and academic performance**.

    This project analyzes the **impact of social media addiction on students**
    using real-world data to understand how prolonged usage influences
    their well-being and academic outcomes.
    """)

#  EDA 
elif section == "Exploratory Data Analysis (EDA)":
    st.header("🔍 Exploratory Data Analysis")
    st.subheader("📌 Basic Dataset Summary")
    st.write(df.describe())

    avg_usage = df["Avg_Daily_Usage_Hours"].mean()
    max_usage = df["Avg_Daily_Usage_Hours"].max()
    avg_addiction = df["Addicted_Score"].mean()

    st.markdown(f"""
    **📌 Conclusion from Dataset Summary:**  
    - Average daily social media usage: **{avg_usage:.2f} hours** (max: {max_usage} hours).
    - Average addiction score: **{avg_addiction:.2f}**, with many students in the moderate-to-high range. 
    - Sleep hours are often below the healthy 7–8 hours.  
    - Mental-health scores vary widely among students. 
    - Some students report conflicts or academic problems linked to social media. 
    """)

    #  CORRELATION HEATMAP
    st.subheader("📈 Correlation Heatmap of Key Numeric Features")
    numeric_cols = ["Avg_Daily_Usage_Hours", "Addicted_Score", "Sleep_Hours_Per_Night", "Mental_Health_Score"]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

    st.subheader("✅ Conclusions from Correlation Analysis")
    st.markdown("""
    - **Addicted_Score vs Avg_Daily_Usage_Hours:** Strong positive correlation → more usage increases addiction.  
    - **Addicted_Score vs Sleep_Hours_Per_Night:** Strong negative correlation → higher addiction reduces sleep.  
    - **Addicted_Score vs Mental_Health_Score:** Moderate negative correlation → higher addiction worsens mental health.  
    - **Sleep_Hours_Per_Night vs Mental_Health_Score:** Positive correlation → better sleep improves mental wellbeing.  
    """)

    # ADDICTION SCORE DISTRIBUTION
    st.subheader("📊 Distribution of Addiction Scores")
    fig, ax = plt.subplots()
    sns.histplot(df["Addicted_Score"], bins=20, kde=True, ax=ax, color='skyblue')
    ax.set_xlabel("Addiction Score")
    ax.set_title("Distribution of Addiction Scores")
    st.pyplot(fig)

    st.success("Most students fall in the **moderate-to-high addiction range**, meaning frequent use is very common.")

    #DAILY USAGE DISTRIBUTION 
    st.subheader("⏳ Distribution of Daily Usage Hours")
    fig, ax = plt.subplots()
    sns.histplot(df["Avg_Daily_Usage_Hours"], bins=20, kde=True, ax=ax, color='salmon')
    ax.set_xlabel("Daily Usage (Hours)")
    ax.set_title("Distribution of Daily Social Media Usage Hours")
    st.pyplot(fig)

    st.success("Many students spend **multiple hours daily on social media**, showing heavy usage is part of everyday life.")

#  SOCIAL MEDIA USAGE
elif section == "Social Media Usage":
    st.header("🌍 Social Media Usage Patterns")
    country_usage = df.groupby("Country")["Avg_Daily_Usage_Hours"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=country_usage.index, y=country_usage.values, ax=ax, palette="viridis")
    ax.set_xlabel("Country")
    ax.set_ylabel("Average Usage (Hours)")
    ax.set_title("Top 10 Countries by Average Daily Social Media Usage")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.success("Average social-media use **differs across countries**, likely due to lifestyle, internet access, and culture.")

#  PLATFORM USAGE
elif section == "Platform Usage":
    st.header("📱 Platform Usage Distribution")

    platform_counts = df["Most_Used_Platform"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(platform_counts, labels=platform_counts.index, autopct='%1.1f%%',
           startangle=5, textprops={'fontsize': 8},
           colors=sns.color_palette("pastel"))
    ax.set_title("Most Used Social Media Platforms")
    st.pyplot(fig)

    st.success("Platforms like **Instagram, WhatsApp, and TikTok are the most commonly used**, showing students prefer fast, engaging content.")

# USAGE vs MENTAL HEALTH 
elif section == "Usage vs Mental Health":
    st.header("🧠 Usage Hours vs Mental Health Score")

    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df,
        x="Avg_Daily_Usage_Hours",
        y="Mental_Health_Score",
        hue="Addicted_Score",
        palette="coolwarm",
        ax=ax
    )
    ax.set_xlabel("Daily Usage (Hours)")
    ax.set_ylabel("Mental Health Score (1–10)")
    ax.set_title("Daily Usage vs Mental Health Score")
    st.pyplot(fig)

    st.success("As daily social-media use **increases**, students generally report **lower mental-health scores.**")

# AGE GROUP vs ADDICTION 
elif section == "Age Group vs Addiction Score":
    st.header("👥 Age Group vs Addiction Score")

    # Group by Age (or Age_Group if present)
    if "Age_Group" in df.columns:
        age_addiction = df.groupby("Age_Group")["Addicted_Score"].mean().reset_index()
        x_col = "Age_Group"
    else:
        age_addiction = df.groupby("Age")["Addicted_Score"].mean().reset_index()
        x_col = "Age"

    fig, ax = plt.subplots()
    sns.barplot(
        data=age_addiction,
        x=x_col,
        y="Addicted_Score",
        palette="coolwarm",
        ax=ax
    )

    ax.set_xlabel(x_col.replace("_", " "))
    ax.set_ylabel("Average Addiction Score")
    ax.set_title("Average Addiction Score Across Age Groups")
    st.pyplot(fig)

    st.success(
        "Different age groups show variation in addiction scores, with **younger students (around 18)** showing the highest addiction levels."
    )

# ACADEMIC IMPACT 
elif section == "Academic Impact":
    st.header("📚 Academic Impact vs Addiction Score")

    fig, ax = plt.subplots()
    sns.boxplot(
        data=df,
        x="Affects_Academic_Performance",
        y="Addicted_Score",
        ax=ax,
        palette="Set2"
    )
    ax.set_xlabel("Academic Impact (0 = No, 1 = Yes)")
    ax.set_ylabel("Addiction Score")
    ax.set_title("Academic Impact vs Addiction Score")
    st.pyplot(fig)

    st.success("Students who report **academic problems usually have higher addiction scores.**")

#  ACADEMIC IMPACT vs USAGE
elif section == "Academic Impact vs Usage":
    st.header("🎓 Academic Impact vs Daily Usage")

    fig, ax = plt.subplots()
    sns.boxplot(
        data=df,
        x="Affects_Academic_Performance",
        y="Avg_Daily_Usage_Hours",
        ax=ax,
        palette="Set3"
    )
    ax.set_xlabel("Academic Impact (0 = No, 1 = Yes)")
    ax.set_ylabel("Daily Usage (Hours)")
    ax.set_title("Academic Impact vs Daily Social Media Usage")
    st.pyplot(fig)

    st.success("Students whose academics are affected **spend more time daily on social media.**")

#  CONFLICTS vs MENTAL HEALTH 
elif section == "Conflicts vs Mental Health":
    st.header("⚠️ Conflicts vs Mental Health Score")

    fig, ax = plt.subplots()
    sns.barplot(
        data=df,
        x="Conflicts_Over_Social_Media",
        y="Mental_Health_Score",
        palette="coolwarm",
        ci=None,
        ax=ax
    )
    ax.set_xlabel("Conflicts (0 = Never, 5 = Very Frequent)")
    ax.set_ylabel("Average Mental Health Score")
    ax.set_title("Average Mental Health Score by Conflict Status")
    st.pyplot(fig)

    st.success("Students who **face more conflicts due to social media generally report lower mental-health scores.**")

# KEY INSIGHTS 
elif section == "Key Insights":
    st.header("📌 Key Insights")
    st.markdown("""
    - More usage → **higher addiction**
    - Higher addiction → **less sleep & poorer mental health**
    - Poor sleep → **lower wellbeing**
    - Heavy users → **more academic problems**
    - Social conflicts → **worse mental health**
    """)

# FINAL CONCLUSION
elif section == "Final Conclusion":
    st.header("✅ Final Conclusion")
    st.markdown("""
    Social media is an important part of modern student life. However,
    **excessive usage leads to addiction**, which negatively impacts:

    ✔️ Sleep  
    ✔️ Mental Health  
    ✔️ Academic Performance   

    📌 **Balanced and mindful social media use is essential for a healthy lifestyle.**
    """)


