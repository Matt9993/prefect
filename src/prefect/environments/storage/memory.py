from typing import Any, Dict, Iterable, List

import prefect
from prefect.environments.storage import Storage


class Memory(Storage):
    """
    Base class for Storage objects.
    """

    def __init__(self) -> None:
        self.flows = dict()  # type: Dict[str, prefect.core.flow.Flow]
        super().__init__()

    def get_runner(self, flow_location: str, return_flow: bool = True) -> Any:
        """
        Given a flow name, returns the flow.

        Args:
            - flow_location (str): the name of the flow
            - return_flow (bool, optional): whether to return the full Flow object
                or a `FlowRunner`; defaults to `True`

        Returns:
            - Flow: the requested Flow
        """
        if not flow_location in self.flows:
            raise ValueError("Flow is not contained in this Storage")
        if return_flow:
            return self.flows[flow_location]
        else:
            runner_cls = prefect.engine.get_default_flow_runner_class()
            return runner_cls(flow=self.flows[flow_location])

    def add_flow(self, flow: "prefect.core.flow.Flow") -> str:
        """
        Method for adding a new flow to this Storage object.

        Args:
            - flow (Flow): a Prefect Flow to add

        Returns:
            - str: the location of the newly added flow in this Storage object
        """
        if flow in self:
            raise ValueError(
                'Name conflict: Flow with the name "{}" is already present in this storage.'.format(
                    flow.name
                )
            )
        self.flows[flow.name] = flow
        return flow.name

    def __contains__(self, obj: Any) -> bool:
        """
        Method for determining whether an object is contained within this storage.
        """
        if not isinstance(obj, prefect.core.flow.Flow):
            return False
        return obj.name in self.flows

    def get_flow_location(self, flow: "prefect.core.flow.Flow") -> str:
        """
        Given a flow, retrieves its location within this Storage object.

        Args:
            - flow (Flow): a Prefect Flow contained within this Storage

        Returns:
            - str: the location of the Flow

        Raises:
            - ValueError: if the provided Flow does not live in this Storage object
        """
        if not flow in self:
            raise ValueError("Flow is not contained in this Storage")

        return [loc for loc, f in self.flows.items() if f.name == flow.name].pop()

    def build(self) -> "Storage":
        """
        Build the Storage object.

        Returns:
            - Storage: a Storage object that contains information about how and where
                each flow is stored
        """
        return self
