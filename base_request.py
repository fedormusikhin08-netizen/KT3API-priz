import os
import time

import requests


class BaseRequest:
    base_url = os.environ.get("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "api_key": "special-key",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

    def request(self, method, path, body=None, expected_error=False):
        url = f"{self.base_url}/{path}"
        response = None
        for _ in range(3):
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=15)
            elif method == "POST":
                response = requests.post(url, json=body, headers=self.headers, timeout=15)
            elif method == "PUT":
                response = requests.put(url, json=body, headers=self.headers, timeout=15)
            else:
                response = requests.delete(url, headers=self.headers, timeout=15)

            if expected_error or response.status_code == 200:
                break
            time.sleep(1)

        print(method, url, response.status_code)
        return response

    def get(self, path, expected_error=False):
        return self.request("GET", path, expected_error=expected_error)

    def post(self, path, body):
        return self.request("POST", path, body)

    def put(self, path, body):
        return self.request("PUT", path, body)

    def delete(self, path):
        return self.request("DELETE", path)


api = BaseRequest()
