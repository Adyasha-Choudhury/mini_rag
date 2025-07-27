import streamlit as st
import logic
import json
st.title("Document Processing")
st.write("This application processes documents to extract and analyze text.")
query = st.text_input("Enter your query:") # You can customize the label
if not query:
    st.warning("Please enter a query to proceed.")
st.subheader("For now, using local files...")
b2 = st.button("Run query")

if b2 and query and ("collection_name" not in st.session_state.keys()):
    st.write("Processing local files...")
    response = logic.pipeline(query)
    st.session_state["collection_name"] = response[0].name
    st.session_state["query"] = response[1]
    st.session_state["model1"] = response[2]

if b2 and query and ("collection_name" in st.session_state.keys()):
    # Reload the collection from disk
    chroma_client = logic.Client(logic.Settings(persist_directory="./chroma_db"))
    collection = chroma_client.get_collection(st.session_state["collection_name"])
    response_json = logic.askbot(collection, query, st.session_state["model1"])

    # Parse the JSON string into a Python dictionary
    try:
        data = json.loads(response_json)

        for key, value in data.items():
            st.subheader(key)
            st.write(value)

        st.write("Query processed successfully.")
    except :
        st.write("Error decoding JSON response, printing as it is:")
        st.write(response_json)


#b1 = st.button("run new query on same files")
#if b1 :
#    query1  = st.text_input("Enter your query:")
#      st.write("Processing new query on the same files...")
    # Reload the collection from disk
#        chroma_client = logic.Client(logic.Settings(persist_directory="./chroma_db"))
#        collection = chroma_client.get_collection(st.session_state["collection_name"])
#        response_json = logic.askbot(collection, query1, st.session_state["model1"])

        # Parse the JSON string into a Python dictionary
#        try:
#            data = json.loads(response_json)

#            for key, value in data.items():
#                st.subheader(key)
#                st.write(value)

#            st.write("Query processed successfully.")
#        except :
#            st.write("Error decoding JSON response, printing as it is:")
#            st.write(response_json)
#    else:
#        st.warning("Please run the first time.")