from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.backoffice.user.domain import UserRepository
from modules.backoffice.user.domain import User
from sqlalchemy_models import UserModel
from .user_mapper import UserMapper


class PostgresUserRepository(UserRepository):
    """
    PostgresUserRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, user):
        """add user to session"""
        self.__session.add(UserMapper.to_model(user))
        await self.__session.flush()

    def all(self):
        """list all users"""

        result = self.__session.query(User).all()
        return result

    async def get(self, id: UUID):
        """get user"""

        user = await self.__session.get(UserModel, id)

        if user:
            return UserMapper.to_domain(user)

        return user

    async def delete(self, id: UUID):
        """delete user"""

        user = await self.__session.get(UserModel, id)

        if user:
            await self.__session.delete(user)
            await self.__session.flush()

    def soft_delete(self, user):
        """soft delete user"""

        if not hasattr(user, "is_active"):
            raise ValueError("User model has not 'is_active' attribute")

        user.is_active = False

        self.add(user)
