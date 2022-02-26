from backendmodular.models import Receitas


def tests_receitas_to_json():
    item = Receitas()
    item.titulo = "Feijoada"
    item.descricao = "Prato típico"

    item_json = item.to_json()

    assert type(item_json) == dict


def tests_receitas_to_string():
    item = Receitas()
    item.titulo = "Feijoada"
    item.descricao = "Prato típico"

    item_str = str(item)

    assert type(item_str) == str
