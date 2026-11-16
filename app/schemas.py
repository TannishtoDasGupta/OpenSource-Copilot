from pydantic import BaseModel, Field

class IssueTextRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    body: str = Field(default="", max_length=20000)

class GitHubIssueRequest(BaseModel):
    owner: str = Field(pattern=r"^[A-Za-z0-9-]{1,39}$")
    repo: str = Field(pattern=r"^[A-Za-z0-9_.-]{1,100}$")
    issue_number: int = Field(gt=0)

class PullRequestRequest(BaseModel):
    owner: str = Field(pattern=r"^[A-Za-z0-9-]{1,39}$")
    repo: str = Field(pattern=r"^[A-Za-z0-9_.-]{1,100}$")
    pull_number: int = Field(gt=0)
