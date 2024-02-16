from langchain.prompts import PromptTemplate


prompt_template_seo ="""Optimize an article for SEO in HTML format, focusing on key enhancements. For the article "{original_article}", perform:
-Keyword Enhancement: Integrate high-traffic keywords, maintaining the article's essence.
-Content Structuring: Use H1 for the title, H2/H3 for subsections, organizing the content into clear, logical sections.
-Bullet Points: Format lists for readability.
-SEO Tags: Add title tags, meta descriptions, and image alt tags relevant to the content.
-Hyperlinks: Incorporate internal/external links to enhance authority and relevance.
-Readability: Enhance clarity and engagement, using concise language and engaging elements.
-HTML Output: Ensure the output is HTML-ready, structured for web publishing.

Aim: Streamline the SEO process, ensuring the final HTML article reflects the original's intent.
"""
prompt_seo=PromptTemplate(input_variables=["original_article"], template=prompt_template_seo)


prompt_template_img="""
Your task is meticulous integration of images into an HTML structure to achieve a harmonious blend between visual and textual content. The HTML article structure and list of images are provided below.

HTML Article Structure:"{html_article}"
List of Images:"{img_list}"

Integration Guidelines:
-Carefully review the article's content to identify optimal insertion points for each image, placing them beside relevant paragraphs where they naturally complement the text.
-Implement resizing of the image to fit with the content, and consider adding a border to enhance its appearance within the article.
-Use the <img> tag for embedding each image, meticulously defining src, alt (for accessibility and SEO), and any necessary style or class attributes to achieve the desired presentation and behavior.
-Ensure that the addition of images respects the article's structure, avoiding any disruption to the readability of the content.
-Final Output: The final HTML document should reflect a professional level of content integration, where images appear beside relevant paragraphs, thoughtfully placed and styled for optimal viewer engagement.

"""
prompt_image_gen=PromptTemplate(input_variables=["html_article", "img_list"], template=prompt_template_img)

