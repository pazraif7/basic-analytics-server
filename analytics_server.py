import sqlite3
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Request
import uvicorn

app = FastAPI()

def init_db() -> None:
    connection = sqlite3.connect('/app/analytics.db')
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

init_db()

@app.post("/process_event")
async def process_event_endpoint(request: Request):

    try:
        body = await request.json()
        userid = body.get("userid")
        eventname = body.get("eventname")

        if not userid or not eventname:
            raise HTTPException(status_code=400, detail="Both userid and eventname are required.")

        event_timestamp: str = datetime.now(timezone.utc).isoformat()

        connection = sqlite3.connect('/app/analytics.db')
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

@app.post("/get_reports")
async def get_reports(request: Request):
    try:
        body = await request.json()
        lastseconds = body.get("lastseconds")
        userid = body.get("userid")

        if not lastseconds or not userid:
            raise HTTPException(status_code=400, detail="Both lastseconds and userid are required.")

        try:
            lastseconds = int(lastseconds)
        except ValueError:
            raise HTTPException(status_code=400, detail="lastseconds must be an integer.")

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(seconds=lastseconds)

        connection = sqlite3.connect('/app/analytics.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT eventtimestamputc, userid, eventname FROM events 
            WHERE userid = ? AND eventtimestamputc >= ?
        ''', (userid, cutoff_time.isoformat()))
        rows = cursor.fetchall()
        connection.close()

        events = [
            {"eventtimestamputc": row[0], "userid": row[1], "eventname": row[2]} for row in rows
        ]

        return {"events": events}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)