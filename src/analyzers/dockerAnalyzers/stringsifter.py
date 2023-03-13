from analyzers.classes import DockerAnalyzer


class StringSifter(DockerAnalyzer):

    def build_image(self):
        return super().build_image()

    def run(self, optional_args: list):
        return super().run(optional_args)
