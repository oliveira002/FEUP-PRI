import json

import requests
from sentence_transformers import SentenceTransformer


def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str


def solr_knn_query(endpoint, collection, data):  # endpoint, collection, embedding, n_results):
    url = f"{endpoint}/{collection}/select"

    '''data = {
        "q": f"{{!knn f=vector topK={n_results}}}{embedding}",
        "fl": "id,name,desc,full_desc,score",
        "qf": "name desc full_desc",
        "rows": n_results,
        "defType": "edismax",
        "wt": "json"
    }'''

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()


def display_results(results):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return

    for doc in docs:
        # print(f"* {doc.get('id')} {doc.get('name')} [score: {doc.get('score'):.2f}]")
        print(doc)


def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "games"

    # query_text = input("Enter your query: ")

    n_results = 10
    q1 = text_to_embedding("(\"water setting\"~3)^2 OR (\"underwater setting\"~2)^4")
    q4 = text_to_embedding("(historical)^2 AND (command army)^3")
    q5 = text_to_embedding("\"2D platform*\"~2\n((\"play animal\"~3^2) OR (\"control animal\"~3^2))")
    q6 = text_to_embedding("\"open world\"~2\n\"RPG\"^3\n\"fantasy realms\"~2")

    #q1_l = text_to_embedding("full_desc:(\"water setting\"~3)^2 OR full_desc:(\"underwater setting\"~2)^4 OR desc:("
    #                         "\"water setting\"~3)^2 OR desc:(\"underwater setting\"~2)^4")
    q1_l = text_to_embedding("underwater setting")
    #q4_l = text_to_embedding("(full_desc:(historical)^2 AND full_desc:(command army)^3) OR (desc:(historical)^2 AND "
    #                         "desc:(command army)^3)")
    q4_l = text_to_embedding("historical games where you command an army")
    #q5_l = text_to_embedding('(full_desc:"2D platform*"~2 AND ((full_desc:"play animal"~3^2) OR full_desc:("control '
    #                         'animal"~3^2))) OR(desc:"2D platform*"~2 AND ((desc:"play animal"~3^2) OR desc:("control'
    #                         ' animal"~3^2)))')
    q5_l = text_to_embedding("platformer where you play as an animal")
    #q6_l = text_to_embedding('(full_desc:"open world"~2 AND full_desc:"RPG"^3 AND full_desc:"fantasy realms"~2) OR ('
    #                         'desc:"open world"~2 AND desc:"RPG"^3 AND desc:"fantasy realms"~2)'
    q6_l = text_to_embedding("open world RPG with fantasy realms")

    queries = {
        "q1_edismax": {
            "q": f"{{!knn f=vector topK={n_results}}}{q1}",
            "defType": "edismax",
            "indent": "true",
            "qf": "full_desc desc",
            "fl": "id,name,desc,full_desc,score",
            # "q.op": "AND",
            "rows": n_results,
            "fq": "categories: single-player date:[NOW/DAY-3653DAYS TO NOW]",
            "lowercaseOperators": "true",
            "wt": "json"
        },
        "q4_edismax": {
            "q": f"{{!knn f=vector topK={n_results}}}{q4}",
            "defType": "edismax",
            "bf": "linear(all_reviews,0,100)^1.5",
            "indent": "true",
            "qf": "full_desc desc",
            "fl": "id,name,desc,full_desc,score",
            # "q.op": "AND",
            "rows": n_results,
            "lowercaseOperators": "true",
            "wt": "json"
        },
        "q5_edismax": {
            "q": f"{{!knn f=vector topK={n_results}}}{q5}",
            "defType": "edismax",
            "indent": "true",
            "qf": "full_desc desc",
            "fl": "id,name,desc,full_desc,score",
            # "q.op": "AND",
            "rows": n_results,
            "lowercaseOperators": "true",
            "wt": "json"
        },
        "q6_edismax": {
            "q": f"{{!knn f=vector topK={n_results}}}{q6}",
            "defType": "edismax",
            "bf": "product(if(exists(query({!v='name:\"RPG\"'})),2,1),exp(product(all_reviews,0.03)))",
            "indent": "true",
            "qf": "full_desc desc",
            "fl": "id,name,desc,full_desc,score",
            # "q.op": "AND",
            "rows": n_results,
            "lowercaseOperators": "true",
            "wt": "json"
        },
        "q1_lucene": {
            "q": f"{{!knn f=vector topK={n_results}}}{q1_l}",
            "defType": "lucene",
            "indent": "true",
            "fl": "id,name,desc,full_desc,score",
            "q.op": "AND",
            "rows": n_results,
            "fq": "categories: single-player date:[NOW/DAY-3653DAYS TO NOW]",
            "wt": "json"
        },
        "q4_lucene": {
            "q": f"{{!knn f=vector topK={n_results}}}{q4_l}",
            "defType": "lucene",
            "indent": "true",
            "fl": "id,name,desc,full_desc,score",
            "q.op": "AND",
            "rows": n_results,
            "wt": "json"
        },
        "q5_lucene": {
            "q": f"{{!knn f=vector topK={n_results}}}{q5_l}",
            "defType": "lucene",
            "indent": "true",
            "fl": "id,name,desc,full_desc,score",
            "q.op": "AND",
            "rows": n_results,
            "wt": "json"
        },
        "q6_lucene": {
            "q": f"{{!knn f=vector topK={n_results}}}{q6_l}",
            "defType": "lucene",
            "indent": "true",
            "fl": "id,name,desc,full_desc,score",
            "q.op": "AND",
            "rows": n_results,
            "wt": "json"
        }
    }

    for key in queries:

        query = queries[key]
        # embedding = text_to_embedding(query["q"])

        try:
            results = solr_knn_query(solr_endpoint, collection, query)

            file_path = f"{key}.json"
            with open(file_path, 'w') as json_file:
                json.dump(results.get("response", {}).get("docs", []), json_file, indent=2)

        except requests.HTTPError as e:
            print(f"Error {e.response.status_code}: {e.response.text}")


if __name__ == "__main__":
    main()
