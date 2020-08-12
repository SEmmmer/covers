json = {
    "error": {
        "code": 400,
        "message": "The request specifies an invalid page token.",
        "errors": [
            {
                "message": "The request specifies an invalid page token.",
                "domain": "youtube.parameter",
                "reason": "invalidPageToken",
                "location": "pageToken",
                "locationType": "parameter"
            }
        ]
    }
}

if __name__ == "__main__":
    print(json["error"])
