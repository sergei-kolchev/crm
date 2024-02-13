from tables.builders import (ObjectFactory, TableBodyCellBuilder,
                             TableButtonsCellBuilder, TableHeaderCellBuilder)

__all__ = ["factory"]


factory = ObjectFactory()
factory.register_builder("header_cell", TableHeaderCellBuilder())
factory.register_builder("body_cell", TableBodyCellBuilder())
factory.register_builder("buttons_cell", TableButtonsCellBuilder())
