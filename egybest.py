from selenium import webdriver
from time import sleep
import time
#قائمة روابط كل مواسم
list_all_season=[]
#قائمة روابط كل حلقات
list_all_eps=[]
#قاءمة روابط تحميل كل حلقات
list_all_link_download_eps=[]
def go_url(url):
    #دالة لفتح الموقع في متصفح
    start = time.time()
    global driver
    global wait
    #فتح  المتصفح
    #استعملت متصفح فيرفوكس
    #بامكانك فتح متصفخ اخر مثل كروم
    driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe')
    driver.implicitly_wait(10) # seconds
    print('get url\n')
    #فتح الموقع الخاص بمسلسل
    driver.get(url)
    print('get url...done\n')
    done = time.time()
    elapsed = done - start
    print('time get url is: '+time.strftime('%H:%M:%S', time.gmtime(elapsed))+'\n')

def egybest_getseason():
    #دالة تأتي برواوبط كل مواسم المسلسل
    #ووضعها في قائمة
    start = time.time()
    sleep(2)
    print('get season\n')
    #بحث عن تاغ a في html الصفحة ثم وضعه في متغير links
    links=driver.find_elements_by_tag_name('a')
    for link in links:
        #ايجاد تاغ a المنشود الذي تحتوي خصائص التالية
        if isinstance(link.get_attribute('class'), str) and link.get_attribute('class')=="movie":
            if 'www.egy.best/season' in link.get_attribute('href'):
                #عند ايجاد تاغ a المنشود ناتي برابط الموجد داخله ثم اضافته الى قائمة
                list_all_season.append(link.get_attribute('href'))
    #ترتيب القائمة
    list_all_season.reverse()
    print('get season...done\n')
    done = time.time()
    elapsed = done - start
    print('time get season is: '+time.strftime('%H:%M:%S', time.gmtime(elapsed))+'\n')
def egybest_geteps1():
    #دالة لايجاد حلقات المسلسل وملا القائمة بروايط الحلقات
    start = time.time()
    sleep(2)
    print('get get eps 1\n')
    #بحث عن حلقات في كل موسم
    for l in list_all_season:
        #قائمة روابط حلقات موسم واحد فقط
        list_eps_one_season=[]
        driver.get(l)
        links=driver.find_elements_by_tag_name('a')    
        for link in links:
            if isinstance(link.get_attribute('class'), str) and link.get_attribute('class')=="movie":
                if 'episode' in link.get_attribute('href'):
                    #بحث عن روابط حلقات في egybest
                    list_eps_one_season.append(link.get_attribute('href'))
        list_eps_one_season.reverse()
        #وضع كل روابط في قائمة
        list_all_eps.append(list_eps_one_season)
        
    print('get get eps 1...done\n')
    done = time.time()
    elapsed = done - start
    print('timeget eps 1 is: '+time.strftime('%H:%M:%S', time.gmtime(elapsed))+'\n')
def egybest_geteps2():
    #دالة لايجاد رابيط تحمميل كل حلقة وادخاله في قائمة
    start = time.time()
    sleep(2)
    print('get get eps 2\n')
    #بحث عن حلقات  موسم بموسم
    for i in list_all_eps:
        #قائمة الخاص بروابط موسم واحد فقط
        list_links_eps_one_season=[]
        #بحث عن رابط تحميل حلقة بحقلة
        for l in i:
            #اغلاق tabs الخاص باعلانات ثم تركيز على tab الخاص بحلقة
            while len(driver.window_handles)>=2:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                sleep(1)
                driver.switch_to.window(driver.window_handles[0])
            #قائمة خاصة جودات
            a=[]
            #قائمة خاصة بتحميل
            b=[]
            #فتح صفحة الخاص بحلقة
            driver.get(l)
            #
            #بحث عن تاغ td ثن وضعه في متغير tds
            tds=driver.find_elements_by_tag_name('td')
            for td in tds:
                #ايجاد الخانات المكتوبة عليها جوادت
                if isinstance(td.text, str) and "0p" in td.text:
                    a.append(td.text)
            #بحث عن تاغ a ثم وضعه في متغير dows
            dows=driver.find_elements_by_tag_name('a')
            for dow in dows:
                #بحث عن لازرار التي تحتوي على تحميل
                if  isinstance(dow.get_attribute('class'), str) and dow.get_attribute('class')=="btn g dl nop _open_window":
                    b.append(dow)
            #حذف العنصر الاولى من قائمة الجودات لانو هذا جودة الخاص بتعربف الحلقة الخاص eggybest
            del a[0]
            #ابجاد رقم العنصر الخاص تحميل بدقة 720
            #ثم ضغط عليه لانتقال لصفحة التحميل
            b[a.index('HD 720p')].click()
            sleep(2)
            while len(driver.window_handles)!=0:
                if len(driver.window_handles)>=2:
                    #تحويل تركيز الصفحة من صفحة الحلقة الى صفحة التحميل
                    driver.switch_to.window(driver.window_handles[1])
                    break
                else:
                    sleep(1)
            #بحث عن تاغ a 
            fikelinks=driver.find_elements_by_tag_name('a')
            for fikelink in fikelinks:
                # بحث عن زر التحميل ثم ضغط عليه
                # لفتح الاعلان
                if isinstance(fikelink.get_attribute('class'), str) and fikelink.get_attribute('class')=="bigbutton _reload":
                    fikelink.click()
            sleep(4)
            links=driver.find_elements_by_tag_name('a')
            for l in links:
                # بحث عن زر التحميل ثم اخذ الربط الخاص بتحميل الحلقة
                # ثم وضع في قائمة
                if isinstance(l.get_attribute('class'), str) and l.get_attribute('class')=="bigbutton" and 'EgyBest' in l.get_attribute('href'):
                    list_links_eps_one_season.append(l.get_attribute('href'))
            # خروج من صفحة التحميل
            driver.close()
            #  تركيز على صفحة الخاص بالحلقة
            driver.switch_to.window(driver.window_handles[0])
            sleep(1)
        #اصافة جميع لروابط تحميل الحلقات في قائمة
        list_all_link_download_eps.append(list_links_eps_one_season)
    print('get get eps 2...done\n')
    done = time.time()
    elapsed = done - start
    print('timeget eps 2 is: '+time.strftime('%H:%M:%S', time.gmtime(elapsed))+'\n')

def egybest(url,name):
    start = time.time()
    print('begin\n')
    go_url(url)
    egybest_getseason()
    egybest_geteps1()
    egybest_geteps2()
    driver.quit()
    egybest_text(name)
    print('done')
    done = time.time()
    elapsed = done - start
    print('time all is: '+time.strftime('%H:%M:%S', time.gmtime(elapsed))+'\n')
def egybest_text(name):
    s=0
    for i in list_all_link_download_eps:
        s+=1
        f= open(name+" S 0"+str(s)+".txt","w+")
        for j in i:
            f.write(j+"\n")
        f.close
print('Download all episodes from site EGYBEST')
print('-'*64)
url=input('enter url your searie :')
name=input('enter name your text file :')
egybest(url,name)
