"""Stream type classes for tap-clickup."""
from pathlib import Path
from singer_sdk.helpers.jsonpath import extract_jsonpath
from typing import Optional, Iterable
from tap_clickup.client import ClickUpStream
import requests

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TeamsStream(ClickUpStream):
    """Teams"""

    name = "team"
    path = "/team"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "team.json"
    records_jsonpath = "$.teams[*]"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "team_id": record["id"],
        }


class SpacesStream(ClickUpStream):
    """Spaces"""

    name = "space"
    path = "/team/{team_id}/space"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "space.json"
    records_jsonpath = "$.spaces[*]"
    parent_stream_type = TeamsStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "space_id": record["id"],
        }


class FoldersStream(ClickUpStream):
    """Folders"""

    name = "folder"
    path = "/space/{space_id}/folder"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "folder.json"
    records_jsonpath = "$.folders[*]"
    parent_stream_type = SpacesStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "folder_id": record["id"],
        }


class FolderListsStream(ClickUpStream):
    """Lists"""

    name = "folder_list"
    path = "/folder/{folder_id}/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "list.json"
    records_jsonpath = "$.lists[*]"
    parent_stream_type = FoldersStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class FolderlessListsStream(ClickUpStream):
    """Folderless Lists"""

    name = "folderless_list"
    path = "/space/{space_id}/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "list.json"
    records_jsonpath = "$.lists[*]"
    parent_stream_type = SpacesStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class ListsStream(ClickUpStream):
    """Lists"""

    name = "list"
    path = "/folder/{folder_id}/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "list.json"
    records_jsonpath = "$.lists[*]"
    parent_stream_type = FoldersStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class TaskTemplatesStream(ClickUpStream):
    """TaskTemplates"""

    name = "task_template"
    path = "/team/{team_id}/task_template?page=0"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "task_template.json"
    records_jsonpath = "$.templates[*]"
    parent_stream_type = TeamsStream


class GoalsStream(ClickUpStream):
    """Goals"""

    name = "goal"
    path = "/team/{team_id}/goal"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "goal.json"
    records_jsonpath = "$.goals[*]"
    parent_stream_type = TeamsStream


class TagsStream(ClickUpStream):
    """Tags"""

    name = "tag"
    path = "/space/{space_id}/tag"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "tag.json"
    records_jsonpath = "$.tags[*]"
    parent_stream_type = SpacesStream


class SharedHierarchyStream(ClickUpStream):
    """SharedHierarchy"""

    name = "shared_hierarchy"
    path = "/team/{team_id}/shared"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "shared.json"
    records_jsonpath = "$.shared"
    parent_stream_type = TeamsStream


class FolderlessTasksStream(ClickUpStream):
    """Tasks can come from lists not under folders"""

    name = "folderless_task"
    path = "/list/{list_id}/task"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "task.json"
    records_jsonpath = "$.tasks[*]"
    parent_stream_type = FolderlessListsStream
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        response.json()
        #for record in extract_jsonpath
        # increase record count
        # if record count == 100 set page = pagesize++
        # if record count == 0 set nextpage = null 
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())


class FolderTasksStream(ClickUpStream):
    """Tasks can come from under Folders"""

    name = "folder_task"
    path = "/list/{list_id}/task"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "task.json"
    records_jsonpath = "$.tasks[*]"
    parent_stream_type = FolderListsStream


class CustomFieldsStream(ClickUpStream):
    """CustomField"""

    name = "custom_field"
    path = "/list/{list_id}/field"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "custom_field.json"
    records_jsonpath = "$.fields[*]"
    parent_stream_type = FolderlessListsStream
