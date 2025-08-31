import streamlit as st
import requests
import base64
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Agentic Blog Generator",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ Agentic Blog Generator")
st.markdown("This interface uses an agentic backend to generate high-quality blog posts. Below is the visual representation of the agent's workflow.")

# --- Display Graph Image ---
try:
    # Instantiate the necessary components to build the graph for visualization
    llm = GroqLLM().get_llm()
    graph_builder = GraphBuilder(llm)
    
    # 1. Build the graph definition
    uncompiled_graph = graph_builder.build_graph()
    
    # 2. Compile the graph to get a runnable and drawable instance
    compiled_graph = uncompiled_graph.compile()
    
    # 3. Get the underlying graph structure and draw it as a PNG
    image_bytes = compiled_graph.get_graph().draw_mermaid_png()
    
    # 4. Encode the image bytes to base64 to display in Streamlit
    b64_image = base64.b64encode(image_bytes).decode()
    
    st.image(f"data:image/png;base64,{b64_image}", caption="Agent Workflow Graph")

except Exception as e:
    st.error(f"Could not generate graph visualization. Error: {e}")


st.markdown("---")

# --- Input Form ---
with st.form("blog_form"):
    topic = st.text_input(
        "**Enter a Blog Topic**",
        placeholder="e.g., The Future of Machine Learning"
    )
    language = st.selectbox(
        "**Select a Language**",
        ("english", "german")
    )
    submitted = st.form_submit_button("Generate Blog", type="primary")

# --- Backend Communication and Rendering ---
if submitted:
    if not topic:
        st.error("Please enter a topic to generate the blog.")
    else:
        api_url = os.getenv("API_URL", "http://127.0.0.1:8000/blogs")
        payload = {"topic": topic, "language": language}

        try:
            with st.spinner("Generating your blog... This may take a moment."):
                response = requests.post(api_url, json=payload)

                if response.status_code == 200:
                    st.success("Blog generated successfully!")
                    result = response.json()
                    blog_data = result.get("data", {}).get("blog", {})

                    if blog_data:
                        st.header(blog_data.get("main_title", "Blog Title"))
                        st.markdown(f"*{blog_data.get('introduction', '')}*")
                        
                        for section in blog_data.get("sections", []):
                            st.subheader(section.get("title", "Section"))
                            st.markdown(section.get("content", ""))
                    else:
                        st.error("Received an empty response from the backend.")
                else:
                    st.error(f"Failed to generate blog. Status code: {response.status_code}")
                    st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend at {api_url}. Please ensure your FastAPI server is running.")


