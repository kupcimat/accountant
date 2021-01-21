# Accountant

Accountant is a fictional application for extracting structured data from bank account statements in PDF. It showcases simple distributed app design and implementation on AWS.

## Architecture Overview

![overview](docs/accountant-overview.png)

Application is split into two components:
* **REST API** - public facing web application, serving clients and generating S3 links
* **Worker** - application processing async tasks, extracting data from PDF documents

Both components are stateless, which allows them to be easily scalable based on demand. REST API runs a simple Python web server with JSON API. It generates presigned S3 links to upload documents and download results. It checks S3 for the results, but never blocks. The actual document parsing is done by worker instances, which run on demand based on number of messages in the SQS queue. The queue is notified about new tasks automatically, everytime a user uploads new document.

## Document Lifecycle

![sequence](docs/accountant-sequence.png)

Each document is tracked using UUID, which is generated when the user requests upload URL. After that it's used to check the result. All documents and results are available on S3, which is used as primary storage. Users comunicate directly with S3 using generated presigned links. This way we don't need any other shared storage for components which makes simpler deployment.

## API

#### GET /
```json
200 OK
{
  "root": {
    "links": {
      "upload": "/api/documents"
    }
  }
}
```

#### POST /api/documents
```json
201 Created
{
  "documentUpload": {
    "uploadUrl": "presigned-upload-url",
    "uploadHeaders": {
      "x-amz-meta-documentType": "document:kb:pdf"
    },
    "uploadCurl": "curl -X PUT -H 'x-amz-meta-documentType: document:kb:pdf' --upload-file filename <presigned-upload-url>",
    "links": {
      "result": "/api/documents/<document-id>"
    }
  }
}
```

#### GET /api/documents/document-id
```json
404 Not Found (Document not found)

202 Accepted  (Result is not ready)

200 OK        (Result is ready)
{
  "documentResult": {
    "resultUrl": "<presigned-result-url>",
    "resultCurl": "curl <presigned-result-url>",
    "links": {
      "result": "/api/documents/<document-id>"
    }
  }
}
```
