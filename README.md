# Simple Static Blog Generator  

This is a simple python script that generates a static blog.  
The motivation is that I wanted something to allow me to quickly make blogposts
without involving any other frameworks. 

## Using this Generator

You must have BlogTemplates folder that contains the HTML template for your 
BlogList page and your PostPage.    
BlogList: The page that lists (in reverse chronological order) all of your posts.  
PostPage: The pages that contain individual blog posts.  


Your posts should be written in a folder named blogposts.

## Writing a blog post

Blog posts should be written in the following format:

```html
<h1 class="title"><a id="blogs/%desired-filename%">%Desired Title%</a></h1>
<p class="date">%m/%d/%Y</p>
<p class="blogtext">%Desired blog content%</p>
```

where areas marked with a "%" are filled according to your preference.
Notably, the text of the blog can contain arbitrary HTML. I would suggest
building your blog and thoroughly checking that no arbitrary HTML has affected
the page layout.

### License
This project is covered under GNU GPLv3

### TODO
Make the bloglist multiple pages, if they are more than n posts. 
