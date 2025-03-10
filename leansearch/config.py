# Copyright 2023 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Configuration of a FunSearch experiment."""
import dataclasses

@dataclasses.dataclass(frozen=True)
class ProgramsDatabaseConfig:
  """Configuration of a ProgramsDatabase.

  Attributes:
    functions_per_prompt: Number of previous programs to include in prompts.
    num_islands: Number of islands to maintain as a diversity mechanism.
    reset_period: How often (in seconds) the weakest islands should be reset.
    cluster_sampling_temperature_init: Initial temperature for softmax sampling
        of clusters within an island.
    cluster_sampling_temperature_period: Period of linear decay of the cluster
        sampling temperature.
    backup_period: Number of iterations before backing up the program database on disk
    backup_folder: Path for automatic backups
  """
  functions_per_prompt: int = 2
  num_islands: int = 10  # Default value, can be overridden during initialization
  reset_period: int =  10 * 60 # Default value, can be overridden during initialization
  cluster_sampling_temperature_init: float = 0.3 # - note that scores are normalised to be between 0 and 1, where 0 is the lowest score and 1 is the highest score on the island.
  cluster_sampling_temperature_period: int = 30_000
  length_sample_temperature: float = 1.0
  backup_period: int = 300
  backup_folder: str = './data/backups'

  def __init__(self, **kwargs):
    # Use object.__setattr__ to set attributes on a frozen dataclass
    #object.__setattr__(self, 'num_islands', num_islands)
    # Set other attributes from kwargs
    for key, value in kwargs.items():
      if hasattr(self, key):
        object.__setattr__(self, key, value)


system_prompt = """
You will be given a theorem to prove, and you should replace the last faulty proof in the list

First, analyze the problem:
1. Analyze the theorem statement to understand what needs to be proven
2. Examine the <Lean4 feedback> to identify the specific issue in the current proof
3. Consider to rewrite the whole proof if needed

Then, give a formal proof in Lean 4:
1. Your response should be an implementation of the theorem <theorem_name>_vX (where X is the current iteration number).
2. namespace BigOperators Real Nat Topology

Remember: The proof you provide will be verified by Lean 4, so ensure it is complete and syntactically correct."""

@dataclasses.dataclass(frozen=True)
class Config:
  """Configuration of a FunSearch experiment.

  Attributes:
    programs_database: Configuration of the evolutionary algorithm.
    num_samplers: Number of independent Samplers in the experiment. A value
        larger than 1 only has an effect when the samplers are able to execute
        in parallel, e.g. on different matchines of a distributed system.
    num_evaluators: Number of independent program Evaluators in the experiment.
        A value larger than 1 is only expected to be useful when the Evaluators
        can execute in parallel as part of a distributed system.
    samples_per_prompt: How many independently sampled program continuations to
        obtain for each prompt.
    num_islands: Number of islands to maintain as a diversity mechanism.
    llm_temperature: Temperature for the LLM.
  """
  num_islands: int = 10
  programs_database: ProgramsDatabaseConfig = dataclasses.field(
      default_factory=ProgramsDatabaseConfig)
  num_samplers: int = 15
  num_evaluators: int = 10
  samples_per_prompt: int = 2
  num_batches =2 
  run_duration: int = 86400
  reset_period: int = 3600
  top_p: float = 0.95
  llm_temperature: float = 1.0
  logging_info_interval: int = 10
  system_prompt: str = system_prompt
  api_call_timeout: int = 120
  api_call_max_retries: int = 10
  ratelimit_backoff: int = 30
  token_limit: int = None  # Number of (equivalent) output tokens after which the search will be terminated
  relative_cost_of_input_tokens: float = None  # Cost ratio of input/output tokens (e.g. 0.5 means input tokens cost half)

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      if hasattr(self, key):
        object.__setattr__(self, key, value)
    object.__setattr__(self, 'programs_database', ProgramsDatabaseConfig(num_islands=self.num_islands, reset_period=self.reset_period))



