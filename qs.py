from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# 创建空的数据列表用来保存数据
# 排名
rank_all = []
# 大学名称
name_all = []
# 综合得分
scor_all = []


def get_text():

    # rank  排名
    list_rank = driver.find_elements(By.XPATH,'//*[@id="qs-rankings"]/tbody/tr//td[@class=" rank"]')
    for li_rank in list_rank:
        rank = li_rank.find_element(By.XPATH,'./div').text
        # 保存数据到列表
        rank_all.append(rank)
        
    # name  大学名称
    list_name = driver.find_elements(By.XPATH,'//*[@id="qs-rankings"]/tbody/tr//td[@class=" uni"]')
    for li_name in list_name:
        name = li_name.find_element(By.XPATH,'./div/a').text
        # 保存数据到列表
        name_all.append(name)

    # 综合得分
    list_scor = driver.find_elements(By.XPATH,'//*[@id="qs-rankings"]/tbody/tr//td[@class="overall sorting_1"]')
    for li_scor in list_scor:
        scor = li_scor.find_element(By.XPATH,'./div').text
        # 保存数据到列表
        scor_all.append(scor)


# 设置浏览器路径
servic = Service(executable_path=r'D:\\edgedriver_win64\\msedgedriver.exe')
driver = webdriver.Edge(service=servic)

# 获取网页
driver.get("https://www.qschina.cn/en/university-rankings/world-university-rankings/2024")
time.sleep(2)


# 获取第一页数据  #####################
get_text()
#print(len(rank_all) == len(name_all) == len(scor_all))


# 获取第二页数据   #########################
# 滚动东滑轮下滑
driver.execute_script("document.documentElement.scrollTop=2700")
time.sleep(2)
# 进行翻页
driver.find_element(By.XPATH,'//*[@id="qs-rankings_next"]').click()
# 获取第二页数据
get_text()
#print(len(rank_all) == len(name_all) == len(scor_all))
time.sleep(1.5)



# 从第三页开始 循环爬取#######
# 此处page设置需要的页数
page = 22
i = 1

# 由于前面已经获取了两页数据，用page-2 来把页数统一
while i <= page-2:
    driver.execute_script("document.documentElement.scrollTop=2700")
    time.sleep(2)
    # 进行翻页
    try:
        next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="qs-rankings_next"]'))
    )
        next_button.click()
    except TimeoutException:
        print("Timeout: Next button not found or not clickable")
    # 获取第三页数据
    get_text()
    if not (len(rank_all) == len(name_all) == len(scor_all)):
        print(i)
    time.sleep(1.5)
    i += 1


# 数据合并为数据表
data = pd.DataFrame({
    '排名':rank_all,
    '英文名称':name_all,
    '综合得分':scor_all,
})

# 保存为CSV文件
data.to_csv('D:/vscode/QS.csv',index=False)


# 下面代码可用可不用
#查看数据前5行，可以检查下数据看是想要的样子
data.head()
