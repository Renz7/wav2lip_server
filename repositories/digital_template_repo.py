from loguru import logger

from internal.db.models import DigitalTemplate
from schema.template import Template
from . import BaseRepository


class DigitalTemplateRepo(BaseRepository):
    __clz__ = DigitalTemplate

    def get_model_clz(self):
        return DigitalTemplate

    def get_templates(self, page, size=10):
        offset = max((page - 1) * size, 0)
        result = self.db.query(DigitalTemplate).order_by(DigitalTemplate.updated_at.desc()).offset(offset).limit(
            size).all()
        logger.info(f"find {len(result)} template from db")

        return list(map(Template.from_db, result))

    def create_template(self, template: DigitalTemplate):
        self.db.add(template)
        self.db.commit()
