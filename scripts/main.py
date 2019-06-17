from postgisAccessor import PostgisAccessor
from embrapa import Embrapa


if __name__ == '__main__':
    storager = PostgisAccessor(host='localhost', username='postgres', password='postgres', database='amostras')

    embrapa = Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager=storager)

    embrapa.load_data_sets()

    embrapa.store()