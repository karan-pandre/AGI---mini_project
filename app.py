# import streamlit as st  # for UI inter
# 
# 
# ce
# import google.generativeai as genai  # for blog generation
# from openai import OpenAI  # for DALL·E 3 image generation
# import os
# from apikey import google_gemini_api_key, openai_api_key  # import API keys

# # Configure the API keys
# genai.configure(api_key=google_gemini_api_key)

# # Create the model
# generation_config = {
#     "temperature": 1.9,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro-002",
#     generation_config=generation_config,
#     system_instruction="Generate a comprehensive, engaging blog post relevant to the given title.",
# )

# # Setting up Streamlit UI
# st.set_page_config(layout='wide')
# st.title('BlogCraft: Your AI Writing Companion')
# st.subheader("Now you can craft perfect blogs with the help of AI - Blogcraft is your new AI blog companion")

# # Sidebar for user input
# with st.sidebar:
#     st.title("Input Your Blog Details")
#     st.subheader("Enter Details of Blog You want to generate")
    
#     # Blog title
#     blog_title = st.text_input("Blog Title")
    
#     # Keywords input
#     keywords = st.text_area("Keywords (comma-separated)")
    
#     # Number of words
#     num_words = st.slider("Number of Words", min_value=250, max_value=1000, step=250)
    
#     # Submit button
#     submit_button = st.button("Generate Blog")

# if submit_button:
#     prompt = (
#         f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" "
#         f"and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. "
#         f"The blog should be approximately {num_words} words in length, suitable for an online audience."
#     )
    
#     # Generate blog content
#     response = model.generate_content([prompt])
    
#     st.title("YOUR BLOG POST:")
#     st.write(response.text)

#     Optional: Generate an image using OpenAI's DALL·E 3
#     client = OpenAI(api_key=openai_api_key)
#     image_response = client.images.generate(
#         model="dall-e-3",
#         prompt=f"Generate a blog post image on the title {blog_title}",
#         size="1024x1024",
#         n=1,
#     )
    
#     image_url = image_response.data[0].url
#     st.image(image_url, caption="Generated Image")

import streamlit as st  # For UI interface
import google.generativeai as genai  # For blog generation
from openai import OpenAI  # For DALL-E image generation
import os
from apikey import google_gemini_api_key, openai_api_key  # Your API keys

# Configure the APIs
genai.configure(api_key=google_gemini_api_key)
client = OpenAI(api_key=openai_api_key)

# Create the model
generation_config = {
    "temperature": 1.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Setting up the UI
st.set_page_config(layout='wide')
st.title('BlogCraft: Your AI Writing Companion')
st.subheader("Craft perfect blogs with the help of AI.")

# Sidebar for user input
with st.sidebar:
    st.title("Input Your Blog Details")
    st.subheader("Enter Details of Blog You want to generate")
    
    # Blog title
    blog_title = st.text_input("Blog Title")
    
    # Keywords input
    keywords = st.text_area("Keywords (comma-separated)")
    
    # Number of words
    num_words = st.slider("Number of Words", min_value=250, max_value=1000, step=250)
    
    # Number of images
    num_images = st.number_input("Number of Images", min_value=0, max_value=5, step=1)

# Submit button
submit_button = st.button("Generate Blog")

if submit_button:
    prompt_parts = [
        f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout."
    ]

    # Blog generation
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    prompt_parts[0]
                ],
            },
        ]
    )
    
    response = chat_session.send_message("INSERT_INPUT_HERE")  # Adjust as needed
    generated_blog = response.text if hasattr(response, 'text') else "No text generated."

    # Display the generated blog
    st.title("YOUR BLOG POST:")
    st.write(generated_blog)

    # Image generation
    if num_images > 0:
        try:
            # Generate an image based on the blog title
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=f"Generate a blog post image on the title {blog_title}",
                size="1024x1024",
                quality="standard",
                n=1,  # Request one image
            )
            image_url = image_response.data[0].url  # Get the first image URL
            st.image(image_url, caption="Generated Image")
        except Exception as e:
            st.error(f"Error generating image: {e}")
