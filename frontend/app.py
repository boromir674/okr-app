import typing as t
import streamlit as st
import requests
import json
import os


BASE_URL = os.environ['OKR_BACKEND_URL']


from knowledge_base import knowledge_base_ui


def main():
    """Main function to render the Streamlit UI."""
    st.title("OKR Management Application")
    st.sidebar.title("Navigation")
    options = ["Dashboard", "Objectives", "Key Results", "Knowledge Base"]
    choice = st.sidebar.radio("Choose a section", options)

    if choice == "Dashboard":
        dashboard_ui()
    elif choice == "Objectives":
        objectives_ui()
    elif choice == "Key Results":
        key_results_ui()
    elif choice == "Knowledge Base":
        knowledge_base_ui()


from key_results_card import KeyResultsCard

response = None

def start_up_query():
    """Initial query to fetch objectives."""
    # Fetch the first 4 objectives to display in the dashboard
    global response
    if not response:
        # Make a GET request to fetch objectives
        response = requests.get(f"{BASE_URL}/objectives/")
    return response

# OKR Dashboard
def dashboard_ui():
    """Render the Dashboard UI."""
    # RENDER
    st.header("Dashboard: Recent Objectives")
    response = start_up_query()
    if response.status_code == 200:
        objectives = response.json()
        # Display top 4 objectives in a grid layout
        first_slice = (0, 2)
        second_slice = (2, 4)
        slices  = (first_slice, second_slice)
        for y in range(2):
            cols = st.columns(2)
            for i, obj in enumerate(objectives[slices[y][0]:slices[y][1]]):
                with cols[i]:
                    # RENDER Objective Name
                    st.subheader(obj["name"])
                    # RENDER Objective Description as expander
                    with st.expander("Description"):
                        st.write(obj["description"])
                    # RENDER expander, which pushes elemnt below in grid when opened !
                    with st.expander("Key Results"):

                        key_results_response = requests.get(f"{BASE_URL}/key_results/")

                        if key_results_response.status_code == 200:

                            all_key_results_in_db = key_results_response.json()
                            key_results_of_current_objective = sorted([kr for kr in all_key_results_in_db if kr["objective_id"] == obj["id"]], 
                                                                      key=lambda x: x["id"], reverse=False)

                            # Key Results Card Component
                            # Render Key Results Card for Objective
                            key_results_card = KeyResultsCard(st, key_results_of_current_objective)
                            key_results_card.render()
                        else:
                            st.error(f"Failed to fetch key results: {key_results_response.status_code} - {key_results_response.text}")
    else:
        st.error(f"Failed to fetch objectives: {response.status_code} - {response.text}")


# Objectives CRUD UI
def objectives_ui():
    """Render the Objectives section UI."""
    st.header("Manage Objectives")

    # RENDER: Create Objective Section
    st.subheader("Create Objective")
    
    # CREATE UI for Objective
    title = st.text_input("Title")
    description = st.text_area("Description")

    # Nested Key Result Creation/Attachment
    st.markdown("##### Key Results")

    # Server Data Fetching
    response = start_up_query()
    if response.status_code == 200:
        objectives = response.json()

    ### STATE management ###
    # the list of KRs is always empty at first, in the Create New Objective flow 
    if "key_results_for_objective" not in st.session_state:
        st.session_state["key_results_for_objective"] = []

    # Initialize session state from Server Data, for each Key Result under each Objective
    from objectives_state import ObjectivesState
    state = ObjectivesState(objectives=objectives)
    flat_state_iterator = iter(state.iter_state())
    for objective in objectives:
        # add Objective 'name'
        key, value = next(flat_state_iterator)
        if key not in st.session_state:
            st.session_state[key] = value

        # add Objective 'description'
        key, value = next(flat_state_iterator)
        if key not in st.session_state:
            st.session_state[key] = value

        for kr in objective.get("key_results", []):
            # KR Short Description
            key, value = next(flat_state_iterator)
            if key not in st.session_state:
                st.session_state[key] = value
            # KR Description
            key, value = next(flat_state_iterator)
            if key not in st.session_state:
                st.session_state[key] = value
    ### STATE end ###

    # RENDER newyly added KR items for 'Create new Objective' flow, from session state data
    from key_result_to_add_to_objective import KeyResultItemSelectedForObjectiveUnderConstruction as KRI
    c = st.container()
    with c:
        for i, kr in enumerate(st.session_state["key_results_for_objective"]):
            col1, col2 = st.columns([4, 1])
            key_result_item = KRI(st, kr)
            with col1:
                key_result_item.render()
            with col2:
                if st.button("Remove", key=f"remove_{kr['id']}"):
                    st.session_state["key_results_for_objective"].remove(kr)
                    st.success(f"Key Result '{kr['short_description']}' removed from Objective!")
                    st.rerun()

        # RENDER ADD KEY RESULT button which opens Popover
        with st.popover("Add Key Result"):
            from key_result_item_creation_ui import KeyResultItemEditUI as KRI_UI
            key_result_crud_ui = KRI_UI(st)
            elements: t.List = key_result_crud_ui.render()

            # Add and Clear buttons
            cols = st.columns([1, 1], gap="small")
            import uuid
            with cols[0]:
                if st.button("Add", key="add_new_key_result"):
                    new_kr = {
                        "id": uuid.uuid4().hex,
                        "short_description": elements[4],
                        "description": elements[0],
                        "progress": elements[1],
                        "metric": elements[2],
                        "unit": elements[3],  # Include unit value
                    }
                    st.session_state["key_results_for_objective"].append(new_kr)
                    st.success("New Key Result added to Objective!")
                    st.rerun()
            with cols[1]:
                if st.button("Clear", key="clear_key_results"):
                    for el in elements:
                        del el
                    st.rerun()

    # RENDER CREATE OBJECTIVE BUTTON: Create Objective and Nested Key Results
    if st.button("Create Objective"):
        payload = {"name": title, "description": description}
        response = requests.post(f"{BASE_URL}/objectives", 
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))
        if response.status_code == 200:
            new_objective = response.json()
            st.success("Objective created successfully!")

            for kr in st.session_state["key_results_for_objective"]:
                kr_payload = {
                    "objective_id": new_objective["id"],
                    "short_description": kr["short_description"],
                    "description": kr["description"],
                    "progress": kr["progress"],
                    "metric": kr["metric"],
                    "unit": kr["unit"],  # Persist unit value
                }
                kr_response = requests.post(f"{BASE_URL}/key_results",
                                            headers={"Content-Type": "application/json"},
                                            data=json.dumps(kr_payload))
                if kr_response.status_code == 200:
                    st.success(f"Key Result '{kr['short_description']}' added successfully!")
                else:
                    st.error(f"Failed to add Key Result '{kr['short_description']}': {kr_response.status_code} - {kr_response.text}")

            st.session_state["key_results_for_objective"] = []
            st.rerun()
        else:
            st.error(f"Failed to create objective: {response.status_code} - {response.text}")

    # RENDER Catalog of Objectives
    st.subheader("Catalog of Objectives")

    # # Fetch objectives
    # objectives_response = requests.get(f"{BASE_URL}/objectives/")
    # if objectives_response.status_code == 200:
    #     objectives = objectives_response.json()
    # else:
    #     st.error(f"Failed to fetch objectives: {objectives_response.status_code} - {objectives_response.text}")
    #     return

    # Fetch key results for mapping
    key_results_response = requests.get(f"{BASE_URL}/key_results/")
    key_results_map = {}
    if key_results_response.status_code == 200:
        key_results = key_results_response.json()
        for kr in key_results:
            if kr["objective_id"] not in key_results_map:
                key_results_map[kr["objective_id"]] = []
            key_results_map[kr["objective_id"]].append(kr)
    else:
        st.error(f"Failed to fetch key results: {key_results_response.status_code} - {key_results_response.text}")
        return

    # CSS for hover effect and styling
    st.markdown("""
    <style>
    .objective-item {
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 8px;
        transition: box-shadow 0.3s ease;
    }
    .objective-item:hover {
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    }
    .objective-item:nth-child(even) {
        background-color: #f9f9f9;
    }
    .objective-item:nth-child(odd) {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

    # Iteratively Render objectives from state data, in a catalog-style layout
    for objective_id, objective_dict in state:
        
        obj_name = objective_dict.get("name", "")
        description = objective_dict.get("description", "")

        # Render Editable Objective Name
        obj_name = st.text_input(
            f"Objective Name (ID: {objective_id})",
            value=obj_name,

            on_change=state.set_objective_name_state_adapted,
            args=(lambda: st.session_state.get(f"edit_obj_name_{objective_id}", obj_name),),

            key=f"edit_obj_name_{objective_id}"
        )

        # Render Editable Objective Description
        obj_description = st.text_area(
            f"Objective Description (ID: {objective_id})",
            value=description,

            on_change=state.set_objective_description_state_adapted,
            args=(lambda: st.session_state.get(f"edit_obj_description_{objective_id}", description),),

            key=f"edit_obj_description_{objective_id}"
        )

        # Render Save Button for changes to Objective
        if st.button(f"Save Objective Changes (ID: {objective_id})", key=f"save_obj_changes_{objective_id}"):
            payload = {"name": obj_name, "description": obj_description}
            response = requests.put(f"{BASE_URL}/objectives/{objective_id}", 
                                    headers={"Content-Type": "application/json"},
                                    data=json.dumps(payload))
            if response.status_code == 200:
                st.success(f"Objective '{obj_name}' updated successfully!")
                # st.rerun()
            else:
                st.error(f"Failed to update objective: {response.status_code} - {response.text}")

        # Iteratively Render Key Results for the Objective
        if objective_id in key_results_map:  # uses a new server data request (can be avoided if all app uses the same state keys for nesting obj and krs)
            for kr in key_results_map[objective_id]:
                # Editable fields for Key Result
                kr_short_description = st.text_input(f"Key Result Title (ID: {kr['id']})", value=kr.get('short_description', ''), key=f"edit_kr_title_{kr['id']}")
                kr_description = st.text_area(f"Key Result Description (ID: {kr['id']})", value=kr['description'], key=f"edit_kr_description_{kr['id']}")

                # Save changes to Key Result
                if st.button(f"Save Key Result Changes (ID: {kr['id']})", key=f"save_kr_changes_{kr['id']}"):
                    kr_payload = {
                        "short_description": kr_short_description,
                        "description": kr_description,
                    }
                    kr_response = requests.put(f"{BASE_URL}/key_results/{kr['id']}",
                                               headers={"Content-Type": "application/json"},
                                               data=json.dumps(kr_payload))
                    if kr_response.status_code == 200:
                        st.success(f"Key Result '{kr_short_description}' updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update Key Result: {kr_response.status_code} - {kr_response.text}")
        else:
            st.write("No Key Results available for this Objective.")

        # Add visual separation between Objectives
        st.markdown("---")

    # Delete Objective
    st.subheader("Delete Objective")
    objective_id = st.number_input("Objective ID", min_value=1, step=1, value=None)
    # Show Objective to be deleted, given ID (state)
    if objective_id:
        response = requests.get(f"{BASE_URL}/objectives/{objective_id}")
        if response.status_code == 200:
            objective = response.json()
            st.write(f"Objective to be deleted: {objective['name']} - {objective['description']}")
        else:
            st.error(f"Failed to fetch objective: {response.status_code} - {response.text}")
    # Delete button
    if st.button("Delete Objective"):
        response = requests.delete(f"{BASE_URL}/objectives/{objective_id}")
        if response.status_code == 200:
            st.success("Objective deleted successfully!")
        else:
            st.error(f"Failed to delete objective: {response.status_code} - {response.text}")


# Key Results CRUD UI
def key_results_ui():
    """Render the redesigned Key Results section UI."""
    st.header("Manage Key Results")
    
    # Create Key Result
    st.subheader("Create Key Result")
    objective_id = st.number_input("Objective ID", min_value=1, step=1)
    description = st.text_area("Description")
    short_description = st.text_input("Title / Short Description")
    progress = st.slider("Progress", min_value=0, max_value=100, step=1)
    metric = st.text_input("Metric (Optional)")
    unit = st.number_input("Unit (Optional)", min_value=1, max_value=99, step=1, value=1)  # Add unit input
    if st.button("Create Key Result"):
        payload = {
            "objective_id": objective_id,
            "description": description,
            "short_description": short_description,
            "progress": progress,
            "metric": metric,
            "unit": unit,  # Persist unit value
        }
        response = requests.post(
            f"{BASE_URL}/key_results",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        if response.status_code == 200:
            st.success("Key Result created successfully!")
        else:
            st.error(f"Failed to create key result: {response.status_code} - {response.text}")


    # READ Key Results
    st.subheader("Catalog of Key Results")
    
    # Fetch objectives for mapping
    objectives_response = requests.get(f"{BASE_URL}/objectives/")
    objectives_map = {}
    if objectives_response.status_code == 200:
        objectives = objectives_response.json()
        objectives_map = {obj["id"]: obj["name"] for obj in objectives}
    else:
        st.error(f"Failed to fetch objectives: {objectives_response.status_code} - {objectives_response.text}")

    # Fetch key results
    response = requests.get(f"{BASE_URL}/key_results/")
    if response.status_code == 200:
        key_results = response.json()

        # CSS for hover effect and styling
        st.markdown("""
        <style>
        .key-result-item {
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 8px;
            transition: box-shadow 0.3s ease;
        }
        .key-result-item:hover {
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        }
        .key-result-item:nth-child(even) {
            background-color: #f9f9f9;
        }
        .key-result-item:nth-child(odd) {
            background-color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

        # Render key results in a catalog-style layout
        for kr in key_results:
            objective_name = objectives_map.get(kr["objective_id"], "Unknown Objective")
            st.markdown(f"""
            <div class="key-result-item">
                <h3>{kr.get('short_description')}</h3>
                <h4>{kr['description']}</h4>
                <p><strong>Progress:</strong> {kr['progress']}%</p>
                <p><strong>Objective:</strong> {objective_name}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"Failed to fetch key results: {response.status_code} - {response.text}")

    # Delete Key Result
    st.subheader("Delete Key Result")
    key_result_id = st.number_input("Key Result ID", min_value=1, step=1)
    if st.button("Delete Key Result"):
        response = requests.delete(f"{BASE_URL}/key_results/{key_result_id}")
        if response.status_code == 200:
            st.success("Key Result deleted successfully!")
        else:
            st.error(f"Failed to delete key result: {response.status_code} - {response.text}")


if __name__ == "__main__":
    main()
