from typing import TypedDict, List
from pydantic import BaseModel, Field

# NEW: A model to represent a single section of the blog.
class BlogSection(BaseModel):
    """Represents a single section of a blog post."""
    title: str = Field(description="The title of this specific blog section.")
    content: str = Field(description="The full content of this section, formatted in Markdown.")

# UPDATED: The main Blog model, now composed of multiple sections.
class Blog(BaseModel):
    """Represents a complete, well-structured blog post."""
    main_title: str = Field(description="The overarching title of the entire blog post.")
    introduction: str = Field(description="An introductory summary of the blog post.")
    sections: List[BlogSection] = Field(description="A list of the individual sections that make up the blog.")

# The main state remains the same, but it will now hold our new Blog structure.
class BlogState(TypedDict):
    topic: str
    blog: Blog
    current_language: str

# from typing import TypedDict
# from pydantic import BaseModel,Field

# class Blog(BaseModel):
#     title:str=Field(description="Title of the blog post")
#     content:str=Field(description="The main content of the blog post")

# class BlogState(TypedDict):
#     topic:str
#     blog:Blog
#     current_language:str
