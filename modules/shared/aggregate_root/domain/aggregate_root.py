from typing import List
from typing import NoReturn
from modules.shared.bus.event.domain import DomainEvent


class AggregateRoot:

    domain_events = []

    def pull_domain_events(self) -> List[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []
        return domain_events

    def record(self, domain_event: DomainEvent) -> NoReturn:
        self.domain_events.append(domain_event)
