import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
import argparse
from selenium import webdriver
import datetime
import re

ABS_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
#DEFAULT_COMMIT = "Configuration Change"
#CRAD_FILE = "Card.dat"

# ///////////////////////////////////////////////////////////////////////////
# read_text
# //////////////////////////////////////////////////////////////////////////

class AllData:

    def __init__(self, Id_ransome_url):
        self.Id_ransome_url = Id_ransome_url
        self.list_of_VT = []
        self.list_of_sha = []
        self.list_of_ransome_note = []


    def __init__(self, Id_ransome_url, list_of_VT, list_of_sha, list_of_ransome_note):
        self.Id_ransome_url = Id_ransome_url
        self.list_of_VT = list_of_VT
        self.list_of_sha = list_of_sha
        self.list_of_ransome_note = list_of_ransome_note


# ///////////////////////////////////////////////////////////////////////////
# read_text
# //////////////////////////////////////////////////////////////////////////

def read_text(xpath, sleep_time, driver):
    #fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath))) #contains elemnts of XPATH
    fields = driver.find_elements_by_xpath(xpath)
    for field in fields:
        print(field.text)
    time.sleep(sleep_time)
    return field

# ///////////////////////////////////////////////////////////////////////////
# get all sha's
# //////////////////////////////////////////////////////////////////////////

def get_sha_from_link_list(link_list):
    sha_list = []
    for link in link_list:
        sha_list.append(re.findall(r"virustotal\..*\/\w+\/\w+/(\w+)\/", link))
        print(link)
    return sha_list

# ///////////////////////////////////////////////////////////////////////////
# get all Data //link and data
# //////////////////////////////////////////////////////////////////////////

def get_all_Data(driver , field, sleep_time):
    url_list = []
    from selenium.webdriver.common.keys import Keys
    for f in field:
        current_url = driver.current_url #i want to get the current url
        f.send_keys(Keys.CONTROL + Keys.ENTER) #open a new tab
        time.sleep(sleep_time) #uploding the page
        try:
         driver.switch_to.window(driver.window_handles[1]) #replace to the next tab
         extention_arr = get_extension_from_id_ransomware(sleep_time, driver)
         get_read_me(sleep_time, driver)
         url_list.append(driver.current_url) #here we get the currnt new url
         print(driver.current_url) # Printing all the urls
         driver.close() #closing the tab
         driver.switch_to.window(driver.window_handles[0]) #switch to the first
        except:
            continue
    return url_list

# ///////////////////////////////////////////////////////////////////////////
# get all links
# //////////////////////////////////////////////////////////////////////////

def get_all_links(driver , field, sleep_time):
    url_list = []
    from selenium.webdriver.common.keys import Keys
    for f in field:
        #current_url = driver.current_url #i want to get the current url
        print("id ransome url {}".format(driver.current_url))
        f.send_keys(Keys.CONTROL + Keys.ENTER) #open a new tab
        time.sleep(sleep_time) #uploding the page
        try:
         driver.switch_to.window(driver.window_handles[1]) #replace to the next tab
         url_list.append(driver.current_url) #here we get the currnt new url
         print("Vt url {}".format(driver.current_url))
         driver.close() #closing the tab
         driver.switch_to.window(driver.window_handles[0]) #switch to the first
        except:
            continue
    return url_list

# ///////////////////////////////////////////////////////////////////////////
# get all extension's
# //////////////////////////////////////////////////////////////////////////


def get_extension_from_id_ransomware(sleep_time, driver):
    try:
        read_me_arr = read_text(r'//span[contains(text(),"записка")]/b', sleep_time, driver)
        print(read_me_arr)
        return read_me_arr
    except:
        return ""

# ///////////////////////////////////////////////////////////////////////////
# get rensome sha
# //////////////////////////////////////////////////////////////////////////

def get_ransome_comments_sha(shas):
    comments_url = r"https://www.virustotal.com/ui/files/{}/comments"
    ransome_sha = []
    import requests
    for sha in shas:
        time.sleep(5)
        comment_url = comments_url.format(sha)
        req = requests.get(url=comment_url)
        data_json = req.json()
        if "#ransomware" in data_json['data'][0]['text']:
            ransome_sha.append(sha)
    return ransome_sha

# ///////////////////////////////////////////////////////////////////////////
# get note is called - Read ME
# //////////////////////////////////////////////////////////////////////////

def get_read_me(sleep_time, driver):
    try:
        extension_arr = read_text(r'//span[contains(text(),"записка")]/b/span', sleep_time, driver)
        print(extension_arr)
        return extension_arr
    except:
        return ""


# ///////////////////////////////////////////////////////////////////////////
# get ssdeep
# //////////////////////////////////////////////////////////////////////////

def get_ssdeep(sha):
    json_url = r"https://www.virustotal.com/ui/files/{}".format(sha)
    import requests
    time.sleep(1)
    req = requests.get(url=json_url)
    data_json = req.json()
    return data_json['data']['attributes']['ssdeep']

# ///////////////////////////////////////////////////////////////////////////
# Run WebDriver
# //////////////////////////////////////////////////////////////////////////

def run(month, year):
    list_of_AllData_class = []

    sleep_time = 0.5
    driver = webdriver.Chrome(r"C:\Driver\chromedriver.exe")
    wait = WebDriverWait(driver, 10)

    driver.get('http://id-ransomware.blogspot.com/{y}/{m}/'.format(y=year, m=month))

    all_urls = wait.until(EC.presence_of_all_elements_located((By.XPATH, r"//li/a[contains(@href,'http://id-ransomware.blogspot.com/2019/')]")))

    # list_of_all_data_class init
    for url in all_urls:
        alldata = AllData(url)
        list_of_AllData_class.append(alldata)

    # Here is the place that all the tables are open - put commit on all the block use CTRL / for comment

     #list of links - all  the links of id ransomware
     list_of_links = get_all_Data(driver, all_urls, sleep_time)
    ## list_of_links = ['http://id-ransomware.blogspot.com/2019/', 'http://id-ransomware.blogspot.com/2019/01/', 'http://id-ransomware.blogspot.com/2019/01/vulston-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/crycipher-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/retmydata-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/boom-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/indrik-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/crytekk-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/ahihi-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/crypt0r-ransomware_10.html', 'http://id-ransomware.blogspot.com/2019/01/juwon-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/scarab-zzz-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/hant-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/trumphead-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/bigbobross-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/anatova-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/xcry-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/scarab-crash-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/james-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/enc1-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/t1happy-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/vaca-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/jsworm-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/australian-aes-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/drakos-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/cyspt-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/scarab-gefest-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/spiteful-doubletake.html', 'http://id-ransomware.blogspot.com/2019/01/gorgon-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/lockergoga-worker32-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/mewware-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/unnamed-desync-ransomware.html', 'http://id-ransomware.blogspot.com/2019/01/xorist-mcafee-ransomware.html', 'http://id-ransomware.blogspot.com/2019/02/', 'http://id-ransomware.blogspot.com/2019/03/', 'http://id-ransomware.blogspot.com/2019/04/', 'http://id-ransomware.blogspot.com/2019/05/', 'http://id-ransomware.blogspot.com/2019/06/', 'http://id-ransomware.blogspot.com/2019/07/']
     vt_link_list = []
     for link in list_of_links:
          try:
              driver.get(link)  #the current link - id ransoware
              field = wait.until(EC.presence_of_all_elements_located((By.XPATH, r"//b/a[contains(@href,'https://www.virustotal.com')]")))
              list = get_all_links(driver, field, sleep_time)
              vt_link_list = vt_link_list + list
          except:
              continue

    #vt_link_list = ['https://www.virustotal.com/gui/file/574b7439b7469ed10331f4f383da0631a78c71b388eab0db1399d8606108b0ea/detection', 'https://www.virustotal.com/gui/file/1fd388f506aab965c43f691204fc3fafa2eb59f667cbf840bc6cfc5a0403c318/detection', 'https://www.virustotal.com/gui/file/7c98962fbb6616a45efb550bf1f3b088def54447a83f815496a6e6e7c7bd0b4b/detection', 'https://www.virustotal.com/gui/file/bdf36127817413f625d2625d3133760af724d6ad2410bea7297ddc116abc268f/detection', 'https://www.virustotal.com/gui/file/8cfbd38855d2d6033847142fdfa74710b796daf465ab94216fbbbe85971aee29/detection', 'https://www.virustotal.com/gui/file/7852b47e7a9e3f792755395584c64dd81b68ab3cbcdf82f60e50dc5fa7385125/detection', 'https://www.virustotal.com/gui/file/47f5a231f7cd0e36508ca6ff8c21c08a7248f0f2bd79c1e772b73443597b09b4/detection', 'https://www.virustotal.com/gui/file/c97d9bbc80b573bdeeda3812f4d00e5183493dd0d5805e2508728f65977dda15/detection', 'https://www.virustotal.com/gui/file/7bcd69b3085126f7e97406889f78ab74e87230c11812b79406d723a80c08dd26/detection', 'https://www.virustotal.com/gui/file/928259fda8a87ca09db0e3554f3b40f392a508aed6b0e6d07d7a1a1fee69c255/detection', 'https://www.virustotal.com/gui/file/a600050d638f35a5b82af24b3d0e0bfc9f1652f82d3ec36851edb90cef202dc1/detection', 'https://www.virustotal.com/gui/file/3e69829b720e8ee3570788b54b1c5f8ea35751a0760f842a8f92f76979e94a1f/detection', 'https://www.virustotal.com/gui/file/63b541a11d8389b13c634665ba72437270cd8bbbbc3df7dc43acfe201a5a67e5/detection', 'https://www.virustotal.com/gui/file/d620778dbbcf11e3a293aeaaebac7b6a9a02e7d8790ca5ffa59bda1e9b9632f4/detection', 'https://www.virustotal.com/gui/file/0eff6a71d9bd1549d4c12bc984ed722b9139f75615d4adcb49f9ec240afe9d7d/detection', 'https://www.virustotal.com/gui/file/c478913dd84ce396f66cefa88e23588100aab951ff1b01aac9ea72fac12611b1/detection', 'https://www.virustotal.com/gui/file/ead07ed5f62afb8b706f35bbbc8b5d3cc58d337aae560a32af2bd8835b7e858f/detection', 'https://www.virustotal.com/gui/file/89f35f20af62201010e3218a22c50ed6994c79fb6f9f2210fd55203e6e6b01a1/detection', 'https://www.virustotal.com/gui/file/08184f452cccd8ab7e3908b85e6a69cda9afe46c4a09dbadad0846eff37ae535/detection', 'https://www.virustotal.com/gui/file/2ae60779c8cc38911a5489fb77e7ef0cb02131fd17a509c9f0e85648ae9fe929/detection', 'https://www.virustotal.com/gui/file/2fec3892efa6ad300ff1d5334875d94e0470bf1b4e71449b10221f790f5f2d3a/detection', 'https://www.virustotal.com/gui/file/615df3284db695a629aa21a8f06d4d2a00c51659ca55effe283a76e3d361698a/detection', 'https://www.virustotal.com/gui/file/170fb7438316f7335f34fa1a431afc1676a786f1ad9dee63d78c3f5efd3a0ac0/detection', 'https://www.virustotal.com/gui/file/bd422f912affcf6d0830c13834251634c8b55b5a161c1084deae1f9b5d6830ce/detection', 'https://www.virustotal.com/gui/file/ab8a76b64448b943dc96a3e993b6e6b37af27c93738d27ffd1f4c9f96a1b7e69/detection', 'https://www.virustotal.com/gui/file/97fb79ca6fc5d24384bf5ae3d01bf5e77f1d2c0716968681e79c097a7d95fb93/detection', 'https://www.virustotal.com/gui/file/bd422f912affcf6d0830c13834251634c8b55b5a161c1084deae1f9b5d6830ce/detection', 'https://www.virustotal.com/gui/file/e32c8b2da15e294e2ad8e1df5c0b655805d9c820e85a33e6a724b65c07d1a043/detection', 'https://www.virustotal.com/gui/file/680949c3c5b4b6ffdbe297fcb15096b5d53c8480d0c53ab4dd9801d711a78f31/detection', 'https://www.virustotal.com/gui/file/9da7d298691613a398e26ac3c4c4e4e9c93069d2162fa6639901dd7c62774ef5/detection', 'https://www.virustotal.com/gui/file/8e9cea6c59e7e54edb950b2b93f29a26b4017e727c573ea2cbeb83a16e3e2063/detection', 'https://www.virustotal.com/gui/file/895ea8c17794b3ca0d0aa44ec8aaab43e9213fef2dedeceb1193d77f09f50d1f/detection', 'https://www.virustotal.com/gui/file/256257d0eee5998402959bf447040246fcb14e030cb19f38cbf8dd0076eac7fb/detection', 'https://www.virustotal.com/gui/file/14ac012d01046b4f4e92f95b3da5fc2e34b90af2d0243a2e774e5938885d7817/detection', 'https://www.virustotal.com/gui/file/52389889be43b87d8b0aecc5fb74c84bd891eb3ce86731b081e51486378f58d2/detection', 'https://www.virustotal.com/gui/file/6e4b5f03370f782dbb46c1f4e24c4a55ef5bd57dbdadd8fb4c2d02253a038473/detection', 'https://www.virustotal.com/gui/file/fab4f72a1645e8520887f966b04fc557e2517c612c9a606594964c5df7857fc6/detection', 'https://www.virustotal.com/gui/file/77642c40eddc84ae332f2da7c9fed81c9438eb69c8b2a4f01996d5fbbe788cf2/detection', 'https://www.virustotal.com/gui/file/bdf36127817413f625d2625d3133760af724d6ad2410bea7297ddc116abc268f/detection', 'https://www.virustotal.com/gui/file/8cfbd38855d2d6033847142fdfa74710b796daf465ab94216fbbbe85971aee29/detection', 'https://www.virustotal.com/gui/file/7852b47e7a9e3f792755395584c64dd81b68ab3cbcdf82f60e50dc5fa7385125/detection', 'https://www.virustotal.com/gui/file/47f5a231f7cd0e36508ca6ff8c21c08a7248f0f2bd79c1e772b73443597b09b4/detection', 'https://www.virustotal.com/gui/file/c97d9bbc80b573bdeeda3812f4d00e5183493dd0d5805e2508728f65977dda15/detection', 'https://www.virustotal.com/gui/file/7bcd69b3085126f7e97406889f78ab74e87230c11812b79406d723a80c08dd26/detection', 'https://www.virustotal.com/gui/file/7c98962fbb6616a45efb550bf1f3b088def54447a83f815496a6e6e7c7bd0b4b/detection', 'https://www.virustotal.com/gui/file/8f20197da8f44485dbec10674cc2df0a48422d4c2c1308d17aa065a5c1ce445e/detection', 'https://www.virustotal.com/gui/file/19b01a24191ab410923c22f152a4c5a4cfd4ec5a7eb2f71e6f98f89412d9f766/detection', 'https://www.virustotal.com/gui/file/7cdd7e30c7091fd2fa3e879dd70087517412a165bf14c4ea4fd354337f22c415/detection', 'https://www.virustotal.com/gui/file/d9e25125a32ad911b55796bcd2b030800d5bf93a27d41e8349c08ded771bfc7f/detection', 'https://www.virustotal.com/gui/file/a98b678578e4d937de8a1f1557286da6df74abac0b49081829a81c886c3a92a3/detection', 'https://www.virustotal.com/gui/file/42dc69a5e31a8cba294b9488d98c415e69925d387bd7b80d637b37c02811226b/detection', 'https://www.virustotal.com/gui/file/d36e6282363c0f9c05b7b04412d10249323d8b0000f2c25f96c6f9de207eedf8/detection', 'https://www.virustotal.com/gui/file/0fa207940ea53e2b54a2b769d8ab033a6b2c5e08c78bf4d7dade79849960b54d/detection', 'https://www.virustotal.com/gui/file/71a20e270052665d18bc0fe4d1f9608e51f4fd427442e7abc3e5d43c4e987bdb/detection', 'https://www.virustotal.com/gui/file/598026f268510c729563809649b5c719e07ad6b95461b980bdcd7571120e993d/detection', 'https://www.virustotal.com/gui/file/7558b47e44541d2417d91ce9308ada497f41fb2f550d9bc43231634fe2c1d5b9/detection', 'https://www.virustotal.com/gui/file/74f9b8d8ad9cd5da148c4459560be843ee9443bf01e2bc7dff77fb333a470196/details', 'https://www.virustotal.com/gui/file/b40b147728289e7d7216008c66a7c94ea9adf5a3d37b3dac1099d4524391f3b4/detection', 'https://www.virustotal.com/gui/file/66a3172e0f46d4139cc554c5e2a3a5b6e2179c4a14aff7e788bb9cc98a2219d5/detection', 'https://www.virustotal.com/gui/file/8d833937f4da8ab0269850f961e8a9f963c23e6bef04a31af925a152f01a1169/detection', 'https://www.virustotal.com/gui/file/3ee4607ed06c270fdf9ddfde65da676d2547607bad420a8114767309b17adfeb/detection', 'https://www.virustotal.com/gui/file/52e322f3bc43d1c6ac27e2449934894f1eeb27645244650c3a219a69879d41fe/details', 'https://www.virustotal.com/gui/item-not-found', 'https://www.virustotal.com/gui/file/1fd388f506aab965c43f691204fc3fafa2eb59f667cbf840bc6cfc5a0403c318/detection']
    shas = get_sha_from_link_list(vt_link_list)

    #ransome_shas = get_ransome_sha(shas)


    with open("ransome_repoert.csv", 'w') as f:
        for sha in shas:
            # ssdeep = get_ssdeep(sha[0])
            # f.write("ssdeep: {}".format(ssdeep))
            f.write("sha: {}".format(sha))

      #   shas=''.join(str(e) for e in shas)
      #   #f.write(shas, sep = ", ")
      #   f.write("ransome_sha: \n")
      # #  f.write(ransome_shas, sep=", ")
      #   f.write("ssdeep:\n")
      #   ssdeep = ''.join(str(i) for i in ssdeep)
      #   f.write("note read me:\n")


# /////////////////////////////////////////////////////////////////////////
# parse_input_args
# <INPUT - args>                             Args object
# <RETURN VALUE - parser.parse_args(args)>   All the arguments that been parsed
# ////////////////////////////////////////////////////////////////////////

def parse_input_args(args):
    parser = argparse.ArgumentParser(
        description='This tool is automation to create a pull request')
    parser.add_argument('-s', '--sha',
                        help='get sha')
    return parser.parse_args(args)

# ///////////////////////////////////////////////////////////////////////////
# Main
# //////////////////////////////////////////////////////////////////////////

def main(args):
    argv = parse_input_args(args)

    if argv.sha:
        sha = argv.sha
        ssdeep = get_ssdeep(sha)
        print(ssdeep)
        return
    else:
        sha = ""

    month = "01"
    year = "2019"
    run(month, year)

if __name__ == "__main__":
    main(sys.argv[1:])



