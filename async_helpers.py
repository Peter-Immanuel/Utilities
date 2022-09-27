import asyncio
import aiohttp
import backoff
from pprint import pprint
from typing import Callable


class AsyncOperations:
    """A class of asynchronous operations
    """

    # a semaphore for limiting the number of requests that can be made at once
    manage_requests = asyncio.BoundedSemaphore(30)

    def __init__(self, instance_url: str, username: str, password: str) -> None:
        self.url = instance_url
        self.username = username
        self.password = password

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60, max_tries=7)
    async def get_org_unit_via_parent(self, session, parent_id: str):
        """Get all the children from the organisation unit supplied

        Args:
            session (_type_): aiohttp session
            parent_id (str): the parent organization unit ID

        Returns:
            list: the JSON response containing the children of the parent organisation unit ID
        """
        # make an async request and await the JSON response
        async with self.manage_requests, session.get(
            self.url
            + f"/api/metadata?organisationUnits:filter=parent.id:eq:{parent_id}",
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as resp:
            awaited_response = await resp.json()

        # return the the child data if it exists
        try:
            child_data = awaited_response["organisationUnits"]
        except KeyError:
            child_data = None

        return child_data

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60, max_tries=7)
    async def make_async_post_requests(self, session, payload):
        """Make asynchronous post requests

        Args:
            session (_type_): async session object
            payload (_type_): JSON payload

        Returns:
            _type_: JSON response
        """

        async with self.manage_requests, session.post(
            self.url, auth=aiohttp.BasicAuth(self.username, self.password), json=payload
        ) as resp:
            awaited_response = await resp.json()
        return awaited_response

    async def check_obj_dict(
        self, session, entity: dict, entity_item: str, replacement_dict: dict
    ):
        """Check if an entity exists from a response body

        Args:
            session (_type_): async session object
            entity (dict): entity in a JSON response
            entity_item (str): entity item/specific object in the JSON response 
            replacement_dict (dict): dictionary to replace the entity item with if it doesn't exist

        Returns:
            dict: cleaned dictionary/ JSON entity 
        """
        item = entity[entity_item]["id"]

        async with self.manage_requests, session.get(
            f"{self.url}/api/identifiableObjects/{item}",
            auth=aiohttp.BasicAuth(self.username, self.password,),
        ) as resp:
            await_response = await resp.json()
            await_response_status = resp.status

        if await_response_status == 200:
            return entity

        elif await_response_status == 404:
            entity[entity_item] = replacement_dict
            return entity

    async def check_obj_list(self, session, entity: dict, entity_item: str):
        """Check if the entity exists in a response body

        Checks if an entity, such as an ID, exists within an instance, expects
        the entity to be a list with one entry

        Args:
            session (_type_): async session object
            entity (dict): the response object body
            entity_item (str): the name of the entity item being checked

        Returns:
            dict: response body
        """

        item = entity[entity_item]

        # if the list is not empty
        if item:
            # grab the first item, then the value of ID and check if it exists
            first_item = item[0]["id"]

            async with self.manage_requests, session.get(
                f"{self.url}/api/identifiableObjects/{first_item}",
                auth=aiohttp.BasicAuth(self.username, self.password,),
            ) as resp:
                await_response = await resp.json()
                await_response_status = resp.status

            if await_response_status == 200:
                return entity

            elif await_response_status == 404:
                entity[entity_item] = []
                return entity
        else:
            return entity

    async def gather_get_tasks(self, async_op, entities, *args):
        """An asynchronous coroutine manager

        This coroutine manages other coroutines

        Args:
            async_op (_type_): an asynchronous operation
            entities (list): JSON response/ list of JSON objects

        Returns:
            list: JSON like object
        """
        async with aiohttp.ClientSession() as open_session:
            tasks = [async_op(open_session, entity, *args) for entity in entities]
            results = await asyncio.gather(*tasks)
        return results
