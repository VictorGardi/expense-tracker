import os
from sqlalchemy import create_engine

ENGINE = create_engine(f"sqlite:///{os.environ['SQLITE_URI']}")
