from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Query, Depends
from sqlalchemy.future import select

from app.dependencies import get_db
from app.models.debt import Debt

router = APIRouter()


@router.get('/debts')
async def process_debts(file_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    current_date = date.today()

    async with db as session:
        query = select(Debt).where(Debt.file_upload_id == file_id, Debt.debt_due_date < current_date)
        result = await session.execute(query)
        debts = result.scalars().all()

        if not debts:
            return {'count': 0, 'debts': []}

        debts_data = [debt.to_dict() for debt in debts]

        # Send an email for each overdue debt
        # I wanted to create one service to do this, but i didnt have enough time, so im just 'mocking here as pseudocode'
        # and just returning the total amount of overdue_debts on the database, based on the file_id send
        for debt in debts_data:
            debt_due_date = datetime.strptime(debt['debt_due_date'], '%Y-%m-%d').date()
            days_of_delay = (current_date - debt_due_date).days

            await send_email(debt['email'], debt['name'], days_of_delay, debt['government_id'])

        return {'total_sent_emails': len(debts_data)}

async def send_email(recipient_email, recipient_name, days_of_delay, government_id):

    # Using a dict containing the name of the creditor of the debt, on a NoSql database, like mongo
    # government_name =  mgdb.government_id.find_one({'_id': government_id})['name']
    # message = f'Olá {recipient_name}, pague hoje mesmo sua dívida com {government_name} vencida a mais de {days_of_delay}.'

    # await aiosmtplib.send(message, recipient_email,hostname="smtp.example.com", port=587)
    pass
