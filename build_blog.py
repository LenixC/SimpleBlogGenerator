import os
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from functools import total_ordering
from html import unescape


@total_ordering
class ArticleSummary:
    """
    Represents the article slug to appear on the blog list page.
    ...
    Attributes
    ----------
    title : str
        the title of the article
    date : datetime.datetime
        the date the object was posted
    lede : str
        the shortened content of the article
    Methods
    -------
    ordering methods
        this class contains ordering methods allowing them to be organized by date
    """
    def __init__(self, title: str, date: str, lede: str):
        """
        Parameters
        ----------
        title : str
            the title of the article
        date : str
            the date the object was posted
        lede : str
            the full content of the article (trims to 256 chars and adds ...)
        """
        self.title = title
        self.date = datetime.strptime(date, "%m/%d/%Y")
        self.lede = lede
        if len(self.lede) > 256:
            self.lede = self.lede[:256] + "..."

    def __lt__(self, obj):
        return ((self.date) < (obj.date))

    def __gt__(self, obj):
        return ((self.date) > (obj.date))

    def __le__(self, obj):
        return ((self.date) <= (obj.date))
    
    def __ge__(self, obj):
        return ((self.date) >= (obj.date))

    def __eq__(self, obj):
        return ((self.date) == (obj.date))

    def __repr__(self):
        return self.title + ": " + str(self.date) + "\n" + self.lede + "\n"


class BlogBuilder:
    """
    A class that contains properties and functions for generating a static blog
    ...
    Attributes
    ----------
    postlistpage : bs4.BeautifulSoup
        the page to be modified for cloning a template and filling with a postlist
    blog_posts_location : str
        the location of the blog posts to populate the bloglist and the blog pages
    blog_page_location : str
        the location of the template for a post page

    Methods
    -------
    build_postlist()
        generates static postlist page and creates pages linked therein
    insert_post(post, header)
        helper function for build_postlist, inserts article summaries 
        into postlistpage
    """
    def __init__(self, bloglist_location, page_post_location, blog_posts_location):
        """
        Parmeters
        ---------
        bloglist_location : str
            the location of the bloglist template page
        blog_page_location : str
            the location of the template for a post page
        blog_posts_location : str
            the location of blog posts to populate blog
        """
        self.postlistpage = None;
        self.page_post_location = page_post_location
        self.blog_posts_location = blog_posts_location
        with open(bloglist_location) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            self.postlistpage = soup


    def build_postlist(self):
        """
        Reads from HTML templates that contain blogpost title, date, and content
        and generates the bloglistpage and creates blog post pages. Posts are
        sorted from most recent to least on the bloglistpage.
        """
        post_list = []
        for filename in os.listdir(self.blog_posts_location):
            with open(self.blog_posts_location + "/" + filename) as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                title = soup.select_one('.title').decode_contents(formatter=None)
                date = soup.select_one('.date').text
                cleaned_content = soup.select_one('.blogtext').text
                article_summary = ArticleSummary(title, date, cleaned_content)
                post_list.append(article_summary)

                cleaned_title = soup.select_one('.title').text
                url = soup.select_one('#blog-location')['href']
                raw_content = soup.select_one('.blogtext').decode_contents(formatter=None)
                page = {'title': cleaned_title,
                        'date': date,
                        'raw_content': raw_content,
                        'url': url,
                        }
                self.build_page(page)
                
        if len(post_list) > 0:
            post_list = sorted(post_list)
            for post in reversed(post_list): # posts should be added newest to oldest
                self.insert_post(post)
        elif len(post_list) == 0:
            empty_list_message = self.postlistpage.new_tag('h3')
            empty_list_message['class'] = "centering text"
            empty_list_message.string = "There's nothing here yet."
            self.postlistpage.html.body.div.append(empty_list_message)


    def insert_post(self, post: ArticleSummary):
        """
        Inserts blog post title, date, and lede into the template page.

        Parameters
        ----------
        post : ArticleSummary
            the post to be added to the page
        """
        content_div = self.postlistpage.select_one("#bloglist")
        
        post_title = self.postlistpage.new_tag('h2')
        post_title['class'] = "title text"
        post_title.string = post.title
        content_div.append(post_title)

        post_date = self.postlistpage.new_tag('p')
        post_date['class'] = "date text"
        post_date.string = post.date.strftime('%m/%d/%Y')
        content_div.append(post_date)

        post_body = self.postlistpage.new_tag('p')
        post_body['class'] = "blogtext text"
        post_body.string = post.lede
        content_div.append(post_body)


    def build_page(self, page: dict):
        """
        Writes content from page to a template file and saves the file in
        the appropriate location

        Parameters
        ----------
        page: dict
            a page contains the title, date, content, and url to output to
        """
        soup = None
        with open(self.page_post_location) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        content_div = soup.select_one("#blogpost")

        page_title = soup.new_tag('h2')
        page_title['class'] = "title text"
        page_title.string = page["title"]
        content_div.append(page_title)

        page_date = soup.new_tag('p')
        page_date['class'] = "date text"
        page_date.string = page["date"]
        content_div.append(page_date)

        page_body = soup.new_tag('p')
        page_body['class'] = "blogtext text"
        page_body.string = page["raw_content"]
        content_div.append(page_body)

        with open(page["url"], "w", encoding='utf-8') as fp:
            fp.write(soup.prettify(formatter=None))

    
    def write_postlist(self):
        """
        Writes modified postlistpage to memory in the home directory.
        """
        with open("blog.html", "w", encoding='utf-8') as fp:
            fp.write(self.postlistpage.prettify(formatter=None))


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-c", "--cwd", 
                           help="The working directory for your blog.")

    args = argParser.parse_args()
    os.chdir(args.cwd)

    blog = BlogBuilder('BlogTemplates/BlogList.html', 
                       'BlogTemplates/PostPage.html', 
                       'blogposts')
    blog.build_postlist()
    blog.write_postlist()

