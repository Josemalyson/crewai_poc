import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, DirectorySearchTool
from dotenv import load_dotenv
from models.ProjectConfig import ProjectConfig

load_dotenv()

# esta configuração tem que ser realizada.
os.environ['OPENAI_API_KEY'] = ' '

MODEL = os.getenv('MODEL')
API_BASE = os.getenv('API_BASE')
PROVIDER = os.getenv('PROVIDER')
MODEL_BASE = os.getenv('MODEL_BASE')

llm = LLM(

    model=MODEL,
    base_url=API_BASE,
    # Para funcionar corretamente com o Ollama localmente é necessário habilitar o provider com o embedder
    embedder={
        "provider": PROVIDER,
        "config": {
            "model": "nomic-embed-text"
        }
    },
    max_tokens=1000,
    max_completion_tokens=1000
)


@CrewBase
class CrewaiPoc():
    """CrewaiPoc crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def senior_software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_software_architect'],
            llm=llm,
            tools=[
                DirectorySearchTool(config=dict(
                    llm=dict(
                        provider=PROVIDER,  # Options include ollama, google, anthropic, llama2, and more
                        config=dict(
                            model=MODEL_BASE,
                        ),
                    ),
                    embedder=dict(
                        provider="ollama",  # or openai, ollama, ...
                        config=dict(
                            model="nomic-embed-text",
                        ),
                    ),
                ))
            ],
            allow_delegation=False,
            verbose=True,
            memory=True,
            cache=True,
            max_tokens=1000,
            max_iter=1,
            max_rpm=1

        )

    @agent
    def project_documentation_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['project_documentation_writer'],
            llm=llm,
            tools=[
                FileReadTool(file_path="TEMPLATE.md",
                             config=dict(
                                 llm=dict(
                                     provider=PROVIDER,  # Options include ollama, google, anthropic, llama2, and more
                                     config=dict(
                                         model=MODEL_BASE,
                                     ),
                                 ),
                                 embedder=dict(
                                     provider=PROVIDER,  # or openai, ollama, ...
                                     config=dict(
                                         model="nomic-embed-text",
                                     ),
                                 ),
                             ))
            ],
            verbose=True,
            allow_delegation=False,
            memory=True,
            cache=True,
            max_tokens=500,
            max_iter=1,
            max_rpm=1
        )

    @agent
    def senior_specialist_software_backend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_specialist_software_backend'],
            llm=llm,
            tools=[
                DirectorySearchTool(
                    config=dict(
                        llm=dict(
                            provider=PROVIDER,
                            # Options include ollama, google, anthropic, llama2, and more
                            config=dict(
                                model=MODEL_BASE,
                            ),
                        ),
                        embedder=dict(
                            provider=PROVIDER,  # or openai, ollama, ...
                            config=dict(
                                model="nomic-embed-text",
                            ),
                        ),
                    ))
            ],
            verbose=True,
            allow_delegation=False,
            memory=True,
            cache=True,
            max_tokens=500,
            max_iter=1,
            max_rpm=1
        )

    @agent
    def senior_specialist_software_frontend(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_specialist_software_frontend'],
            llm=llm,
            tools=[
                DirectorySearchTool(
                    config=dict(
                        llm=dict(
                            provider=PROVIDER,  # Options include ollama, google, anthropic, llama2, and more
                            config=dict(
                                model=MODEL_BASE,
                            ),
                        ),
                        embedder=dict(
                            provider=PROVIDER,  # or openai, ollama, ...
                            config=dict(
                                model="nomic-embed-text",
                            ),
                        ),
                    ))
            ],
            verbose=True,
            allow_delegation=False,
            memory=True,
            cache=True,
            max_tokens=500,
            max_iter=1,
            max_rpm=1
        )

    @agent
    def senior_project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_project_manager'],
            llm=llm,
            tools=[
                DirectorySearchTool(
                    config=dict(
                        llm=dict(
                            provider=PROVIDER,  # Options include ollama, google, anthropic, llama2, and more
                            config=dict(
                                model=MODEL_BASE,
                            ),
                        ),
                        embedder=dict(
                            provider=PROVIDER,  # or openai, ollama, ...
                            config=dict(
                                model="nomic-embed-text",
                            ),
                        ),
                    ))
            ],
            verbose=True,
            allow_delegation=False,
            memory=True,
            cache=True,
            max_tokens=1000,
            max_iter=1,
            max_rpm=1
        )

    @task
    def architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_task'],
            output_json=ProjectConfig
        )

    @task
    def analyzer_code_backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyzer_code_backend_task'],
            output_json=ProjectConfig,
            context=[self.architecture_task()]
        )

    @task
    def analyzer_code_frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyzer_code_frontend_task'],
            output_json=ProjectConfig,
            context=[self.architecture_task(), self.analyzer_code_backend_task()]
        )

    @task
    def write_document_business(self) -> Task:
        return Task(
            config=self.tasks_config['write_document_business'],
            output_file='rules_business.md',
            context=[self.architecture_task(), self.analyzer_code_backend_task(), self.analyzer_code_frontend_task(), ],
        )

    @task
    def writer_md(self) -> Task:
        return Task(
            config=self.tasks_config['writer_md'],
            context=[self.architecture_task(), self.analyzer_code_backend_task(), self.analyzer_code_frontend_task(),
                     self.write_document_business()],
            output_file='report.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiPoc crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_agent=None,
            # Para funcionar corretametne com os modelos Ollama é necessário adiconar
            embedder={
                "provider": PROVIDER,
                "config": {
                    "model": "nomic-embed-text"
                }
            },
            memory=True,
            cache=True,
            max_rpm=1
        )
