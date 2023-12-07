from scholarly import scholarly
import pandas as pd

def get_citation_count(publication):
    return publication['num_citations']

def get_author_impact(author):
    return author['hindex']

def get_institution_ranking(publication, df):
    institution_row = df[df['中文名称'] == publication['affiliation']]
    if not institution_row.empty:
        institution_ranking = institution_row['目录排名'].values[0]
        return institution_ranking
    else:
        return "机构排名信息不可用"

# 输入作者名字和文献名字
author_name = input("请输入作者的名字：")
publication_title = input("请输入文献的名字：")

# 搜索作者
search_query = scholarly.search_author(author_name)
# 获取第一个结果
author_result = next(search_query)

# 填充作者信息
author = scholarly.fill(author_result)

# 搜索文献
search_query = scholarly.search_pubs(publication_title)
# 获取第一个结果
publication_result = next(search_query)

# 填充文献信息
publication = scholarly.fill(publication_result)

# 读取 QS 世界大学排名文件
df = pd.read_csv(r'D:/vscode/QS.csv')

# 获取文献的引用率
citation_count = get_citation_count(publication)
print("文献引用率：", citation_count)

# 获取作者的影响力因素
impact_factor = get_author_impact(author)
print("作者影响力因素：", impact_factor)

# 获取机构排名
institution_ranking = get_institution_ranking(publication, df)
print("机构排名：", institution_ranking)

# 加权平均计算重要性评估
citation_weight = 0.4
impact_weight = 0.3
ranking_weight = 0.3

importance_score = (citation_weight * citation_count +
                    impact_weight * impact_factor +
                    ranking_weight * institution_ranking)

print("重要性评估：", importance_score)
