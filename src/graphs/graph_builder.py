from langgraph.graph import StateGraph, START, END
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode
from dotenv import load_dotenv
from src.llms.groqllm import GroqLLM

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)

    def build_graph(self):
        """
        Builds a graph with conditional routing for different languages,
        matching the desired structure.
        """
        # Define the nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_node("route", self.blog_node_obj.route) # The routing node
        self.graph.add_node("english_node", self.blog_node_obj.english_structuring)
        self.graph.add_node("german_node", self.blog_node_obj.german_translation)

        # Define the edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        # Add the conditional branching
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "english": "english_node",
                "german": "german_node"
            }
        )

        # Connect the final nodes to the end
        self.graph.add_edge("english_node", END)
        self.graph.add_edge("german_node", END)
        
        return self.graph

    def setup_graph(self, usecase=None):
        """Sets up and compiles the graph."""
        return self.build_graph().compile()

# --- Section for langgraph dev ---
load_dotenv()
llm = GroqLLM().get_llm()
builder = GraphBuilder(llm)
# This is the variable that `langgraph dev` will look for.
graph = builder.build_graph().compile()









# from src.llms.groqllm import GroqLLM
# from langgraph.graph import StateGraph, START, END
# from src.states.blogstate import BlogState
# from src.nodes.blog_node import BlogNode

# class GraphBuilder:
#     def __init__(self, llm):
#         self.llm = llm
#         self.graph = StateGraph(BlogState)
#         self.blog_node_obj = BlogNode(self.llm)

#     def build_graph(self):
#         """
#         Builds the graph for generating and structuring blog posts.
#         """
#         self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
#         self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        
#         # A single node for German translation and structuring
#         self.graph.add_node("german_translation_and_structuring", self.blog_node_obj.translation_and_structuring)
        
#         # A node for the default case (English) which just structures the content
#         self.graph.add_node("english_structuring", self.blog_node_obj.no_translation_structuring)

#         self.graph.add_edge(START, "title_creation")
#         self.graph.add_edge("title_creation", "content_generation")
        
#         # After content is generated, decide where to go based on language
#         self.graph.add_conditional_edges(
#             "content_generation",
#             self.blog_node_obj.route_decision,
#             {
#                 "english": "english_structuring",
#                 "german": "german_translation_and_structuring"
#             }
#         )

#         self.graph.add_edge("english_structuring", END)
#         self.graph.add_edge("german_translation_and_structuring", END)
        
#         return self.graph.compile()

#     def setup_graph(self, usecase=None): # Usecase is no longer strictly needed but kept for compatibility
#         """
#         Sets up and compiles the graph.
#         """
#         return self.build_graph()




# from langgraph.graph import StateGraph,START,END
# from src.llms.groqllm import GroqLLM
# from src.states.blogstate import BlogState
# from src.nodes.blog_node import BlogNode

# class GraphBuilder:
#     def __init__(self,llm):
#         self.llm=llm
#         self.graph=StateGraph(BlogState)
    
#     def build_topic_graph(self):
#         """
#         Build a graph to generate blogs based on topic
#         """
#         self.blog_node_obj=BlogNode(self.llm)
#         self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
#         self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

#         self.graph.add_edge(START,"title_creation")
#         self.graph.add_edge('title_creation',"content_generation")
#         self.graph.add_edge('content_generation',END)

#         return self.graph
    
#     def build_language_graph(self):
#         """
#         Build a graph for blog generation with inputs topic and language
#         """

#         self.blog_node_obj=BlogNode(self.llm)
#         self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
#         self.graph.add_node("content_generation",self.blog_node_obj.content_generation)
#         self.graph.add_node("english_translation",lambda state: self.blog_node_obj.translation({**state,'current_language':'english'}))
#         self.graph.add_node("german_translation",lambda state: self.blog_node_obj.translation({**state,'current_language':'german'}))
#         self.graph.add_node("route",self.blog_node_obj.route)

#         self.graph.add_edge(START,"title_creation")
#         self.graph.add_edge('title_creation',"content_generation")
#         self.graph.add_edge("content_generation","route")
#         self.graph.add_conditional_edges(
#             "route",
#             self.blog_node_obj.route_decision,
#             {
#                 'english':"english_translation",
#                 'german':"german_translation"
#             }
#         )

#         self.graph.add_edge("english_translation",END)
#         self.graph.add_edge("german_translation",END)
#         return self.graph
       
    
#     def setup_graph(self,usecase):
#         if usecase=="topic":
#             self.build_topic_graph()

#         if usecase=="language":
#             self.build_language_graph()

#         return self.graph.compile()
    

# ## This is for the langsmith Langgraph studio for debugging

# llm=GroqLLM().get_llm()

# graph_builder=GraphBuilder(llm)
# graph=graph_builder.build_language_graph().compile()
    
