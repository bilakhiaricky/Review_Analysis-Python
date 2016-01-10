
import re
import time,sys
from selenium import webdriver
import codecs
fw=codecs.open('bestbuy_finalreviews.txt','w', "utf-8")

#main url of the tv reviews from bestbuy
url='http://www.bestbuy.com/site/sharp-32-class-31-1-2-diag--led-1080p-hdtv-black/5420105.p?id=1219128175325&skuId=5420105'

#open the browser and visit the url
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)

#sleep for 2 seconds
time.sleep(2)

#find the 'Ratings and Reviews' button based on its css path
button=driver.find_element_by_css_selector('#ui-id-3')#ui-id-3
button.click() #click on the button
time.sleep(2) #sleep

print 'page 1 done'

page=2
while True:
    #get the css path of the 'next' button
    cssPath='#BVRRDisplayContentFooterID > div > span.BVRRPageLink.BVRRNextPage > a'
    
    try:
        button=driver.find_element_by_css_selector(cssPath)
    except:
        error_type, error_obj, error_info = sys.exc_info()
        print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', page
        print error_type, 'Line:', error_info.tb_lineno
        break

    #click the button to go the next page, then sleep    
    button.click()
    time.sleep(2)
   
    reviews=re.finditer('<div class="BVRRReviewTextContainer">((.|\s)*?)</div> </div>',driver.page_source)    
    dates=re.finditer('class="BVRRValue BVRRReviewDate">(.*?)<',driver.page_source)
    #averageRatings=re.finditer('aria-label="(.*?) out of 5 stars"(.*?)<',driver.page_source)   
    eachCustomerReview = re.finditer('<div id="BVRRDisplayContentID" class="BVRRDisplayContent">((.|\s)*)', driver.page_source) 
    ratings=re.finditer('<span property="v:value" class="BVRRNumber BVRRRatingNumber">(.*?)<',eachCustomerReview.next().group(0))
    
     #code to check if this is not the average rating of the page
    averageRatings=re.finditer('aria-label="(.*?) out of 5 stars"(.*?)<',driver.page_source)    
    for avrgRating in averageRatings:
        average=avrgRating.group(1)
        #print "averagerating=="+str(average)
      
    for review in reviews:
        
        actualReview = re.finditer('<span class="BVRRReviewText">(.*?)</span>',review.group(0))
        fw.write("www.bestbuy.com \t")
        for r in actualReview:
            review_final=r.group(1)
            fw.write(review_final)
        fw.write('\t')
        
        rating_final=ratings.next().group(1)
        fw.write(str(rating_final)+"\t")
        #print "rating_final=="+str(rating_final)
      
        date_final=dates.next().group(1)
        fw.write(str(date_final)+'\n')
        
        #fw.write("\n")
        
    print 'page',page,'done'
    page+=1
    
#write the results
fw.close()

