import time
import uuid
import logging
import boto3
from fastapi import APIRouter, FastAPI,File, UploadFile, Request, Response
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from mangum import Mangum
from PIL import Image, ExifTags
from typing import Callable


logger = logging.getLogger()
logger.setLevel(logging.INFO)
       
class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            response = await original_route_handler(request)
            return response.Items          
        return custom_route_handler

app = FastAPI(debug=True)
handler = Mangum(app)
router = APIRouter(route_class=LoggingRoute)


''' create html page to show uploaded file '''
@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>Upload File</title>
        </head>
        <body>
            <h1>Upload Your Image(JPG/PNG file)</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


''' upload image, save IP and created time in dynamodb, rreturneceive a JSON array of metadata.
Persisst a log of all POST requests with timestamps and IP address in a database '''  
@app.post("/")
async def post_image(request: Request, file: UploadFile = File(...)):    
    if not file:
        return {"message": "No upload file sent"}
    if file.content_type != "image/jpeg":
        return {"message": "Please Upload only image file"}
       
    #Extract image info , metadata using PIL module
    image = Image.open(file.file)
    exifdata = image.getexif()
    image_metadata= {ExifTags.TAGS.get(tagid, tagid):exifdata.get(tagid) for tagid in exifdata}  

    #create new item 
    item = {
        "user_IP": request.client.host,
        "created_time":int(time.time()),
        "id": f"{uuid.uuid4()}.jpg"
    }

    # Put the item into the table in dynamodb.
    table = _get_table()
    table.put_item(Item=item)  

    #get timestamps and IP address in the dynamoDB
    response = table.scan(
        IndexName='user_IP',
        ProjectionExpression='created_time,user_IP'
        )
    logger.info(response.get("Items"))   
    return {"dimension": image.size, "format": image.format, "mode": image.mode, "metadata": image_metadata}


''' shows all POST requests with timestamps and IP address in a database. '''  
@app.get("/list_IPs")
async def list_IPs():
    # List IPs and created time from the table, using the user IP.
    table = _get_table()
    response = table.scan(
        IndexName='user_IP',
        ProjectionExpression='created_time,user_IP'
        )
    Items = response.get("Items")
    logger.info(Items)
    return {"Log File": Items}
app.include_router(router)

def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)