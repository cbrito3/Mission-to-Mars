# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


#We'll want to assign the title and summary text to variables we'll reference later. In the next empty cell, let's begin our scraping. Type the following:

slide_elem.find('div', class_='content_title')


# In[6]:


#The title is in that mix of HTML in our output—that's awesome! But we need to get just the text, and the extra HTML stuff isn't necessary. In the next cell, type the following:

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#What will we need to change in the following line of code to scrape the article summary instead of the title: 

#slide_elem.find(“div”, class_=‘content_title’).get_text()
    #We’ll need to change the class to “article_teaser_body.”


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


#Since there are only three buttons, and we want to click the full-size image button, we can go ahead and use the HTML tag in our code.
#In the next cell, let's type the following:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


#We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image. Let's go back to Jupyter Notebook to do that.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#We've done a lot with that single line. Let's break it down:
#An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
#What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#Now let's break it down:
#df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
#df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
#df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.


# In[15]:


#This is exactly what Robin is looking to add to her web application. How do we add the DataFrame to a web application? 
#Robin's web app is going to be an actual webpage. Our data is live—if the table is updated, then we want that change to appear in Robin's app also.
#Thankfully, Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
#Add this line to the next cell in your notebook and then run the code.


# In[16]:


df.to_html()


# In[17]:


#The result is a slightly confusing-looking set of HTML code—it's a <table /> element with a lot of nested elements. This means success. 
#After adding this exact block of code to Robin's web app, the data it's storing will be presented in an easy-to-read tabular format.
#Now that we've gathered everything on Robin's list, we can end the automated browsing session. This is an important line to add to our 
#web app also. Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on). We really only want the automated browser to remain active while we're scraping data. It's like turning off a light switch when you're ready to leave the room or home.
#In the last empty cell of Jupyter Notebook, add browser.quit() and execute that cell to end the session.

browser.quit()


# In[ ]:




