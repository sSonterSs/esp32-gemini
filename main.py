import io
import os
from fastapi import FastAPI, Request, Response
from google import genai
from PIL import Image

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/upload")
async def upload(request: Request):
    try:
        image_bytes = await request.body()
        if not image_bytes:
            return Response(content="Нет данных", status_code=400)

        img = Image.open(io.BytesIO(image_bytes))

        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=[img, "Коротко опиши, что на этом фото"]
        )
        return Response(content=response.text, status_code=200)

    except Exception as e:
        return Response(content=str(e), status_code=500)
