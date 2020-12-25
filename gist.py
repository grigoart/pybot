import requests


class GistApi:
    def __init__(self, token):
        self.auth = 'token ' + token

    def create(self, files, description):
        return requests.post("https://api.github.com/gists", json={
            'files': files,
            'description': description
        }, headers={
            'Authorization': self.auth,
            'Accept': 'application/vnd.github.v3+json'
        })

    def list(self):
        return requests.get("https://api.github.com/gists?per_page=100", headers={
            'Authorization': self.auth,
            'Accept': 'application/vnd.github.v3+json'
        })

    def get(self, gist_id):
        return requests.get("https://api.github.com/gists/" + gist_id, headers={
            'Authorization': self.auth,
            'Accept': 'application/vnd.github.v3+json'
        })

    def upsert_file(self, gist_id, file_name, file_content):
        return requests.patch("https://api.github.com/gists/" + gist_id, json={
            'files': {
                file_name: {
                    'content': file_content
                }
            }
        }, headers={
            'Authorization': self.auth,
            'Accept': 'application/vnd.github.v3+json'
        })

    def fetch_file(self, gist_id, file_id):
        return requests.get("https://gist.githubusercontent.com/raw/" + gist_id + "/" + file_id, headers={
            'Authorization': self.auth,
            'Accept': 'application/vnd.github.v3+json'
        })
