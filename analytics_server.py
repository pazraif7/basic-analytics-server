import sqlite3
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
import uvicorn

app = FastAPI()

def init_db() -> None:
    connection = sqlite3.connect('analytics.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            eventtimestamputc TEXT NOT NULL,
            userid TEXT NOT NULL,
            eventname TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


@app.post("/process_event")
async def process_event_endpoint(request: Request):

    try:
        body = await request.json()
        userid = body.get("userid")
        eventname = body.get("eventname")

        if not userid or not eventname:
            raise HTTPException(status_code=400, detail="Both userid and eventname are required.")

        event_timestamp: str = datetime.now(timezone.utc).isoformat()

        connection = sqlite3.connect('analytics.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO events (eventtimestamputc, userid, eventname)
            VALUES (?, ?, ?)
        ''', (event_timestamp, userid, eventname))
        connection.commit()
        connection.close()

        return {"message": "Event processed successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)