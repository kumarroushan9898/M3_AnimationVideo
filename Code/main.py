"""Discovery entry point for Manim's render CLI."""
import sys
from pathlib import Path

# Manim loads this file directly. Make its parent package importable from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Code.scene_01_hook import Hook as HookScene
from Code.scene_02_concept import Concept as ConceptScene
from Code.scene_03_basis_vectors import BasisVectors as BasisVectorsScene
from Code.scene_04_worked_example import WorkedExample as WorkedExampleScene
from Code.scene_05_interpretation import Interpretation as InterpretationScene
from Code.scene_06_summary import Summary as SummaryScene


class Hook(HookScene):
    pass


class Concept(ConceptScene):
    pass


class BasisVectors(BasisVectorsScene):
    pass


class WorkedExample(WorkedExampleScene):
    pass


class Interpretation(InterpretationScene):
    pass


class Summary(SummaryScene):
    pass
