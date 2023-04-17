from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from engine import Base, engine


class ColorModel(Base):
    """ORM model for wares colors. Seems useless."""
    __tablename__ = 'colors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    objects: Mapped[list['ObjectModel']] = relationship(
        back_populates='colors'
    )


class ObjectModel(Base):
    """ORM model for wares."""
    __tablename__ = 'things'
    nm_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    brand: Mapped[str]
    brand_id: Mapped[int]
    site_brand_id: Mapped[int]
    supplier_id: Mapped[int]
    sale: Mapped[int]
    price: Mapped[int]
    sale_price: Mapped[int]
    rating: Mapped[float]
    feedbacks: Mapped[int]
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id'))
    colors: Mapped['ColorModel'] = relationship(back_populates='objects')

    def json(self):
        return {
            'nm_id': self.nm_id,
            'name': self.name,
            'brand': self.brand,
            'brand_id': self.brand_id,
            'site_brand_id': self.site_brand_id,
            'supplier_id': self.supplier_id,
            'sale': self.sale,
            'price': self.price,
            'sale_price': self.sale_price,
            'rating': self.rating,
            'feedbacks': self.feedbacks,
            'colors': {'id': self.colors.id, 'name': self.colors.name}
        }


Base.metadata.create_all(engine)
