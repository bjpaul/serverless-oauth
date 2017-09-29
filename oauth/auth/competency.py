from common.config import Config

cnf = Config()


def list_competency_config():
    list_competency = []
    list_competency.append({cnf.competency_name_key: "DevOps", cnf.competency_color_code_key: "#eb5525"})
    list_competency.append({cnf.competency_name_key: "JVM", cnf.competency_color_code_key: "#d63bff"})
    return list_competency
