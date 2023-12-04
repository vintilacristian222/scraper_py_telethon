import streamlit as st
import json


# Function to load and save Telegram settings
def load_telegram_settings():
    with open("telegram_settings.json", "r") as file:
        return json.load(file)


def save_telegram_settings(settings):
    with open("telegram_settings.json", "w") as file:
        json.dump(settings, file, indent=4)


# Load existing Telegram settings
telegram_settings = load_telegram_settings()

st.title("Telegram Channel Configuration")

# Channel Operation Selection
operation = st.radio("Choose Operation", ["Add New Channel", "Edit Existing Channel", "Delete Channel"])

if operation == "Add New Channel":
    new_channel_id = st.text_input("New Channel ID")
    new_specific_words = st.text_area("Specific Words (comma-separated)")
    new_authors = st.text_area("Authors (comma-separated)")
    new_alias = st.text_input("Alias")
    new_channel_browser_id = st.text_input("Channel Browser ID")
    if st.button("Add Channel"):
        new_channel_data = {
            "source_channel_id": new_channel_id,
            "specific_words": [word.strip() for word in new_specific_words.split(',') if word.strip()],
            "authors": [author.strip() for author in new_authors.split(',') if author.strip()],
            "alias": new_alias,
            "channel_browser_id": new_channel_browser_id
        }
        telegram_settings["channels"].append(new_channel_data)
        save_telegram_settings(telegram_settings)
        st.success(f"Channel '{new_channel_id}' added successfully.")

elif operation == "Edit Existing Channel":
    channel_ids = [channel["source_channel_id"] for channel in telegram_settings["channels"]]
    selected_channel_id = st.selectbox("Select a Channel", channel_ids)
    selected_channel = next(
        (channel for channel in telegram_settings["channels"] if channel["source_channel_id"] == selected_channel_id),
        None)

    if selected_channel:
        edited_specific_words = st.text_area("Edit Specific Words (comma-separated)",
                                             value=", ".join(selected_channel["specific_words"]))
        edited_authors = st.text_area("Edit Authors (comma-separated)", value=", ".join(selected_channel["authors"]))
        edited_alias = st.text_input("Edit Alias", value=selected_channel["alias"])
        edited_channel_browser_id = st.text_input("Edit Channel Browser ID",
                                                  value=selected_channel["channel_browser_id"])

        if st.button("Save Changes"):
            selected_channel["specific_words"] = [word.strip() for word in edited_specific_words.split(',') if
                                                  word.strip()]
            selected_channel["authors"] = [author.strip() for author in edited_authors.split(',') if author.strip()]
            selected_channel["alias"] = edited_alias
            selected_channel["channel_browser_id"] = edited_channel_browser_id
            save_telegram_settings(telegram_settings)
            st.success(f"Changes to channel '{selected_channel_id}' saved successfully.")

elif operation == "Delete Channel":
    channel_ids = [channel["source_channel_id"] for channel in telegram_settings["channels"]]
    selected_channel_id = st.selectbox("Select a Channel to Delete", channel_ids)
    if st.button("Delete Channel"):
        telegram_settings["channels"] = [channel for channel in telegram_settings["channels"] if
                                         channel["source_channel_id"] != selected_channel_id]
        save_telegram_settings(telegram_settings)
        st.success(f"Channel '{selected_channel_id}' deleted successfully.")

# Display current settings
st.subheader("Current Telegram Settings:")
st.json(telegram_settings)


# Function to convert settings to a downloadable file
def convert_to_downloadable_json(settings):
    return json.dumps(settings).encode('utf-8')


# Download current settings as JSON
st.download_button(
    label="Download Current Configuration",
    data=convert_to_downloadable_json(telegram_settings),
    file_name='telegram_settings.json',
    mime='application/json'
)

# Upload new JSON configuration
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
if uploaded_file is not None:
    uploaded_data = json.loads(uploaded_file.getvalue().decode("utf-8"))
    telegram_settings.update(uploaded_data)
    save_telegram_settings(telegram_settings)
    st.success("Settings updated with uploaded JSON configuration.")
