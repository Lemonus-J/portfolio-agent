from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError, AzureError
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

credential = DefaultAzureCredential()
service = BlobServiceClient(account_url="https://hwmportfoliostorage.blob.core.windows.net/", credential=credential)


@app.get("/profile")
async def read_profile():
    try:
        blob_client = service.get_blob_client(container="portfolio-data", blob="profile.json")
        data = blob_client.download_blob().readall()
        return json.loads(data)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Blob or container not found: {str(e)}")

    except ClientAuthenticationError as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

    except AzureError as e:
        raise HTTPException(status_code=500, detail=f"Azure error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")