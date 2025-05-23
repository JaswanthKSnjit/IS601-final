from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from datetime import datetime, timezone, timedelta
from app.models.user_model import User, RetentionAnalytics
from uuid import UUID


class AnalyticsService:
    @staticmethod
    async def log_user_activity(user_id: UUID, db: AsyncSession):
        """Update the last login timestamp for a user."""
        user = await db.get(User, user_id)
        if user:
            now = datetime.now(timezone.utc)
            user.last_login_at = now
            db.add(user)
            await db.commit()

    @staticmethod
    async def get_retention_data(db: AsyncSession):
        """Retrieve the most recent retention analytics data."""
        result = await db.execute(
            select(RetentionAnalytics).order_by(RetentionAnalytics.timestamp.desc())
        )
        retention_records = await result.scalars().all()  # Await the coroutine

        # Convert RetentionAnalytics objects to dictionaries
        return [
            {
                "timestamp": record.timestamp.isoformat(),
                "total_anonymous_users": record.total_anonymous_users,
                "total_authenticated_users": record.total_authenticated_users,
                "conversion_rate": record.conversion_rate,
                "inactive_users_24hr": record.inactive_users_24hr,
            }
            for record in retention_records
        ]

        


    @staticmethod
    async def calculate_retention_metrics(db: AsyncSession):
        """Calculate retention metrics and save them into the database."""
        now = datetime.now(timezone.utc)

        # Count total anonymous and authenticated users
        total_anonymous = await db.scalar(select(func.count()).where(User.role == "ANONYMOUS"))
        total_authenticated = await db.scalar(select(func.count()).where(User.role == "AUTHENTICATED"))

        # Calculate conversion rate
        conversion_rate = (
            f"{(total_authenticated / (total_anonymous + total_authenticated) * 100):.2f}%"
            if (total_anonymous + total_authenticated) > 0
            else "0%"
        )

        # Identify inactive users based on last login time
        inactive_24hr = await db.scalar(
            select(func.count()).where(User.last_login_at < now - timedelta(hours=24))
        )

        # Construct and save analytics metrics
        analytics = RetentionAnalytics(
            total_anonymous_users=total_anonymous or 0,
            total_authenticated_users=total_authenticated or 0,
            conversion_rate=conversion_rate,
            inactive_users_24hr=inactive_24hr or 0,
        )

        db.add(analytics)
        await db.commit()


