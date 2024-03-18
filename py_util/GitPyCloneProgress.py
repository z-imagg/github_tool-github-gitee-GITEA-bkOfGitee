import git

from rich.progress import Progress,TaskID

class GitPyCloneProgressC(git.remote.RemoteProgress):
    def __init__(self,prgrsNm:str,prgrs:Progress):
        super().__init__()
        #进度条标题
        self.prgrsNm:str=prgrsNm
        self.task_id:TaskID=None
        self.prgrs:Progress = prgrs

    def update(self, op_code, cur_count, max_count=None, message=''):
        if self.task_id is None:
            self.task_id=self.prgrs.add_task(description=self.prgrsNm, total=max_count)
        self.prgrs.update(self.task_id, advance=cur_count)


          
# repo = git.Repo.clone_from(url="git@gitee/xx/xx.git", to_path="xx/xx/xx", progress=GitPyCloneProgressC())
