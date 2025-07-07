import streamlit as st

def knowledge_base_ui():
    """Render the Knowledge Base UI."""
    st.header("Knowledge Base")
    tabs = st.tabs(["Cheatsheet", "What is OKR?", "Examples & Use Cases"])

    with tabs[0]:
        st.markdown("""
        # OKR Cheatsheet

        > Objectives and Hey Results

        ## What is it?
        
        - Is management technique for recurring planning and progress reporting
        - Connects team and personal objectives to measurable results, making people move together in right direction
        - Helps keep vision, goals, and objcetives always in front of people
        - People get clarity of knowing what's expected from them

        ## Definitions

        - **Objectives (Os)**
            - It is what you want to achieve
            - Quarterly (but for junior individual contributors can be monthly)
            - Must be measurable with one or a few KRs
            - Can be Operational or Aspirational
            - Must be able to pass/cascade down or across for alignment

        - **Key Results (KRs)**
            - It is how you will know whether you are achieving your objective
            - It is the metric which measures the Objective (Complete/Incomplete is measurable)
            - If it's not a metric then the KR is a Milestone (date when the Objective is due)

        - **Tactics**
            - KRs inform the “What” while Tactics inform the “How”
            - Should be planned for each Key Result

        ## Structure

        Planned and monitored continuously

        - **Objectives (Os)**:
          - max 3-5 per person at a time
          - Qualititative

            - EG: Build X skill within the team by Dec 14'

        - **Key Result**:
          - max 3 per Objective
          - Quantitative

            - EG: Do a PoC to showcase capability on X

        ## Paradigm
        
        I will {Objective} as measured by {Key Results}

        ## Best Practices

        - Objectives must contribute to the organization goals - *directly or indirectly*
        - Objectives must be ambitious - A 60-70% achievemtn is considered good, a 100% achievement means it wasn't challenging enough
        - 3-5 objectives - alive at any given point in time
        - Up to 3 Key Results to contribute towards each Objective

        ## Implementation Guidance

        - OKRs should be part of your role profile / day-to-day work - not outside of what you do but not routine also
        - Keep OKRs sizable - don't slice them down to specifics
        - On-going OKRs - may not have KR end date, but should still be measurable
        - Growth focused - focus on building yourself, not completing the OKRs
        - **Ambitious** - *goals must be uncomfortable and hard to achieve*
        - **Each OKR must be of a sizable duration** - *pick a duration that your "you yourself/team/company" can comfortably measure*
        - **End date is important** - *keep it tagged on your desk*
        - **OKRs are live** - *do not type-in and forget*
        - **OKRs must be reviewed (ie by people/managers) periodically** - (corpo: *usually every month or every quarter*)

        - Operational vs. Aspirational • OKRs should not all be unachievable as some OKR experts suggest -many can be "Operational" and thus achievable, despite being “stretch goals” • If the implication is that achieving 70%-80% consistently should be considered a good outcome then it will become quickly demotivating to everyone that they are always ending up hitting 70%-80% of the aim
        - Writing OKRs - The Importance of Language • Phrase OKRs in the language relevant to the targeted group • Use action verbs to start each O or KR -All KRs should be actionable verb as it makes it more clear and more actionable when cascaded down as an Objective • When in doubt use experimental phrases to improve baseline: -Complete X experimental lead generation projects in Q1 to grow lead flow -Complete X of PR Projects in Q1 to improve brand awareness -Invest 10% of time each week into non-measurable, experimental, “serendipitous” marketing
        - Keep In Mind • You don't know what you don't know -Can't anticipate everything - need to acknowledge that there are many unknowns -Planning is by definition done in the past with what you knew at the time • Running experiments is critical -It's necessary to increase performance over time • You may achieve every KR, while not every Objective -That's OK as long as you are learning and can apply the learnings in the next quarter • It's OK to fail -But it's important to plan thoughtfully in advance, then analyze the gap in a retrospective assessment (as aforementioned, the Owner / DRI is responsible for this) and plan for the next quarter using the insights
        - Grading • Purpose: for learnings and improvements, not for performance evaluation • After the end of the quarter, each DRI grades Key Results from 0 to 1 • Key Result Grade is not the same as KR measurement - If your company discovered that a given KR had little business value and stopped it mid- quarter, you have still achieved a good business outcome and deserve a high grade • Objective’s grade is an average of KR grades • Grade of 1.0 for Objective is reasonable for operational objectives and grade of 0.7-0.8 is good for “aspirational” - Encourage setting ambitious objectives when possible for the following quarters • Always base employee evaluations on KR metrics and never on OKR grades

        """)

    with tabs[1]:
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

    with tabs[2]:
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
