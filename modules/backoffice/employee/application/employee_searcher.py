from modules.backoffice.employee.domain import EmployeeRepository


class EmployeeSearcher:
    """
    Class to get search Employees
    """

    def __init__(self, employee_repository: EmployeeRepository):
        """
        Args:
            employee_repository: repository for employee database table operations
        """

        self.__employee_repository = employee_repository

    async def search(self, query_params: dict):
        """
        Args:
            query_params (dict): query params.
        Returns:
            dict: paginated employees.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)
        export = query_params.pop("export", False)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}

        employee_results = await self.__employee_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
            list_all=export,
        )

        return employee_results
