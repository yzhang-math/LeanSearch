import logging
import time
import ast
import os
import pathlib
import sys
from typing import Any
import lean_dojo
import re

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

  def __init__(self, base_path: pathlib.Path, timeout_secs: int = 30, python_path: str = "python", id: int = 0, theorem_setup = ["Mathlib/Algebra/BigOperators/Pi.lean", "pi_eq_sum_univ"]):
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
    
    logging.info(f"Initializing sandbox {self.id} with theorem {theorem_setup}")
    self.repo = None
    self.theorem = None
    self.theorem_path = None
    self.theorem_name = None
    # self.repo = lean_dojo.LeanGitRepo(
    #   "https://github.com/leanprover-community/mathlib4",
    #   "29dcec074de168ac2bf835a77ef68bbe069194c5"
    #   )
    self.repo = lean_dojo.LeanGitRepo.from_path("/home/paul/Desktop/ML_experiments/lean4-example_1")
        #print(self.repo)
        #traced_repo = lean_dojo.trace(self.repo)
    #self.theorem_path = "Lean4Example.lean"
    self.theorem_path = theorem_setup[0]
    #self.theorem_name = "amc12a_2015_p10"
    self.theorem_name = theorem_setup[1]
    self.theorem = lean_dojo.Theorem(self.repo, self.theorem_path, self.theorem_name)
    
    #self.theorem_path = theorem_path
    #self.theorem_path = "miniF2F-lean4/MiniF2F/Valid.lean"
    #self.theorem_name = theorem_name
    #self.theorem_name = "amc12a_2015_p10"
    self.theorem = lean_dojo.Theorem(self.repo, self.theorem_path, self.theorem_name)
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
    score = 0

    if False:
      try:
        tactics = parse_lean_tactics(function_to_run)
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
    
    feedbackmsg = ''
    
    try:
      with lean_dojo.Dojo(entry=self.theorem, timeout=timeout_seconds) as (dojo, state):
        #logging.info(f"Sandbox: {self.id} Parsing tactics from proof:\n {function_to_run}")
        tactics = parse_lean_tactics(function_to_run)
        if not tactics:
          return -1, False, "No tactics to evaluate"
        
        #logging.info(f"Sandbox: {self.id} Evaluating Tactics: {tactics}")

        # Return 0, True, "Skip Lean Dojo"
        # Run each tactic
        ran_tactics = ''
        result = None
        succ_tac = 0
        for tactic in tactics:
            #logging.info(f"Sandbox: {self.id} Running tactic: \n{tactic}")
            ran_tactics += '\n' + tactic
            result = dojo.run_tac(state, tactic.strip())
            
            if isinstance(result, lean_dojo.LeanError):
                #logging.info(f"Sandbox: {self.id} Tactic error\n {result.error} at tactic {tactic}")

                return score, True, ran_tactics + f"\n\n<Lean4 feedback> last tactic error: \n{result.error} \n"
            elif isinstance(result, lean_dojo.ProofGivenUp):
                #logging.info(f"Sandbox: {self.id} Proof given up")
                return score, True, ran_tactics+"\n<Lean4 feedback> Proof contains sorry"
            elif isinstance(result, lean_dojo.ProofFinished):
                logging.info(f"Sandbox: {self.id} Proof completed")
                return 100, True, ran_tactics+"\n<Lean4 feedback> Proof completed"
            if "sorry" not in tactic and score < 9.2:
                score += 4/(1+succ_tac)
            state = result
            succ_tac += 1
            
        feedbackmsg = ran_tactics + "\n<Lean4 feedback> Proof unfinished without error\n" + result.pp
            
    except Exception as e:
      logging.error(f"Sandbox: {self.id} Error executing tactics {e}")
      retcode = 1

    if retcode != 0:
        self._save_diagnostics(program, call_data_folder)
        with open(error_file, "r") as f:
            outerr = f.read()
        logging.error(f"Sandbox: {self.id} Leandojo failed")
        return -1, False, None

    # Return score based on verification success
    return score, True, feedbackmsg  # Or some other scoring scheme

  @staticmethod
  def _save_diagnostics(program: str, output_path: pathlib.Path):
    filepath = output_path / "program.py"
    logging.debug(f"Writing program to {filepath}")
    with open(filepath, "w+") as f:
      f.write(program)

def validate_tactic(tactic: str) -> str:
    if not tactic:
      return None
    valid_tactics = ['sorry', 'rw', 'simp', 'intro', 'exact', 'apply', 'split', 'cases', 'induction', 'destruct', 'revert', 'have', 'ext', 'calc']
    invalid_words = ['begin', 'end', '{']
    cleaned_str = tactic.strip().replace('[', ' [')
    startingword = cleaned_str.split(' ')[0]
    if startingword in invalid_words:
       return tactic.split(startingword)[0]
    if "--" in tactic:
      return tactic.split('--')[0]
    else:
      return tactic

def parse_lean_tactics1(self, proof: str) -> list[str]:
    """Parse a Lean proof into individual tactics."""
    # Remove 'by' if present
    if proof.startswith('by'):
        proof = proof[2:].strip()
    logging.info(f"Parsing tactics from proof:\n {proof}")
    # Split into tactics (this is a simple split, might need to be more sophisticated)
    maybetactics = [t.strip() for t in proof.split('\n') if t.strip()]
    
    tactics = []
    for tactic in maybetactics:
      nexttactic = self._validate_tactic(tactic)
      if nexttactic:
        tactics.append(nexttactic)
    return tactics
  
def parse_lean_tactics(proof: str) -> list[str]:
    """Parse a Lean proof into individual tactics, handling multi-line indented blocks and removing comments."""
    # Remove 'by' if present
    # logging.info(f"Parsing tactics from proof:\n{proof}")
    if proof.startswith('by'):
        proof = proof[2:]

    # Remove multi-line comments /- ... -/ using regex
    cleaned_proof = re.sub(r'/\-[\s\S]*?\-/', '', proof)
    
    lines = cleaned_proof.split('\n')
    tactics = []
    current_tactic = ""
    current_indent = -1
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue  # Skip empty lines
        
        # Remove comments from the line
        if "--" in line:
            line = line.split("--")[0].rstrip()
            if not line.strip():
                continue  # Skip lines that were only comments

        
        # Calculate line's indentation level
        indent_level = len(line) - len(line.lstrip())
        first_char = line.lstrip()[0]

        if current_indent == -1:
           current_indent = indent_level

        if  indent_level > current_indent:
          validated_tactic = validate_tactic(line)
          if validated_tactic.strip():
             current_tactic += "\n" + validated_tactic
          # This is a continuation of the current tactic (indented block)
        elif indent_level == current_indent and first_char in '·|{':
          validated_tactic = validate_tactic(line)
          if validated_tactic.strip():
             current_tactic += "\n" + validated_tactic
          # continuation of case tactics
        else:
            # If we have a stored tactic, validate and save it first
            if current_tactic:
                # validated_tactic = validate_tactic(current_tactic.strip())
                # if validated_tactic:
                #     tactics.append(' '*indent_level + validated_tactic)
                tactics.append(current_tactic)
            
            # Start a new tactic
            validated_tactic = validate_tactic(line)
            if validated_tactic.strip():
              current_tactic = validated_tactic
              current_indent = indent_level

            
            

    
    # Don't forget to process the last tactic
    if current_tactic:
        validated_tactic = validate_tactic(current_tactic.strip())
        if validated_tactic:
            tactics.append(validated_tactic)
    if False and time.time() % 3 < 0.1:
        logging.info(f'Parsing proof: \n{proof}')
        logging.info(f"Parsed tactics:")
        for t in tactics:
            logging.info(f"  {t}")
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

