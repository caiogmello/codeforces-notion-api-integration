import requests
import datetime
from src.utilities.ExceptionHandler import ExceptionHandler


class CodeforcesAPI:
    def __init__(self) -> "CodeforcesAPI":
        """	
        Class to interact with the Codeforces API and get the submissions.
        """
        
        self._url = "https://codeforces.com/api/"

    def get_user_info(self, user: str) -> dict:
        """
        Get user information from Codeforces API.
        """

        url = f"{self._url}user.info?handles={user}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "FAILED":
            raise ExceptionHandler(data["comment"])

        return data

    def get_submissions(self, user: str, count=None, initial=None) -> dict:
        """
        Get user all submissions from Codeforces API, included the not accepted ones.
        Is possible to set the number of submissions to get and the initial submission to get.
        """

        paramaters = f"handle={user}"
        if count is not None:
            paramaters += f"&count={count}"
        if initial is not None:
            paramaters += f"&from={initial}"

        url = f"{self._url}user.status?{paramaters}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "FAILED":
            raise ExceptionHandler(data["comment"])

        return data

    def only_ok_submissions(self, submissions: dict) -> dict:
        """
        Get only the accepted submissions from all submissions.
        """

        return [sub for sub in submissions["result"] if sub["verdict"] == "OK"]

    def seconds_to_date(self, seconds: int) -> str:
        try:
            date_time = datetime.datetime.fromtimestamp(seconds)
            formatted_date = date_time.strftime("%d/%m/%Y %H:%M:%S")
            return formatted_date
        except:
            return None

    def format_submission(self, submission: dict) -> dict:
        """
        Format the submission to a dictionary with the following keys:
        - handle: the user handle
        - id: the submission id
        - contestId: the contest id
        - index: the problem index
        - name: the problem name
        - rating: the problem rating
        - tags: the problem tags
        - time: the submission time
        - url: the problem url
        """

        contest = "contest"
        if submission["contestId"] > 5000:
            contest = "gym"

        dct = {
            "handle": submission["author"]["members"][0]["handle"],
            "id": submission["id"],
            "contestId": submission["contestId"],
            "index": submission["problem"]["index"],
            "name": submission["problem"]["name"],
            "rating": None,
            "tags": submission["problem"]["tags"],
            "time": self.seconds_to_date(submission["creationTimeSeconds"]),
            "url": f"https://codeforces.com/{contest}/{submission['contestId']}/problem/{submission['problem']['index']}",
        }
        try:
            dct["rating"] = submission["problem"]["rating"]
        except:
            pass

        return dct

    def format_all_submissions(self, submissions: dict) -> list:
        return [
            self.format_submission(sub) for sub in self.only_ok_submissions(submissions)
        ]
