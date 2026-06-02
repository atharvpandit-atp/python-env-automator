import streamlit as st
import os
import sys
import platform

st.set_page_config(page_title="DevEnv Automator", page_icon="⚙️", layout="centered")

st.title("⚙️ Developer Environment Automator")
st.write("This tool automates your local workspace setup, generating standard directory structures, dependency tracking, and configuration files.")

st.divider()

# Interactive configuration inputs for the user
st.subheader("1. Configure Your Setup")
project_name = st.text_input("Target Project Name (Folder)", value="my_new_ai_project")

# Multi-select for dynamic directory creation
selected_dirs = st.multiselect(
    "Select Directories to Create:",
    ['src', 'tests', 'docs', 'logs', 'notebooks', 'config'],
    default=['src', 'tests', 'docs', 'logs']
)

# Text area to let the user customize their starter packages
packages_input = st.text_area(
    "Starter Packages (one per line):",
    value="numpy==1.26.4\npandas==2.2.2\nscikit-learn==1.5.0\nstreamlit"
)

st.divider()
st.subheader("2. Execute Automation")

if st.button("Build Environment", type="primary"):
    with st.spinner("Executing setup scripts..."):
        # Create a container to capture log outputs
        log_container = st.container()
        has_error = False
        
        # Target path inside the current execution directory
        target_path = os.path.join(os.getcwd(), project_name)
        
        # 1. Check Python Version
        current_version = sys.version_info
        version_str = platform.python_version()
        if current_version >= (3, 8):
            st.success(f"✔ Python Version Check: Passed (Detected {version_str})")
        else:
            st.error(f"❌ Python Version Check: Failed (Requires 3.8+, detected {version_str})")
            has_error = True

        if not has_error:
            try:
                # 2. Create Directory Structure
                for folder in selected_dirs:
                    path = os.path.join(target_path, folder)
                    os.makedirs(path, exist_ok=True)
                st.success(f"✔ Directory Structure Created inside `/{project_name}`")

                # 3. Generate requirements.txt
                req_path = os.path.join(target_path, "requirements.txt")
                with open(req_path, "w") as f:
                    f.write(packages_input)
                st.success("✔ `requirements.txt` written successfully.")

                # 4. Generate .gitignore
                gitignore_path = os.path.join(target_path, ".gitignore")
                gitignore_content = "__pycache__/\n*.py[cod]\nvenv/\n.venv/\nlogs/\n*.log\n.env\n"
                with open(gitignore_path, "w") as f:
                    f.write(gitignore_content)
                st.success("✔ `.gitignore` file initialized.")
                
                st.balloons()
                st.toast("Environment setup successfully created!")
                
            except Exception as e:
                st.error(f"Critical execution failure: {e}")

st.sidebar.markdown("### System Specs")
st.sidebar.info(f"OS: {platform.system()} {platform.release()}\n\nPython: {platform.python_version()}")