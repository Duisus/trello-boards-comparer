import os

from jinja2 import Environment, FileSystemLoader

from classes.compare_result import CompareResult

__all__ = ["get_report"]


def _get_path_to_templates():
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, "../report_template")


ENV = Environment(loader=FileSystemLoader(_get_path_to_templates()))


def get_report(compare_result: CompareResult, mark: int) -> str:
    template = ENV.get_template("report-template.html.jinja")

    return template.render(compare_result=compare_result, mark=mark)
