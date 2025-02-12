import logging

import ast
import os
import pathlib
import sys
from typing import Any
import lean_dojo

import cloudpickle

CONTAINER_MAIN = (pathlib.Path(__file__).parent / "container" / "container_main.py").absolute()

IMAGE_NAME = "funsearch_sandbox"


class DummySandbox:
  """Base class for Sandboxes that execute the generated code.

  Note: this base class executes the code but does not offer any sandboxing!!!
  It should be only used in unit testing or debugging, and not with real LLM
  unless the host environment is in some kind of sandbox itself.
  Even in sandboxed host, the executed code could theoretically affect later executions.
  """

  sandboxes = 0

  def __init__(self, **kwargs):
    self.id = DummySandbox.sandboxes

    DummySandbox.sandboxes += 1

  def run(
          self,
          program: str,
          function_to_run: str,
          test_input,
          timeout_seconds: int,
  ) -> tuple[Any, bool,Any]:
    """Returns `function_to_run(test_input)` and whether execution succeeded."""

    # The same "program" seems to be now repeatedly parsed using AST and then compiled.
    # This could probably be simplified quite a bit.
    namespace = DummySandbox.compile_code(program)
    return namespace[function_to_run](test_input), True, None

  @staticmethod
  def compile_code(program: str):
    namespace = {}

    parsed_code = ast.parse(program)
    compiled_code = compile(parsed_code, filename="<ast>", mode="exec")
    exec(compiled_code, namespace)
    return namespace


class ExternalProcessSandbox(DummySandbox):
  """Sandbox that executes the code in a separate Python process in the same host.

  Note: This does not provide real safety and should be only used in an environment where the host process is
  in some kind of safe sandbox itself (i.e., a container).
  This kind of sandbox merely makes it more probable that single invalid call does not break the whole
  funsearch algorithm. It might be easier to set up and thus nice environment to tune the prompts and other code.
  """

  def __init__(self, base_path: pathlib.Path, timeout_secs: int = 30, python_path: str = "python", id: int = 0, theorem_path: str = "Mathlib/Algebra/BigOperators/Pi.lean", theorem_name: str = "pi_eq_sum_univ"):
    super(ExternalProcessSandbox, self).__init__()

    self.id = id
    self.output_path = pathlib.Path(base_path) / f"sandbox{self.id}"
    self.timeout_secs = timeout_secs
    self.python_path = python_path
    self.call_count = 0

    self.input_path = self.output_path / "inputs"
    for p in [self.output_path, self.input_path]:
      if not p.exists():
        p.mkdir(parents=True)
    
    logging.info(f"Initializing sandbox {self.id} with theorem {theorem_name} from {theorem_path}")
    self.repo = None
    self.theorem = None
    self.theorem_path = None
    self.theorem_name = None
    self.repo = lean_dojo.LeanGitRepo(
      "https://github.com/leanprover-community/mathlib4",
      "29dcec074de168ac2bf835a77ef68bbe069194c5"
      )
    self.theorem_path = theorem_path
    self.theorem_name = theorem_name
    self.theorem = lean_dojo.Theorem(self.repo, theorem_path, theorem_name)
    logging.info(f"Finished initializing sandbox {self.id}")

  def _exec(self, call_data_path: pathlib.Path, input_path: pathlib.Path, error_file_path: pathlib.Path):
    """Use podman/docker to execute python in a container.
    - The main.py shall execute the LLM generated method from prog.pickle file providing
      input.pickle as the input for the method.
    - main.py writes the output of the method into output.pickle.
    Everything except the /workspace folder will be read-only so that the environment remains good
    for future runs.
    """
    prog_path = call_data_path / "prog.pickle"
    output_file = call_data_path / "output.pickle"
    cmd = (f"{self.python_path} {CONTAINER_MAIN} {prog_path} {input_path} {output_file}"
           f"  2> {error_file_path}")
    logging.debug(f"Executing: {cmd}")
    return os.system(cmd)

  def run(
          self,
          program: str,
          function_to_run: str,
          test_input,
          timeout_seconds: int,
  ) -> tuple[Any, bool, any]:

    call_data_folder = (self.output_path / f"call{self.call_count}").absolute()
    if not call_data_folder.exists():
        call_data_folder.mkdir()

    # Instead of pickling, save Lean code directly
    prog_file = (call_data_folder / "prog.lean").absolute()
    with open(prog_file, "w+") as f:
        f.write(program)  # Save Lean code

    error_file = self.output_path / f"stderr_{self.call_count}.log"

    # Execute verification (this needs to be implemented in container_main.py)
    retcode = 0
    retcode = self._exec(call_data_folder, prog_file, error_file)
    self.call_count += 1

    retcode = 0

    if False:
      try:
        tactics = self._parse_lean_tactics(function_to_run)
        logging.info(f"Evaluating Tactics: {tactics}")

        return 0, True, "Skip Lean Dojo"
      except Exception as e:
        logging.error(f"Error executing theorem: {e}")
        retcode = 1


      if retcode != 0:
        self._save_diagnostics(program, call_data_folder)
        with open(error_file, "r") as f:
            outerr = f.read()
        return outerr, False

    # Return score based on verification success
      return 100, True, "Proof completed successfully"  # Or some other scoring scheme
    
    try:
      with lean_dojo.Dojo(entry=self.theorem, timeout=timeout_seconds) as (dojo, state):
        tactics = self._parse_lean_tactics(function_to_run)
        logging.info(f"Sandbox: {self.id} Evaluating Tactics: {tactics}")

        # Return 0, True, "Skip Lean Dojo"
        # Run each tactic
        for tactic in tactics:
            logging.info(f"Sandbox: {self.id} Running tactic: {tactic}")
            result = dojo.run_tac(state, tactic)
            if isinstance(result, lean_dojo.LeanError):
                logging.info(f"Sandbox: {self.id} Tactic error")
                return 1, True, f"Tactic error: {result.error}"
            elif isinstance(result, lean_dojo.ProofGivenUp):
                logging.info(f"Sandbox: {self.id} Proof given up")
                return 1, True, "Proof given up"
            elif isinstance(result, lean_dojo.ProofFinished):
                logging.info(f"Sandbox: {self.id} Proof completed")
                return 100, True, "Proof completed"
            state = result
    except Exception as e:
      logging.error(f"Sandbox: {self.id} Error executing tactics {e}")
      retcode = 1

    if retcode != 0:
        self._save_diagnostics(program, call_data_folder)
        with open(error_file, "r") as f:
            outerr = f.read()
        logging.error(f"Sandbox: {self.id} Leandojo failed")
        return outerr, False, None

    # Return score based on verification success
    return 10, True, "Unknown status"  # Or some other scoring scheme

  @staticmethod
  def _save_diagnostics(program: str, output_path: pathlib.Path):
    filepath = output_path / "program.py"
    logging.debug(f"Writing program to {filepath}")
    with open(filepath, "w+") as f:
      f.write(program)

  def _validate_tactic(self, tactic: str) -> str:
    if not tactic:
      return None
    valid_tactics = ['sorry', 'rw', 'simp', 'intro', 'exact', 'apply', 'split', 'cases', 'induction', 'destruct', 'revert', 'have', 'ext']
    cleaned_str = tactic.strip().replace('[', ' [')
    startingword = cleaned_str.split(' ')[0]
    if startingword not in valid_tactics:
      return None
    if "--" in tactic:
      return tactic.split('--')[0].strip()
    else:
      return tactic

  def _parse_lean_tactics(self, proof: str) -> list[str]:
    """Parse a Lean proof into individual tactics."""
    # Remove 'by' if present
    if proof.startswith('by'):
        proof = proof[2:].strip()
    logging.info(f"Parsing tactics from proof: {proof}")
    # Split into tactics (this is a simple split, might need to be more sophisticated)
    maybetactics = [t.strip() for t in proof.split('\n') if t.strip()]
    
    tactics = []
    for tactic in maybetactics:
      nexttactic = self._validate_tactic(tactic)
      if nexttactic:
        tactics.append(nexttactic)
    return tactics

class ContainerSandbox(ExternalProcessSandbox):
  """Basic sandbox that runs unsafe code in Podman or Docker container.
  - the sandbox should be safe against inadvertent bad code by LLM but not against malicious attacks.
  - does not require any other dependencies on the host than Podman/Docker
  - does not support multithreading
  - might provide easier or more lightweight debugging experience than some other fancier sandbox environments
  """
  executable = "podman"
  image_built = False

  @classmethod
  def build_image(cls, extra_pip_packages):
    version = sys.version.split(" ")[0]
    ret = os.system("podman --version")
    if ret != 0:
      ret = os.system("docker --version")
      if ret != 0:
        raise Exception("Could not find Podman or Docker. Can not use ContainerSandbox.")
      else:
        cls.executable = "docker"

    dockerfile = pathlib.Path(__file__).parent / "container" / "Dockerfile"
    logging.debug("Building container image")
    extra = ""
    if extra_pip_packages:
      extra = f"--build-arg INSTALL_PACKAGES=\"{extra_pip_packages}\""

    cmd = (f"{cls.executable} build --build-arg PYTHON_VERSION={version} {extra} "
           f"-t {IMAGE_NAME} -f {dockerfile} {CONTAINER_MAIN.parent}")
    logging.debug(f"Executing: {cmd}")
    os.system(cmd)
    cls.image_built = True

  def __init__(self, base_path: pathlib.Path, extra_pip_packages: str = "numpy", timeout_secs=30, id: int = 0):
    super(ContainerSandbox, self).__init__(base_path, timeout_secs)

    if not ContainerSandbox.image_built:
      ContainerSandbox.build_image(extra_pip_packages)

  def _exec(self, call_data_path: pathlib.Path, input_path: pathlib.Path, error_file_path: pathlib.Path):
    """Use podman/docker to execute python in a container.
    - The main.py shall execute the LLM generated method from prog.pickle file providing
      input.pickle as the input for the method.
    - main.py writes the output of the method into output_{id}.pickle.
    Everything except the /workspace folder will be read-only so that the environment remains good
    for future runs.
    """
    output_file = call_data_path / f"output_{self.id}.pickle"
    cmd = (f"{self.executable} run "
           f"--stop-timeout={self.timeout_secs} "
           f"-v {CONTAINER_MAIN}:/main.py:ro "
           f"-v {call_data_path}:/workspace "
           f"-v {input_path}:/input.pickle:ro "
           f"{IMAGE_NAME}:latest /usr/local/bin/python3 "
           f"/main.py /workspace/prog.pickle /input.pickle {output_file}"
           f" 2> {error_file_path}")
    logging.debug(f"Executing: {cmd}")
    return os.system(cmd)

