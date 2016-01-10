# -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 11:57:35 2015

@author: Ricky
"""
#import the two libraries we will be using in this script
import urllib2,re,sys,string

#make a new browser, this will download pages from the web for us. This is done by calling the 
#build_opener() method from the urllib2 library
browser=urllib2.build_opener()

#desguise the browser, so that websites think it is an actual browser running on a computer
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

filewrite1=open('Review.txt','w')
filewrite2=open('Ratings.txt','w')
filewrite3=open('Date.txt','w')

#number of pages you want to retrieve (remember: 10 freelancers per page)
pagesToGet=60

"""
Note: The range() function
    the range(a,b) function returns the list of numbers from a all the way to (but excluding) b. 
    For example, range (1,4) will return  [1, 2, 3]
"""

#for every number in the range from 1 to pageNum+1  
for page in range(1,pagesToGet+1):
    
    #print 'processing page :', page
    
    #make the full page url by appending the page num to the end of the standard prefix
    #we use the str() function because we cannot concatenate strings with numbers. We need
    #to convert the number to a string first.
    url='https://www.walmart.com/reviews/product/25059349?&page=' + str(page) + '&sort=helpful'

    try:
        #use the browser to get the url.
        response=browser.open(url)    
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR LINK:',url
        print error_type, 'Line:', error_info.tb_lineno
        continue
    
    #read the response in html format. This is essentially a long piece of text
    
    filewrite=open('Comment.txt','w') 
    myHTML1=response.read()
    filewrite.write(myHTML1)
    filewrite.close()
    filefinal=open('strip.txt','w')
    filew=open('Comment.txt','r')
    for line in filew:
        filestrip=line.strip()
        filefinal.write(filestrip)
    filew.close() 
    filefinal.close()
    fileread=open('strip.txt','r')
    
    
    review=re.finditer('<p class=js-customer-review-text data-max-height=110>(.*?)</p>',fileread)#get all the matches
    ratings=re.finditer('</i><span class=visuallyhidden>(.*?) ',fileread)
    date=re.finditer('<span class="customer-review-date hide-content-m">(.*?)<',fileread)
    
    for review_list in review:
        review_final=review_list.group(1) 
        review_final=string.replace(review_final, "&amp;","&")
        review_final=string.replace(review_final, '34;','"')
        review_final=string.replace(review_final, '&#39;',"'")
        review_final=string.replace(review_final, '&#"','"')
        #print review_final
        filewrite1.write(review_final + '\n')
    for ratings_list in ratings:
        ratings_final=ratings_list.group(1) 
        #print ratings_final
        filewrite2.write(ratings_final + '\n')
    for date_list in date:
        date_final=date_list.group(1) 
        #print date_final
        filewrite3.write(date_final + '\n')
#close the file. File that are opened must always be closed to make sure everything is actually written and finalized.
filewrite1.close()
filewrite2.close()
filewrite3.close()
count=3
filewrite4=open('Rating_final.txt','w')
fileread=tuple(open('Ratings.txt','r'))
while (count<= (len(fileread)-1)):
    #print count
    #print fileread[1379]
    filewrite4.write(fileread[count]) 
    count=count+1  
    if ((count%23)== 0):
        #print "in if"
        count=count+3     
filewrite4.close()

final_file=open('Wallmart_final.txt','w')
fileread1=tuple(open('Review.txt','r'))
fileread2=tuple(open('Rating_final.txt','r'))
fileread3=tuple(open('date.txt','r'))
for loop_count in range(0,(len(fileread1))):
    final_file.write('www.wallmart.com' + '\t' + fileread1[loop_count].strip() + '\t' + fileread2[loop_count].strip() + '\t' + fileread3[loop_count].strip() + '\n')
    
final_file.close()
#fileread4=tuple(open('Wallmart_final.txt','r'))
#print len(fileread4)
#print fileread4[0]
#print fileread4[1199]
