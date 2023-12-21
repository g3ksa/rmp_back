from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import os
import requests
from dotenv import load_dotenv
import json

json_file_path = "test.json"

load_dotenv()
app = FastAPI()


@app.post("/uploadfile/")
async def upload_file(image: UploadFile):
    print("image")
    try:
        image_bytes = await image.read()
        recognition_url = "https://api.logmeal.es/v2/image/segmentation/complete/v1.0"
        files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
        headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}
        recognition = requests.post(recognition_url, files=files, headers=headers)
        image_id = recognition.json()["imageId"]

        recipe_url = "https://api.logmeal.es/v2/nutrition/recipe/ingredients/v1.0"
        recipe_response = requests.post(
            recipe_url, headers=headers, json={"imageId": image_id}
        )

        # with open(json_file_path, "r") as file:
        #     data = json.load(file)

        ingredients = recipe_response.json()["recipe"]

        str_recipe = ""
        for idx, value in enumerate(ingredients):
            str_recipe += f'{idx+1}: {value["name"]} {value["weight"]}{value["unit"]}\n'

        return JSONResponse(content={"result": str_recipe}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
