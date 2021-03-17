import datetime
import json
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, MetaData, Table, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Row
from sqlalchemy.exc import NoResultFound, ProgrammingError
from sqlalchemy.future import Engine, create_engine

from contaxy.operations import JsonDocumentOperations
from contaxy.schema.json_db import JsonDocument
from contaxy.utils.postgres_utils import create_schema
from contaxy.utils.state_utils import GlobalState, RequestState


class PostgresJsonDocumentManager(JsonDocumentOperations):
    def __init__(
        self,
        global_state: GlobalState,
        request_state: RequestState,
    ):
        """Initializes the Postgres Json Document Manager.

        Args:
            global_state: The global state of the app instance.
            request_state: The state for the current request.
        """
        self.global_state = global_state
        self.request_state = request_state
        self._engine = self._create_db_engine()
        self._metadata = MetaData()

    def create_json_document(
        self,
        project_id: str,
        collection_id: str,
        key: str,
        json_document: Dict,
    ) -> JsonDocument:
        """Creates a json document for a given key.

        An upsert strategy is used, i.e. if a document already exists for the given key it will be overwritten. The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            key (str): Json Document Id, i.e. DB row key.
            json_document (Dict): The actual Json document.

        Returns:
            JsonDocument: The created Json document.
        """

        table = self._get_collection_table(project_id, collection_id)

        insert_data = {"key": key, "json_value": json_document}
        insert_data = self._add_metadata_for_insert(insert_data)
        upsert_data = self._add_metadata_for_update(insert_data)

        upsert_statement = (
            postgresql.insert(table)
            .values(**insert_data)
            .on_conflict_do_update(index_elements=["key"], set_=upsert_data)
        )

        with self._engine.begin() as conn:
            result = conn.execute(upsert_statement)
            if result.rowcount == 0:
                raise RuntimeError("Upsert failed")
            conn.commit()

        return self.get_json_document(project_id, collection_id, key)

    def get_json_document(
        self, project_id: str, collection_id: str, key: str
    ) -> JsonDocument:
        """Get a Json document by key.

        The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            key (str): Json Document Id, i.e. DB row key.
            json_document (Dict): The actual Json document.

        Raises:
            ValueError: No document found for the given key.

        Returns:
            JsonDocument: The requested Json document.
        """
        table = self._get_collection_table(project_id, collection_id)
        select_statement = table.select().where(table.c.key == key)
        with self._engine.begin() as conn:
            result = conn.execute(select_statement)
            try:
                row = result.one()
            except NoResultFound:
                raise ValueError(f"No document with key {key} found")
        return self._map_db_row_to_document_model(row)

    def get_json_documents(
        self, project_id: str, collection_id: str, keys: List[str]
    ) -> List[JsonDocument]:
        """Get multiple Json documents by key.

        The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            keys (List[str]): Json Document Ids, i.e. DB row keys.
            json_document (Dict): The actual Json document.

        Returns:
            JsonDocument: The requested Json document.
        """

        table = self._get_collection_table(project_id, collection_id)
        select_statement = table.select().where(table.c.key.in_(keys))
        with self._engine.begin() as conn:
            result = conn.execute(select_statement)
            rows = result.fetchall()
        return self._map_db_rows_to_document_models(rows)

    def update_json_document(
        self,
        project_id: str,
        collection_id: str,
        key: str,
        json_document: dict,
    ) -> JsonDocument:
        """Updates a Json document via Json Merge Patch strategy.

        The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            key (str): Json Document Id, i.e. DB row key.
            json_document (Dict): The actual Json document.

        Raises:
            ValueError: No document found for the given key.

        Returns:
            JsonDocument: The updated document.
        """
        table = self._get_collection_table(project_id, collection_id)

        json_value = json.dumps(json_document)

        update_data = self._add_metadata_for_update({})

        sql_statement = (
            table.update()
            .where(table.c.key == key)
            .values(
                json_value=func.jsonb_merge_patch(table.c.json_value, json_value),
                **update_data,
            )
        )

        with self._engine.begin() as conn:
            result = conn.execute(sql_statement)
            if result.rowcount == 0:
                # This will raise a value error if doc not exists
                self.get_json_document(project_id, collection_id, key)
                raise RuntimeError(
                    f"Document {key} could not be deleted (project_id: {project_id}, collection_id {collection_id})"
                )
            conn.commit()

        return self.get_json_document(project_id, collection_id, key)

    def delete_json_document(
        self, project_id: str, collection_id: str, key: str
    ) -> None:
        """Delete a Json document by key.

        The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            key (str): Json Document Id, i.e. DB row key.
            json_document (Dict): The actual Json document.

        Raises:
            ValueError: No document found for the given key.
        """
        table = self._get_collection_table(project_id, collection_id)
        delete_statement = table.delete().where(table.c.key == key)
        with self._engine.begin() as conn:
            result = conn.execute(delete_statement)
            if result.rowcount == 0:
                # This will raise a value error if doc not exists
                self.get_json_document(project_id, collection_id, key)
                raise RuntimeError(
                    f"Document {key} could not be deleted (project_id: {project_id}, collection_id {collection_id})"
                )
            conn.commit()

    def delete_documents(
        self, project_id: str, collection_id: str, keys: List[str]
    ) -> int:
        """Delete Json documents by key.

        The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            keys (List[str]): Json Document Ids, i.e. DB row keys.
            json_document (Dict): The actual Json document.

        """
        table = self._get_collection_table(project_id, collection_id)
        delete_statement = table.delete().where(table.c.key.in_(keys))
        with self._engine.begin() as conn:
            result = conn.execute(delete_statement)
            conn.commit()
        return result.rowcount

    def list_json_documents(
        self,
        project_id: str,
        collection_id: str,
        filter: Optional[str] = None,
    ) -> List[JsonDocument]:
        """List all existing Json documents and optionally filter via Json Path syntax.

            The project is equivalent to the DB schema and the collection to a DB table inside the respective DB schema. Schema as well as table will be lazily created.

        Args:
            project_id (str): Project Id, i.e. DB schema.
            collection_id (str): Json document collection Id, i.e. DB table.
            filter (Optional[str], optional): Json Path filter. Defaults to None.

        Raises:
            ValueError: If filter is provided and does not contain a valid Json Path filter.

        Returns:
            List[JsonDocument]: List of Json documents.
        """
        table = self._get_collection_table(project_id, collection_id)
        sql_statement = table.select()
        if filter:
            sql_statement = sql_statement.where(
                func.jsonb_path_exists(table.c.json_value, filter),
            )
            print(sql_statement)

        with self._engine.begin() as conn:
            try:
                result = conn.execute(sql_statement)
            except ProgrammingError:
                raise ValueError("Please provide a valid Json Path filter.")

            rows = result.fetchall()
        return self._map_db_rows_to_document_models(rows)

    def _add_metadata_for_insert(self, data: dict) -> dict:
        insert_data = data.copy()
        # TODO: Finalize
        insert_data["created_at"] = datetime.datetime.utcnow()
        # data["created_by"] =
        return insert_data

    def _add_metadata_for_update(self, data: dict) -> dict:
        update_data = data.copy()
        # TODO: Finalize
        update_data["updated_at"] = datetime.datetime.utcnow()
        # data["updated_by"] =
        return update_data

    def _map_db_rows_to_document_models(self, rows: List[Row]) -> List[JsonDocument]:
        docs = []
        for row in rows:
            docs.append(self._map_db_row_to_document_model(row))
        return docs

    def _map_db_row_to_document_model(self, row: Row) -> JsonDocument:
        data = {}
        for column_name, value in row._mapping.items():
            if isinstance(value, dict):
                data.update({column_name: json.dumps(value)})
                continue
            data.update({column_name: value})
        return JsonDocument(**data)

    def _get_collection_table(self, project_id: str, collection_id: str) -> Table:
        # TODO: Decide on actual column datatypes
        collection = Table(
            collection_id,
            self._metadata,
            Column("key", postgresql.VARCHAR, primary_key=True),
            Column("json_value", postgresql.JSONB),
            Column("created_at", DateTime),
            Column("created_by", postgresql.VARCHAR),
            Column("updated_at", DateTime),
            Column("updated_by", postgresql.VARCHAR),
            schema=project_id,  # TODO: Check if sufficient if we set on metadata object
            keep_existing=True,  # TODO: Depends on how we handle schema modifications
        )

        try:
            collection.create(self._engine, checkfirst=True)
        except ProgrammingError as err:
            if err.code != "f405":
                raise err
            create_schema(self._engine, project_id)
            collection.create(self._engine, checkfirst=True)

        return collection

    def _create_db_engine(self) -> Engine:
        state_namespace = self.request_state[PostgresJsonDocumentManager]
        if not state_namespace.db_engine:
            url = self.global_state.settings.POSTGRES_CONNECTION_URI
            engine = create_engine(url, future=True)
            # Test the DB connection and set to global state if succesful
            with engine.begin():
                state_namespace.db_engine = engine
        return state_namespace.db_engine
