# Mi Primer Crew — Tutorial Fase 0-1 con CrewAI

Este es un ejemplo **didactico y minimo** para aprender los fundamentos de
[CrewAI](https://crewai.com). Construimos un equipo (crew) de dos agentes que,
a partir de un tema (`topic`), investigan y redactan un resumen en espaniol.

El objetivo es que entiendas los conceptos base y el flujo de datos, no crear
algo complejo. No usa herramientas externas (buscadores web, etc.), asi que
solo necesitas una clave de un modelo de lenguaje (LLM) para ejecutarlo.

---

## 1. Que es CrewAI y sus conceptos base

CrewAI es un framework de Python para orquestar **agentes de IA** que colaboran
entre si para resolver tareas. Sus cuatro piezas fundamentales son:

- **Agent (Agente):** un "trabajador" impulsado por un LLM. Tiene un `role`
  (rol/especialidad), un `goal` (objetivo) y un `backstory` (personalidad y
  experiencia que guian su comportamiento). En este ejemplo tenemos un
  `investigador` y un `redactor`.

- **Task (Tarea):** una unidad de trabajo concreta que se le asigna a un agente.
  Define una `description` (que hacer) y un `expected_output` (como debe lucir el
  resultado). Aqui tenemos `tarea_investigacion` y `tarea_redaccion`.

- **Crew (Equipo):** el conjunto de agentes y tareas trabajando juntos. El crew
  coordina quien hace que y en que orden, y produce el resultado final.

- **Process (Proceso):** la estrategia de ejecucion del crew. En este ejemplo
  usamos `sequential` (secuencial): las tareas se ejecutan una tras otra y la
  salida de cada tarea queda disponible como contexto para la siguiente. Otra
  opcion es `hierarchical` (jerarquico), donde un agente "manager" coordina al
  resto.

---

## 2. Recorrido archivo por archivo

Estructura del proyecto:

```
mi_primer_crew/
├── .env.example                 # plantilla de variables de entorno (sin claves reales)
├── .gitignore                   # evita subir .env y archivos temporales
├── pyproject.toml               # dependencias y comandos del proyecto
├── README.md                    # este tutorial
└── src/
    └── mi_primer_crew/
        ├── __init__.py
        ├── main.py              # punto de entrada: define el input y arranca el crew
        ├── crew.py              # define agentes, tareas y el crew (decoradores)
        └── config/
            ├── agents.yaml      # descripcion de los agentes
            └── tasks.yaml       # descripcion de las tareas
```

### `config/agents.yaml`
Describe **quienes** son los agentes. Cada agente tiene `role`, `goal` y
`backstory`. La variable `{topic}` se sustituye en tiempo de ejecucion por el
valor que pasamos como input. Es "datos", no codigo: aqui no hay logica.

### `config/tasks.yaml`
Describe **que** hacen los agentes. Cada tarea tiene `description`,
`expected_output` y `agent` (que agente la ejecuta, referenciando la clave de
`agents.yaml`).

### `crew.py`
Es el **codigo** que conecta todo. Usa decoradores que enlazan con el YAML:

- `@CrewBase` marca la clase como un crew y carga los YAML de `config/`.
- `@agent def investigador(...)` lee la clave `investigador` de `agents.yaml`
  y crea un objeto `Agent`. Lo mismo para `redactor`.
- `@task def tarea_investigacion(...)` lee la clave `tarea_investigacion` de
  `tasks.yaml` y crea un objeto `Task`. La `tarea_redaccion` ademas recibe
  como `context` el resultado de la investigacion y escribe el resultado en
  `resumen.md` (`output_file`).
- `@crew def crew(...)` ensambla el equipo con `process=Process.sequential`.
  `self.agents` y `self.tasks` se rellenan automaticamente gracias a los
  decoradores.

En resumen: **el YAML dice el "que" y el "quien"; `crew.py` dice el "como" se
arma todo.**

### `main.py`
Es el **punto de entrada**. Define el diccionario `inputs` con el `topic`
(por defecto `"La inteligencia artificial en la medicina"`), y llama a
`MiPrimerCrew().crew().kickoff(inputs=inputs)` para arrancar la ejecucion.
Tambien incluye funciones auxiliares (`train`, `replay`, `test`).

### `pyproject.toml`
Declara las **dependencias** (`crewai[tools]`) y los **comandos** del proyecto
en `[project.scripts]`. Por ejemplo, `run_crew = "mi_primer_crew.main:run"`
permite que `crewai run` sepa que funcion ejecutar.

---

## 3. Configurar el `.env`

CrewAI necesita la clave de un LLM para funcionar. Copia la plantilla y
rellena tus valores reales:

```bash
cp .env.example .env
```

Edita `.env` y pon tu clave. Por ejemplo, para OpenAI:

```
OPENAI_API_KEY=sk-...tu-clave-real...
MODEL=gpt-4o-mini
```

> **Importante:** el archivo `.env` esta en `.gitignore`, asi que **nunca**
> se subira al repositorio. No compartas tus claves reales.

---

## 4. Instalar y ejecutar

Este proyecto usa [uv](https://docs.astral.sh/uv/) para gestionar dependencias.

Instala las dependencias (cualquiera de las dos opciones):

```bash
crewai install
# o, equivalentemente:
uv sync
```

Ejecuta el crew:

```bash
crewai run
```

### Flujo de datos

```
topic ("La inteligencia artificial en la medicina")
   |
   v
[investigador] -- tarea_investigacion --> lista de puntos clave
   |
   v  (context)
[redactor] -- tarea_redaccion --> resumen.md (informe final en markdown)
```

El `topic` entra por `main.py`, el `investigador` produce una lista de hallazgos,
esa lista se pasa como contexto al `redactor`, y el resultado final se escribe
en `resumen.md`.

---

## 5. Ejercicios propuestos

Para afianzar lo aprendido, intenta modificar el crew:

1. **Anadir un tercer agente revisor.** Crea un agente `revisor` en
   `agents.yaml` y una `tarea_revision` en `tasks.yaml` que reciba como
   contexto el resumen del redactor y corrija estilo/claridad. Registralo con
   `@agent`/`@task` en `crew.py`.

2. **Cambiar el proceso a jerarquico.** Cambia `process=Process.sequential` por
   `process=Process.hierarchical` en `crew.py` y define un
   `manager_llm`. Observa como cambia la coordinacion.

3. **Parametrizar el idioma de salida.** Anade un input `idioma` en `main.py` y
   usa `{idioma}` en `tasks.yaml` para que el informe se escriba en el idioma
   que indiques.

4. **(Avanzado) Anadir una herramienta de busqueda web.** Integra una tool como
   `SerperDevTool` para que el investigador busque en internet. Requiere una
   clave adicional (`SERPER_API_KEY`).

---

## Referencia rapida de comandos

```bash
cp .env.example .env        # crea tu .env y pon tu clave
crewai install              # instala dependencias (o: uv sync)
crewai run                  # ejecuta el crew -> genera resumen.md
```

Documentacion oficial: https://docs.crewai.com
