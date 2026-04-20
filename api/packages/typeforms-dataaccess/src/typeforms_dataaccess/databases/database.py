import databases
import sqlalchemy

def create_database(database_url: str, force_rollback: bool = False):
    metadata = sqlalchemy.MetaData()

    _form_table = sqlalchemy.Table(
        'form',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
        sqlalchemy.Column('title', sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            'created_at',
            sqlalchemy.DateTime,
            nullable=False,
            server_default=sqlalchemy.func.now()
        ),
        sqlalchemy.Column(
            'modified_at',
            sqlalchemy.DateTime,
            nullable=False,
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now()
        ),
    )

    _field_table = sqlalchemy.Table(
        'field',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
        sqlalchemy.Column('form_id', sqlalchemy.String, sqlalchemy.ForeignKey('form.id'), nullable=False),
        sqlalchemy.Column('label', sqlalchemy.String, nullable=False),
        sqlalchemy.Column('field_type', sqlalchemy.String, nullable=False),
        sqlalchemy.Column('order', sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column('required', sqlalchemy.Boolean, nullable=False),
        sqlalchemy.Column('config', sqlalchemy.Text, nullable=False),
    )

    sync_url = database_url.replace("sqlite+aiosqlite", "sqlite")
    engine = sqlalchemy.create_engine(
        sync_url,
        connect_args={"check_same_thread": False}
    )

    metadata.create_all(engine)

    return databases.Database(database_url, force_rollback=force_rollback)