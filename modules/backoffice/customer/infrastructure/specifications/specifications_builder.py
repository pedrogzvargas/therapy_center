from modules.backoffice.customer.infrastructure.specifications.alchemy import NameSpecification
from modules.backoffice.customer.infrastructure.specifications.alchemy import LastNameSpecification


SPECIFICATIONS = dict(
        name=NameSpecification,
        last_name=LastNameSpecification,
    )


class SpecificationsBuilder:

    @staticmethod
    def build(query_params: dict):
        if not isinstance(query_params, dict):
            raise ValueError(f"Query params {query_params} is not instance of dict")

        query_params = {key: value for key, value in query_params.items() if value is not None}
        specifications = []
        for key, value in query_params.items():
            specification = SPECIFICATIONS.get(f"{key}")
            if specification:
                specifications.append(specification(value))

        return specifications
