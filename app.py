from LlamaIndexWrapper import  LlamaIndexWrapper
import streamlit as st

wrapper = LlamaIndexWrapper()

if "query_engine" not in st.session_state.keys():
    wrapper.main()
    query_engine = wrapper.create_query_engine()
    st.session_state.query_engine = query_engine

from PIL import Image
import streamlit as st

im = Image.open("Fashion Search AI Assistant.png")
st.logo(im, size="large")

st.title("Fashion Search Engine")

search_text = st.text_input("Search for products brands etc.")

if search_text:
    with st.spinner(f"Searching for {search_text}..."):
        response = st.session_state.query_engine.query(search_text)
        if response.source_nodes:
            st.write(f"Found {len(response.source_nodes)} results for {search_text}")
            for node in response.source_nodes:
                st.write(node.text)
                st.image(image=node.metadata['img'], width=200)
        else:
            st.write("No relevant products found with specified search teams.")