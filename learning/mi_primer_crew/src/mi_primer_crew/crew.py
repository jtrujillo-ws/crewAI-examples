from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class MiPrimerCrew():
    """MiPrimerCrew: un crew didactico con dos agentes (investigador y redactor).

    Los decoradores @agent, @task y @crew conectan este codigo con los
    archivos YAML de la carpeta config/. Por ejemplo, @agent def investigador
    lee la clave 'investigador' de agents.yaml.
    """

    # Rutas a los archivos de configuracion YAML (relativas a este modulo).
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def investigador(self) -> Agent:
        return Agent(
            config=self.agents_config['investigador'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def redactor(self) -> Agent:
        return Agent(
            config=self.agents_config['redactor'],  # type: ignore[index]
            verbose=True,
        )

    @task
    def tarea_investigacion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_investigacion'],  # type: ignore[index]
        )

    @task
    def tarea_redaccion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_redaccion'],  # type: ignore[index]
            # El redactor recibe como contexto el resultado de la investigacion.
            context=[self.tarea_investigacion()],
            # El informe final se guarda en este archivo markdown.
            output_file='resumen.md',
        )

    @crew
    def crew(self) -> Crew:
        """Crea el crew de MiPrimerCrew con proceso secuencial."""
        return Crew(
            agents=self.agents,   # recopilados por el decorador @agent
            tasks=self.tasks,     # recopiladas por el decorador @task
            process=Process.sequential,
            verbose=True,
        )
