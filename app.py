import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai import LLM
import os

st.set_page_config(page_title="A&R Flash", page_icon="🔥")

st.title("🔥 A&R Flash")
st.write("AI Trend Scout for Arabic Pop")

google_api_key = st.text_input("Enter Gemini API Key", type="password")

if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key

    llm = LLM(
        model="gemini-1.5-flash",
        temperature=0.7
    )

    trend_scout = Agent(
        role="Trend Scout",
        goal="Generate 10 fresh Arabic pop song concepts for youth 17-24 in Arab Israel optimized for TikTok virality.",
        backstory="You are a sharp A&R trend spotter. Output Arabic only.",
        llm=llm,
        verbose=False
    )

    ar_judge = Agent(
        role="A&R Judge",
        goal="Select TOP 3 most viral ideas and score them for TikTok/Live/Spotify, then give short production briefs.",
        backstory="You are a commercial A&R. Output Arabic only.",
        llm=llm,
        verbose=False
    )

    task_ideas = Task(
        description="Generate ideas",
        agent=trend_scout
    )

    task_judge = Task(
        description="Evaluate ideas",
        agent=ar_judge
    )

    crew = Crew(
        agents=[trend_scout, ar_judge],
        tasks=[task_ideas, task_judge],
        process=Process.sequential
    )

    if st.button("Generate A&R Report"):
        with st.spinner("Cooking hits... 🔥"):
            result = crew.kickoff()
            st.success("Done!")
            st.write(result)
