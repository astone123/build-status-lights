class BitbucketWebhookData():
    def __init__(self, data, config):
        self.repo_url = self.get_attribute_from_path(data, ['repository', 'links', 'html', 'href'])
        self.branch_name = self.get_attribute_from_path(data, ['commit_status', 'refname'])
        self.build_status = self.get_attribute_from_path(data, ['commit_status', 'state'])
        self.is_valid_repo_url = any(project.get('repo_url', '') == self.repo_url for project in config.projects)
        self.is_valid_branch = any(project.get('branch', '') == self.branch_name for project in config.projects)

    def get_attribute_from_path(self, data, path_array):
        value = None
        for elem in path_array: 
            try:
                if value == None:
                    value = data[elem]
                else:
                    value = value[elem]
            except KeyError:
                return None
        return value
