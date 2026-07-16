#!/usr/bin/env python
import sys
import warnings

from mi_primer_crew.crew import MiPrimerCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Tema por defecto que se pasa al crew. Cambialo para investigar otro asunto,
# o modifica esta variable para experimentar.
DEFAULT_TOPIC = "La inteligencia artificial en la medicina"


def run():
    """Ejecuta el crew con el tema por defecto."""
    inputs = {
        'topic': DEFAULT_TOPIC,
    }
    try:
        MiPrimerCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Ocurrio un error al ejecutar el crew: {e}")


def train():
    """Entrena el crew durante un numero de iteraciones."""
    inputs = {
        'topic': DEFAULT_TOPIC,
    }
    try:
        MiPrimerCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"Ocurrio un error al entrenar el crew: {e}")


def replay():
    """Reproduce la ejecucion del crew desde una tarea concreta."""
    try:
        MiPrimerCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Ocurrio un error al reproducir el crew: {e}")


def test():
    """Prueba la ejecucion del crew y devuelve los resultados."""
    inputs = {
        'topic': DEFAULT_TOPIC,
    }
    try:
        MiPrimerCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"Ocurrio un error al probar el crew: {e}")
