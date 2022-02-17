
import csv
import itertools

from pymed import PubMed


# Пример 1 Построение графа авторов
# not required but kindly!!! requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="Авторы.Соавторы 0 анализируем", email="my@email.address")

# Создаем GraphQL query по запросу в заголовке
query = "SARS COV-2[Title]"
print("Найдено", pubmed.getTotalResultsCount(query))

# выполняем
results = list(pubmed.query(query, max_results=10000))

# Создаем Node для каждого author
nodes = {
    author: index
    for index, author in enumerate(
        set(
            itertools.chain.from_iterable(
                [
                    [
                        f'{author["lastname"]} {author["firstname"]}'
                        for author in article.authors
                    ]
                    for article in results
                ]
            )
        )
    )
}

# Создаем связи с соавторами (each combination authors-co-authorship)
edges = list(
    itertools.chain.from_iterable(
        [
            [combination for combination in itertools.combinations(co_author_list, 2)]
            for co_author_list in [
                [
                    nodes[f'{author["lastname"]} {author["firstname"]}']
                    for author in article.authors
                ]
                for article in results
            ]
        ]
    )
)

# Удаляем дупликаты и расчитываем веса
edges = set([(edge[0], edge[1], edges.count(edge)) for edge in edges])


# пишем в файлы
with open("./nodes.csv", "w", encoding="utf8", newline="") as nodes_file:

    # CSV writer
    writer = csv.writer(nodes_file, delimiter=",")

    # header
    writer.writerow(["id", "label"])

    # каждому автору - строка
    for name, index in nodes.items():
        writer.writerow([index, name])


with open("./edges.csv", "w", encoding="utf8", newline="") as edge_file:

    #CSV
    writer = csv.writer(edge_file, delimiter=",")

    # веса
    writer.writerow(["source", "target", "weight"])


    for edge in edges:
        writer.writerow(edge)


# Второй пример работы с данными запроса

from pymed import PubMed


# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="my@email.address")


query = "occupational health[Title]"

# выполняем и показываем первые 500
results = pubmed.query(query, max_results=500)


for article in results:
    print(type(article))
    print(article.toJSON())


# Третий пример работы с данными
# Формирование сложного поискового запроса
from pymed import PubMed

#
pubmed = PubMed(tool="MyTool", email="e.p@d-health.pro")


query = '(("2018/05/01"[Date - Create] : "3000"[Date - Create])) AND (erectyile dysfunction[Title] AND diabetes)'
("Найдено", pubmed.getTotalResultsCount(query))


results = pubmed.query(query, max_results=500)


for article in results:

    # Extract and format information from the article
    article_id = article.pubmed_id
    title = article.title
    if article.keywords:
        if None in article.keywords:
            article.keywords.remove(None)
        keywords = '", "'.join(article.keywords)
    publication_date = article.publication_date
    abstract = article.abstract

    # покажем раздел abstract
    print(
        f'{article_id} - {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
    )


from pymed import PubMed

pubmed = PubMed(tool="MyTool", email="my@email.address")


query = '(("2018/05/01"[Date - Create] : "3000"[Date - Create])) AND (Xiaoying Xian[Author] OR diabetes)'
print("Найдено", pubmed.getTotalResultsCount(query))


results = pubmed.query(query, max_results=500)


for article in results:


    article_id = article.pubmed_id
    title = article.title
    if article.keywords:
        if None in article.keywords:
            article.keywords.remove(None)
        keywords = '", "'.join(article.keywords)
    publication_date = article.publication_date
    abstract = article.abstract


    print(
        f'{article_id} - {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
    )
