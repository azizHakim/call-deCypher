import json

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

def post_process_facts(facts):
    fact_list = facts.split('\n')

    for i in range(len(fact_list)):
        if fact_list[i] == "":
            fact_list.pop(i)
        elif fact_list[i][0:2] == "- ":
            fact_list[i] = fact_list[i][2:]
        
    return fact_list


def process_result(question, facts, result_path):
    result = {}
    result["question"] = question
    result["facts"] = facts
    result["status"] = "done"

    with open(result_path, "w") as file:
        json.dump(result, file, indent=4)
    file.close()
