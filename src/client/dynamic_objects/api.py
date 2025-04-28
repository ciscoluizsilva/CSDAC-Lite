from dataclasses import dataclass
from typing import Any, List

from .models import (
    DynamicMappingCollection,
    DynamicObject,
    DynamicObjectCollection,
    NewDynamicObject,
)


@dataclass
class DynamicObjects:
    client: Any

    def create(self, new_dynamic_object: NewDynamicObject) -> DynamicObject:
        """
        Create a new dynamic object
        :param new_dynamic_object: New dynamic object
        :return: DynamicObject
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects"
        )
        response = self.client.post(target, new_dynamic_object.__dict__)
        return DynamicObject(**response)

    def delete(self, dynamic_object_id: str) -> None:
        """
        Delete a dynamic object
        :param dynamic_object_id: Dynamic object ID
        :return:
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}"
        )
        self.client.delete(target)

    def get_all(self) -> DynamicObjectCollection:
        """
        Get all dynamic objects
        :return: DynamicObjects
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects?limit=1000"
        )
        response = self.client.get(target)
        return DynamicObjectCollection(**response)

    def get(self, dynamic_object_id: str) -> DynamicObject:
        """
        Get a dynamic object
        :param dynamic_object_id: Dynamic object ID
        :return: DynamicObject
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}"
        )
        response = self.client.get(target)
        return DynamicObject(**response)

    def add_mapping(
        self, ip: List[str], dynamic_object_id: str
    ) -> DynamicMappingCollection:
        """
        Add a mapping to a dynamic object
        :param ip: IP address
        :param dynamic_object_id: Dynamic object ID
        :return: DynamicMapping
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}/mappings?action=add"
        )
        response = self.client.put(
            target,
            {"mappings": ip, "type": "DynamicObjectMappings", "id": dynamic_object_id},
        )
        return DynamicMappingCollection(**response)

    def remove_mapping(
        self, ip: List[str], dynamic_object_id: str
    ) -> DynamicMappingCollection:
        """
        Add a mapping to a dynamic object
        :param ip: IP address
        :param dynamic_object_id: Dynamic object ID
        :return: DynamicMapping
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}/mappings?action=remove"
        )
        response = self.client.put(
            target,
            {"mappings": ip, "type": "DynamicObjectMappings", "id": dynamic_object_id},
        )
        return DynamicMappingCollection(**response)

    def remove_all_mappings(self, dynamic_object_id: str) -> DynamicMappingCollection:
        """
        Add a mapping to a dynamic object
        :param dynamic_object_id: Dynamic object ID
        :return: DynamicMapping
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}/mappings?action=remove_all"
        )
        response = self.client.put(
            target, {"type": "DynamicObjectMappings", "id": dynamic_object_id}
        )
        return DynamicMappingCollection(**response)

    def get_mappings(self, dynamic_object_id: str) -> DynamicMappingCollection:
        """
        Get all mappings of a dynamic object
        :param dynamic_object_id: Dynamic object ID
        :return: DynamicObjectCollection
        """
        target = self.client.generate_url(
            f"fmc_config/v1/domain/{self.client.domain_uuid}/object/dynamicobjects/{dynamic_object_id}/mappings"
        )
        response = self.client.get(target)
        return DynamicMappingCollection(**response)
