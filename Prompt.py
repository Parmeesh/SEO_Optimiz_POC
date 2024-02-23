from langchain.prompts import PromptTemplate


prompt_temp_gemini_seo ="""
Given the input article tagged as {original_article}, along with a list of important keywords provided in {keyword_list} extracted from another article with the same title, your task is to enhance and prepare it for SEO-optimized web publishing in HTML format. Follow these steps meticulously to ensure the article is both enriched for search engines and reader-friendly:

    Keyword Optimization:
        Analyze the {original_article} to identify its core themes and subjects.
        Review the {keyword_list} containing extracted keywords. Integrate those keywords that are relevant to the context of {original_article}. This integration should enhance the SEO potential without compromising the article’s original intent.

    Content Structuring:
        Organize the article using HTML tags, starting with an <h1> tag for the main title. Utilize <h2> and <h3> tags for subsections to structure the content logically.
        Break down the text into concise paragraphs and bulleted lists (<ul> or <ol> with <li> items) for improved readability and engagement.

    SEO Enhancements:
        Add essential SEO HTML tags including a concise <title> tag, a compelling <meta name="description"> tag that summarizes the article, and <meta name="keywords"> tag filled with the optimized keywords, including those selected from the {keyword_list}.

    Hyperlink Integration:
        Incorporate internal links to relevant pages within your website and external links to authoritative sources, using the <a href="URL">anchor text</a> format. This step enhances the article's credibility and SEO performance.

    Readability and Engagement:
        Revise the article to ensure language is clear, concise, and engaging. Aim for a balance between professionalism and accessibility to maintain the reader's interest.
        Include engaging elements such as questions, anecdotes, or quotes where appropriate, formatting them to stand out.

    HTML Output Preparation:
        Convert the optimized and structured content into clean HTML code. Ensure all HTML elements are correctly used and closed, and the code is formatted for easy reading and editing.
        Validate the HTML to check for any errors or warnings that need to be addressed before publishing.

    SEO Optimization Check:
       	Run a final SEO check on the HTML content, ensuring all optimizations align with current best practices and the article is primed for high search engine visibility.

Objective:
Your goal is to transform the {original_article} into an SEO-optimized, reader-friendly HTML document ready for web publishing. This process involves not just technical SEO enhancements but also improving the article's readability and engagement to meet both search engine and reader expectations. By integrating relevant keywords from the {keyword_list}, you aim to further enhance the article's visibility and relevance.

Ensure the final HTML output is clean, well-structured, and fully optimized, ready to make a significant impact online.
"""

prompt_gemini_seo=PromptTemplate(input_variables=["original_article", "keyword_list"], template=prompt_temp_gemini_seo)




prompt_temp_openai_seo ="""
Task: Take the content from '{original_article}' and transform it into an article that is not only optimized for search engines but also formatted in HTML, ready for web publishing. Your task involves several key steps, each crucial for enhancing the article's SEO and user readability while maintaining its original intent and structure.

1. **Keyword Integration**
   - Integrate the provided keywords into the article's text. Ensure these keywords are woven seamlessly into the content, enhancing SEO without compromising the narrative's flow or readability.

2. **HTML Structuring**
   - Apply HTML tags to organize the article properly.
     - Use `<h2>` tags for main headings and `<h3>` tags for subheadings.
     - Emphasize important terms with `<strong>` tags.
     - Keep the original paragraph structure, using headings to logically divide sections.

3. **SEO Enhancements**
   - Craft an engaging `<title>` tag and a descriptive `<meta name="description">` tag, including primary keywords to boost the article's search relevance.

4. **Link Strategy**
   - Incorporate internal and external links strategically.
     - For internal links, use descriptive anchor text pointing to relevant content within your site.
     - Choose reputable sources for external links, ensuring the anchor text supports the article's context and adds value.

5. **Readability and Engagement**
   - Enhance the article's readability with clear, accessible language.
   - Use bullet points or numbered lists to present information concisely and engagingly.

6. **Final HTML Output**
   - Produce a complete HTML document ready for publishing, including `<html>`, `<head>`, and `<body>` tags, integrating all SEO enhancements.

**Objective**: Your goal is to refine the article for optimal search engine visibility and user engagement, preserving the original content's essence and format, and making it ready for online publication.

"""
prompt_openai_seo=PromptTemplate(input_variables=["original_article"], template=prompt_temp_openai_seo)




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


prompt_temp_keyword='''
Analyze the following text and identify the top 10 most important keywords and phrases. These should be the key terms that are crucial for understanding the main topics and concepts of the text. The objective is to extract these keywords to use them for creating an SEO-optimized article related to the same subject. Focus on relevance and searchability, ensuring that the selected keywords will help in improving the article's visibility on search engines.

---

Article_text:"{article_text}"

---

Please provide a list of the top 10 keywords and phrases extracted from the text, prioritizing those with the highest relevance and potential impact on SEO.
'''
prompt_for_keywords = PromptTemplate(input_variables=["article_text"], template=prompt_temp_keyword)