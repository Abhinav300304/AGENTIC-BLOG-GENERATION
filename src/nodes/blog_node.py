from src.states.blogstate import BlogState, Blog
from langchain_core.messages import HumanMessage

class BlogNode:
    """
    A class to represent the blog node with distinct methods for each path.
    """
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """Create a base title for the blog."""
        prompt = "Generate a creative and SEO-friendly blog title for the topic: {topic}."
        response = self.llm.invoke(prompt.format(topic=state['topic']))
        return {"blog": {"title": response.content, "content": ""}}

    def content_generation(self, state: BlogState):
        """Generate the main, unstructured content for the blog."""
        prompt = "You are an expert blog writer. Generate a detailed blog content with a breakdown for the topic: {topic}."
        response = self.llm.invoke(prompt.format(topic=state["topic"]))
        return {"blog": {"title": state['blog']['title'], "content": response.content}}

    def _structure_content(self, state: BlogState, language: str):
        """A helper function to structure content for a given language."""
        prompt = """
        You are an expert content writer and translator.
        Your task is to take the following blog content, translate it into {language},
        and then structure it into a complete blog format.

        You MUST structure your output into a JSON object with a 'main_title', an 'introduction',
        and a list of 'sections', where each section has its own 'title' and 'content'.

        ORIGINAL CONTENT:
        Title: {blog_title}
        Content: {blog_content}
        """
        messages = [
            HumanMessage(
                content=prompt.format(
                    language=language,
                    blog_title=state["blog"]["title"],
                    blog_content=state["blog"]["content"]
                )
            )
        ]
        structured_blog = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": structured_blog.model_dump()}

    def english_structuring(self, state: BlogState):
        """Node to structure the content in English."""
        print("Executing English structuring node.")
        return self._structure_content(state, "English")

    def german_translation(self, state: BlogState):
        """Node to translate and structure the content in German."""
        print("Executing German translation node.")
        return self._structure_content(state, "German")

    def route(self, state: BlogState):
        """This node simply passes the state to the conditional router."""
        return state

    def route_decision(self, state: BlogState):
        """Determines the next step based on the selected language."""
        if state.get("current_language", "").lower() == "german":
            return "german"
        return "english"
# from src.states.blogstate import BlogState, Blog # Import the corrected Blog model
# from langchain_core.messages import HumanMessage

# class BlogNode:
#     """
#     A class to represent the blog node.
#     """
#     def __init__(self, llm):
#         self.llm = llm

#     def title_creation(self, state: BlogState):
#         """
#         Create the title for the blog. This will be used as a base for the main title.
#         """
#         if "topic" in state and state['topic']:
#             prompt = """You are an expert blog content writer. Use Markdown formatting.
#                     Generate a blog title for the {topic}. This title should be creative and SEO friendly."""
#             system_message = prompt.format(topic=state['topic'])
#             response = self.llm.invoke(system_message)
#             # We'll store this temporarily and let the structuring node create the final main_title
#             return {"blog": {'title': response.content}}

#     def content_generation(self, state: BlogState):
#         """
#         Generate the main, unstructured content for the blog.
#         """
#         if "topic" in state and state["topic"]:
#             system_prompt = """You are an expert blog writer. Use Markdown formatting.
#             Generate a detailed blog content with a detailed breakdown for the {topic}.
#             The content should be comprehensive and well-structured."""
#             system_message = system_prompt.format(topic=state["topic"])
#             response = self.llm.invoke(system_message)
#             # Store the generated content in the state
#             return {"blog": {"title": state['blog']['title'], "content": response.content}}

#     def translation_and_structuring(self, state: BlogState):
#         """
#         Translate the content to the specified language AND structure it
#         according to the Pydantic model.
#         """
#         translation_prompt = """
#         You are an expert content writer and translator.
#         Your task is to take the following blog content, translate it into {current_language},
#         and then structure it into a complete blog format.

#         You MUST structure your output into a JSON object that conforms to the following schema:
#         - A 'main_title' for the entire blog.
#         - An 'introduction' paragraph.
#         - A list of 'sections', where each section has its own 'title' and 'content'.

#         ORIGINAL CONTENT TO TRANSLATE AND RESTRUCTURE:
#         ---
#         Title: {blog_title}
#         Content: {blog_content}
#         ---
#         """
#         print(f"Translating and structuring content for: {state['current_language']}")
        
#         # We now have a simple title and a block of content to work with
#         blog_title = state["blog"]["title"]
#         blog_content = state["blog"]["content"]

#         messages = [
#             HumanMessage(
#                 content=translation_prompt.format(
#                     current_language=state["current_language"],
#                     blog_title=blog_title,
#                     blog_content=blog_content
#                 )
#             )
#         ]

#         # This call asks the LLM to format its response according to the Blog Pydantic model
#         structured_blog = self.llm.with_structured_output(Blog).invoke(messages)

#         # Replace the old blog structure with the new, structured, translated blog.
#         # .model_dump() converts the Pydantic model to a dictionary for state compatibility.
#         return {"blog": structured_blog.model_dump()}

#     def no_translation_structuring(self, state: BlogState):
#         """
#         This node handles the case where no translation is needed (i.e., English).
#         It still structures the content according to the Pydantic model.
#         """
#         return self.translation_and_structuring({**state, 'current_language': 'English'})

#     def route_decision(self, state: BlogState):
#         """
#         Route the content to the respective translation/structuring function.
#         """
#         print(f"Routing based on language: {state.get('current_language')}")
#         if state.get("current_language") and state["current_language"].lower() == "german":
#             return "german"
#         else:
#             # Default to English structuring if language is 'english' or not provided
#             return "english"

# from src.states.blogstate import BlogState
# from langchain_core.messages import HumanMessage,SystemMessage
# from src.states.blogstate import Blog
# class BlogNode:
#     """
#     A class to represent the blog node
#     """

#     def __init__(self,llm):
#         self.llm=llm

#     def title_creation(self,state:BlogState):
#         """"
#         Create the title for the blog
#         """

#         if "topic" in state and state['topic']:
#             prompt="""
#                     You are an expert blog content writer.Use Markdown formatting.Generate 
#                     a blog title for the {topic}.This title should be creative and SEO friendly
#                 """
#             system_message=prompt.format(topic=state['topic'])
#             response=self.llm.invoke(system_message)
#             return {"blog":{'title':response.content}}
        

#     def content_generation(self,state:BlogState):
#         if "topic" in state and state["topic"]:
#             system_prompt = """You are expert blog writer. Use Markdown formatting.
#             Generate a detailed blog content with detailed breakdown for the {topic}"""
#             system_message = system_prompt.format(topic=state["topic"])
#             response = self.llm.invoke(system_message)
#             return {"blog": {"title": state['blog']['title'], "content": response.content}}    


#     def translation(self,state:BlogState):
#         """
#         Translate the content to the specified language.
#         """
#         translation_prompt="""
#         Translate the following content into {current_language}.
#         - Maintain the original tone, style, and formatting.
#         - Adapt cultural references and idioms to be appropriate for {current_language}.

#         ORIGINAL CONTENT:
#         {blog_content}

#         """
#         print(state["current_language"])
#         blog_content=state["blog"]["content"]
#         messages=[
#             HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_content=blog_content))

#         ]
#         transaltion_content = self.llm.with_structured_output(Blog).invoke(messages)
#         return {"blog": {"content": transaltion_content}}

#     def route(self, state: BlogState):
#         return {"current_language": state['current_language'] }
    

        

#     def route_decision(self, state: BlogState):
#         """
#         Route the content to the respective translation function.
#         """
        
#         if state["current_language"] == "english":
#             return "english"
#         elif state["current_language"] == "german": 
#             return "german"
#         else:
#             return state['current_language']