## Airflow example with Python and DockerOperator
This example shows you how to create a pipeline with Docker for  the different steps in your Python project.
The several steps in the pipeline are represented by different packages. 
In this example we are creating a very simple pipeline:
1. Download some data,
2. Preprocess that data,
3. Process data

To create a virtual environment and a wheel file from our Python project, we are using [`poetry`](https://python-poetry.org/docs/).
We have created a single Dockerfile that uses the docker-entrypoint shell script to distinguish between running the different Python packages.


Before starting up anything, you first have to build your project using: `poetry build`.
We have named our project `airflow-example`, so the wheel file created using the build command will be available in the `dist` directory and will be named `airflow_example-0.1.0-py3-none-any.whl`.
This is important because this way we can give this name as a build argument when creating the Docker image.

Next, we can build our Docker image:

`docker build --build-arg app_whl_file="airflow_example-0.1.0-py3-none-any.whl" -t airflow-example .`

Be sure to add the name of your newly created Docker image to your DockerOperator in the created Airflow DAG.

```python
download = DockerOperator(
        task_id='running_download',
        image='airflow-example:latest',
        api_version='auto',
        auto_remove=True,
        command="/docker-entrypoint.sh run-download",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        dag=dag
    )
```

Lastly, start up your airflow system using the `docker-compose.yml`.

Before you can use the Docker containers in your workflow, you need to change permissions on your mounted `/var/run/docker.sock`.

```bash
docker exec -it name-of-running-container bash
chmod 777 /var/run/docker.sock
```