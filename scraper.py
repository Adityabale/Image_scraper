import os
import time
import requests
from selenium import webdriver
#https://www.geeksforgeeks.org/web-driver-methods-in-selenium-python/
#Selenium is a powerful tool for controlling web browsers through programs and performing browser automation.
#Selenium Webdriver is the parent of all methods and classes used in Selenium Python.
#Selenium’s Python Module is built to perform automated testing with Python

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #https://pythonbasics.org/selenium-scroll-down/
        #The selenium scroll down code calls the method execute_script() with the javascript to scroll to the end of the web page.
        #scroll down the complete body height or a specific height of the webpage.
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        #with inspect on browser check the css class of the images-(Q4LuWd in this case)
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:

            try:
                img.click()
                # try to click every thumbnail such that we can get the real image behind it
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            #once you click the image the css class will change
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
                    #it will append all the image urls in the empty set

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
                #once the count of all the image urls links in set = nmax links required then break

        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            with webdriver.Chrome() as wd:
                load_more_button=wd.find_elements_by_css_selector('.mye4qd')

            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_content = requests.get(url).content
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        #insert name for the downloaded images in sequence of counter.
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    #https: // www.geeksforgeeks.org / os - module - python - examples /
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
    #here we are trying to append search term with target path
    #eg\images\ferrari

    if not os.path.exists(target_folder):
        #it will check for the folder in current working directory.
        #print(os.getcwd()) will give current working directory
        #D:\Data Science\Ineuron\Main course\Python\Image scrapping project\ImageScrapper\ImageScrapper
        os.makedirs(target_folder)


    with webdriver.Chrome(executable_path=driver_path) as wd:
        #it will try to call 'D:\chromedriver.exe'
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=1)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


# How to execute this code
# Step 1 : pip install selenium. pillow, requests
# Step 2 : make sure you have chrome installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# Step 5 : put it inside the same folder of this code


DRIVER_PATH = r'D:\chromedriver.exe'
search_term = 'avatar 2'
# num of images you can pass it from here  by default it's 10 if you are not passing
#number_images = 50
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=50)