import pygraphviz as pgv
from sqlalchemy import MetaData
from models import engine

# Crea una instancia de MetaData y asóciala con tu motor de base de datos
metadata = MetaData()
metadata.reflect(bind=engine)

# Crea un gráfico del esquema
graph = pgv.AGraph(strict=False, directed=True)

# Agrega nodos y relaciones al gráfico
for table in metadata.tables.values():
    graph.add_node(table.name, shape='rectangle')
    for fk in table.foreign_keys:
        graph.add_edge(table.name, fk.column.table.name)

# Renderiza el gráfico como una imagen
graph.draw('database_diagram.png', prog='dot')


