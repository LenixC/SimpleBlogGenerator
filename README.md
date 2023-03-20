# Simple Static Blog Generator  

This is a simple python script that generates a static blog.  
The motivation is that I wanted something to allow me to quickly make blogposts
without involving any other frameworks, and I wanted it to contain
as simple as instructions as possible. 

## Using this Generator

In your website directory you must have BlogTemplates folder that contains the HTML template for your 
BlogList page and your PostPage.    
BlogList: The page that lists (in reverse chronological order) all of your posts.  
PostPage: The pages that contain individual blog posts.  

To run, simply run `python3 build_blog.py -c "location"`

Your posts should be written in a folder named blogposts.

## Writing a blog post

Blog posts should be written in the following format:

```html
<h1 class="title"><a id="blog-location" href="blogs/%desired-filename%">%Desired Title%</a></h1>
<p class="date">%m/%d/%Y</p>
<p class="blogtext">%Desired blog content%</p>
```

where areas marked with a "%" are filled according to your preference.
The tags themselves aren't important, only the classes and id are checked.
Notably, the text of the blog can contain arbitrary HTML. I would suggest
building your blog and thoroughly checking that no arbitrary HTML has affected
the page layout.

Your BlogList.html file must contain a div with id="bloglist" and your
PostPage.html must contain a div with id="blogpost". These are where 
generated content are placed. 

Currently, the blog outputs the title to an h2, the date to a p, and the
blogtext to a p, each with class="text". 

### License
This project is covered under GNU GPLv3

### TODO
Make the bloglist multiple pages, if they are more than n posts. 
