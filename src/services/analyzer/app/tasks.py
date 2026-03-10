from src.config.celery_app import celery_app
from src.config.container import container


@celery_app.task(name="analyze_file_task")
def analyze_file_task(input_path: str, output_path: str):
    use_case = container.generate_excel_report()
    use_case.execute(input_path, output_path)

    return {"status": "success", "output": output_path}
