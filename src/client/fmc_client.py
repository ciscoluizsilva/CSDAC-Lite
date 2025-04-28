from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Optional, Callable, Dict

import requests
import urllib3
from requests.auth import HTTPBasicAuth

from .dynamic_objects import DynamicObjects


def handle_rate_limit(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        max_retries = 3  # Define a maximum number of retries to prevent infinite loops
        retry_count = 0

        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    # Extract retry delay from headers or set a default delay
                    retry_after = e.response.headers.get("Retry-After", 30)
                    time.sleep(int(retry_after))
                    retry_count += 1
                else:
                    raise  # Re-raise the exception if it's not a 429
        raise Exception("Max retries exceeded for 429 error.")

    return wrapper


@dataclass
class FMCClient:
    session: requests.Session
    host: str
    port: int
    auth: HTTPBasicAuth
    domain_name: Optional[str] = field(default="Global")
    verify_cert: bool = field(default=False)
    current_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_timeout: int = 0
    refresh_count: int = 0
    dynamic_objects: DynamicObjects = field(init=False)
    domain_uuid: Optional[str] = None

    def __post_init__(self) -> None:
        self.dynamic_objects = DynamicObjects(self)

    @classmethod
    def from_credentials(
        cls,
        host: str,
        port: int,
        username: str,
        password: str,
        domain_name: Optional[str] = None,  # Domain name
        verify_cert: bool = False,
    ) -> FMCClient:
        """
        Create a new FMC client from credentials
        :param host:
        :param port:
        :param username:
        :param password:
        :param domain_name: DOMAIN NAME, default = Global
        :param verify_cert:
        :return:
        """
        session = requests.Session()
        auth = HTTPBasicAuth(username, password)
        client = cls(session, host, port, auth, domain_name, verify_cert)
        client.authenticate()
        return client

    def generate_url(self, target: str) -> str:
        base_url = f"https://{self.host}:{self.port}/api/"
        return f"{base_url}{target}"

    def generate_header(self) -> dict[str, Any]:
        """
        Generate the header for the request
        :return: dict
        """
        return {"X-auth-access-token": self.current_token}

    @handle_rate_limit
    def authenticate(self) -> None:
        """
        Authenticate the client with the FMC
        :return:
        """
        if self.verify_cert is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        target = self.generate_url("fmc_platform/v1/auth/generatetoken")
        response = self.session.post(
            target, auth=self.auth, data="", verify=self.verify_cert
        )
        response.raise_for_status()
        domains = json.loads(response.headers["DOMAINS"])
        for domain in domains:
            if domain["name"] == self.domain_name:
                self.domain_uuid = domain["uuid"]
                break
        if self.domain_uuid is None:
            raise Exception(f"Domain {self.domain_name} not found")

        self.current_token = response.headers["X-auth-access-token"]
        self.refresh_token = response.headers["X-auth-refresh-token"]
        self.token_timeout = int(time.time()) + 1800

    @handle_rate_limit
    def token_refresh(self) -> None:
        """
        Refresh the token
        :return:
        """
        if self.token_timeout > int(time.time()):
            return
        if self.refresh_count >= 3:
            self.authenticate()
            return
        target = self.generate_url("fmc_platform/v1/auth/refreshtoken")
        headers = {"X-auth-refresh-token": self.refresh_token}
        response = self.session.post(target, headers=headers, verify=self.verify_cert)
        response.raise_for_status()
        self.current_token = response.headers["X-auth-access-token"]
        self.refresh_token = response.headers["X-auth-refresh-token"]
        self.token_timeout = int(time.time()) + 1800
        self.refresh_count += 1

    @handle_rate_limit
    def get(self, target_url: str) -> Any:
        """
        GET request
        :return:
        """
        self.token_refresh()
        response = self.session.get(
            target_url, headers=self.generate_header(), verify=self.verify_cert
        )
        response.raise_for_status()

        json_response = response.json()
        # Handle pagination
        if "paging" in json_response:
            if "next" in json_response["paging"]:
                new_response = self.get(json_response["paging"]["next"][0])
                json_response["items"].extend(new_response["items"])
        json_response.pop("paging", None)
        return json_response

    @handle_rate_limit
    def post(self, target_url: str, data: Dict[str, Any]) -> Any:
        """
        POST request
        :return:
        """
        self.token_refresh()
        response = self.session.post(
            target_url,
            headers=self.generate_header(),
            json=data,
            verify=self.verify_cert,
        )
        response.raise_for_status()
        return response.json()

    @handle_rate_limit
    def put(self, target_url: str, data: Dict[str, Any]) -> Any:
        """
        PUT request
        :return:
        """
        self.token_refresh()
        response = self.session.put(
            target_url,
            headers=self.generate_header(),
            json=data,
            verify=self.verify_cert,
        )
        response.raise_for_status()
        return response.json()

    @handle_rate_limit
    def delete(self, target_url: str) -> Any:
        """
        DELETE request
        :return:
        """
        self.token_refresh()
        response = self.session.delete(
            target_url, headers=self.generate_header(), verify=self.verify_cert
        )
        response.raise_for_status()
        return response.json()
