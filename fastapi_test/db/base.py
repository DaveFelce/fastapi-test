# pylint: disable=wildcard-import,unused-import,unused-wildcard-import

# Import all the models, so that Base has them before being
# imported by Alembic
from fastapi_test.db.base_class import Base  # noqa
from fastapi_test.models import *  # noqa
