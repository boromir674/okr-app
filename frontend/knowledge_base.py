import streamlit as st

def knowledge_base_ui():
    """Render the Knowledge Base UI."""
    st.header("Knowledge Base")
    tabs = st.tabs(["What is OKR?", "Examples & Use Cases"])

    with tabs[0]:
        st.markdown("""
        # What is OKR?

        ## Overview
        Objectives and Key Results (OKR) is a goal-setting framework used by individuals, teams, and organizations to define measurable goals and track their outcomes. It was popularized by Andrew Grove at Intel in the 1970s and later adopted by companies like Google, LinkedIn, and Microsoft.

        ### Components of OKR
        1. **Objective**: A significant, concrete, and clearly defined goal. Objectives should be inspirational and action-oriented.
        2. **Key Results**: Measurable success criteria used to track the achievement of the objective. Key results should be specific, measurable, and free of ambiguity.

        ### History
        - **1970s**: Andrew Grove introduced OKRs at Intel.
        - **1999**: John Doerr introduced OKRs to Google, where they became central to the company's culture.
        - **2018**: Doerr published *Measure What Matters*, explaining the OKR framework.

        ### Best Practices
        - Define a small set of OKRs ("Less is more").
        - Focus on outcomes, not outputs.
        - Use leading indicators for key results to enable course correction.
        - Avoid vague terms like "help" or "consult" in objectives.

        ## Why Use OKRs?
        OKRs help organizations:
        - Align efforts across teams.
        - Focus on measurable progress.
        - Encourage ambitious yet achievable goals.

        ## Differences Between Objectives and Key Results
        | **Aspect**       | **Objective**                     | **Key Result**                  |
        |-------------------|-----------------------------------|----------------------------------|
        | **Definition**    | A significant goal to achieve.   | Measurable criteria for success.|
        | **Nature**        | Inspirational and action-oriented.| Specific and quantifiable.      |
        | **Example**       | "Increase customer satisfaction."| "Achieve a Net Promoter Score of 80%." |
        """)

    with tabs[1]:
        st.markdown("""
        # Examples & Use Cases

        ## Examples of OKRs

        ### Example 1: Marketing Team
        **Objective**: Increase brand awareness.
        **Key Results**:
        1. Achieve 50,000 social media followers.
        2. Publish 10 blog posts with 1,000+ views each.
        3. Generate 5,000 website visits from organic search.

        ### Example 2: Product Development Team
        **Objective**: Launch a new product successfully.
        **Key Results**:
        1. Complete product development by Q3.
        2. Achieve 90% customer satisfaction in beta testing.
        3. Generate $100,000 in revenue within the first month.

        ### Example 3: Sales Team
        **Objective**: Improve sales performance.
        **Key Results**:
        1. Close 50 new deals in Q2.
        2. Achieve $1M in revenue.
        3. Reduce customer churn rate to below 5%.

        ## Use Cases
        1. **Startups**: Align teams on critical goals during early growth stages.
        2. **Large Organizations**: Ensure cross-functional alignment and focus on measurable outcomes.
        3. **Personal Development**: Set and track personal goals, such as fitness or learning objectives.

        ## Benefits of OKRs
        - Encourages ambitious goal-setting.
        - Provides clarity and focus.
        - Enables regular progress tracking.
        - Promotes accountability and transparency.

        ## Criticism
        - Individual-level OKRs can resemble task lists and may not be effective.
        - Overuse of OKRs at multiple levels can lead to a waterfall approach, which is counterproductive.
        """)
