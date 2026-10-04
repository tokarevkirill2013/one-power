from fastapi import FastAPI

from starlette.responses import HTMLResponse

app = FastAPI()
HTMLc = '''<html>
 <head>
  <title>FastAPIApp
   </title>
    </head>
     <boby>
      <h1>грузись </h1>
        <boby>
         </html> '''
@app.get('/',response_class=HTMLc)

async def read_root():
    return HTMLc

