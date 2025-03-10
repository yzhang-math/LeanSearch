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

"""Class for sampling new programs."""
from collections.abc import Collection, Sequence

#import llm
#import numpy as np
#import time

import evaluator
import programs_database
import logging
import time
#import asyncio

import os

class LLM:
  """Language model that predicts continuation of provided source code."""

  def __init__(self, samples_per_prompt: int, model, log_path=None, api_call_timeout=60, api_call_max_retries=10, ratelimit_backoff=30) -> None:
    self._samples_per_prompt = samples_per_prompt
    self.model = model
    self.prompt_count = 0
    self.log_path = log_path
    self.api_call_timeout = api_call_timeout
    self.api_call_max_retries = api_call_max_retries
    self.ratelimit_backoff = ratelimit_backoff
    self.theorem_declare = None
    self.theorem_insert = None

  async def _draw_sample(self, prompt: str, label: int) -> str:
    """Returns a predicted continuation of `prompt`."""
    #print("llm prompt:", prompt)
    start = time.time()
    response, usage_stats = await self.model.prompt(prompt,time_cutoff=self.api_call_timeout,ratelimit_backoff=self.ratelimit_backoff,max_retries=self.api_call_max_retries)
    end = time.time()
    usage_stats.prompt_count = self.prompt_count
    usage_stats.sampler_id = label
    usage_stats.time_to_response = end-start
    usage_stats.time_of_response = end
    if label is not None:
        #self._log(usage_stats, self.prompt_count, label)
        logging.debug("sample:%s:%d:%d:%d:%d:%.3f:%.3f:%.3f:%.3f"%(self.model.model,label,self.prompt_count,len(prompt),len(response),start,end,end-start,usage_stats.total_tokens))
    self.prompt_count += 1
    if response.strip() and self.theorem_declare not in response:
        #logging.info(f'Inserting statement block:{self.theorem_insert} in response')
        #print(response)
        response = insert_statement_block(response, self.theorem_insert)

    return response, usage_stats

  async def draw_samples(self, prompt: str, label: int) -> Collection[str]:
    """Returns multiple predicted continuations of `prompt`."""
    return [await self._draw_sample(prompt, label) for _ in range(self._samples_per_prompt)]

  # def _log(self, prompt: str, response: str, index: int, label: int):
  #   model_name_replaced = self.model.model.replace("/", "_")
  #   name_for_log = f"{model_name_replaced}_{label}_{index}.log"
  #   if self.log_path is not None:
  #     with open(self.log_path / name_for_log, "a") as f:
  #       f.write("=== PROMPT ===\n")
  #       f.write(prompt)
  #       f.write("\n=== RESPONSE ===\n")
  #       f.write(str(response))
  #       f.write("\n================\n")
  #       f.write(f"Total tokens: {usage_stats.total_tokens}\n")
  #       f.write(f"Prompt tokens: {usage_stats.tokens_prompt}\n")
  #       f.write(f"Completion tokens: {usage_stats.tokens_completion}\n")
  #       f.write(f"Model: {self.model.model}\n")


def insert_statement_block(text, statement_block):
    # Find the position of the first '--'
    end_comment_pos = text.rfind('-/')
    
    newline_pos = -1
    if end_comment_pos!= -1:
      newline_pos = text.find('\n', end_comment_pos, len(text))
    else:
      dash_pos = text.find('--')
      if dash_pos != -1:
        newline_pos = text.rfind('\n', 0, dash_pos)
        

    # Find the previous newline character
    
    
    if newline_pos == -1:
        # If no previous newline, insert at the beginning
        insertion_pos = 0
    else:
        # Insert after the previous newline
        insertion_pos = newline_pos + 1
    
    # Insert the statement at the insertion position
    modified_text = text[:insertion_pos] + statement_block + '\n' + text[insertion_pos:]
    
    #logging.info(f'modified text after inserting statement \n{modified_text}')
    return modified_text


class Sampler:
  """Node that samples program continuations and sends them for analysis."""

  def __init__(
      self,
      database: programs_database.ProgramsDatabase or multi_testing.AsyncProgramsDatabase, # # undefined name 'multi_testing'
      evaluators: Sequence[evaluator.Evaluator],
      model: LLM,
      label = 0,
  ) -> None:
    self._database = database
    self._evaluators = evaluators
    self._llm = model
    self.sampler_id = label
    self.api_responses = 0

  async def sample(self, prompt, eval_queue):
    """Continuously gets prompts, samples programs, sends them for analysis."""
    #prompt = await self._database.get_prompt()

    #logging.info(f'sampler {self.sampler_id} working')
    samples = await self._llm.draw_samples(prompt.code, self.sampler_id)
    # This loop can be executed in parallel on remote evaluator machines.
    self.api_responses += len(samples)
    
    for sample in samples:
      #chosen_evaluator = np.random.choice(self._evaluators)
      sample, usage_stats = sample
      usage_stats.island_id = prompt.island_id
      usage_stats.version_generated = prompt.version_generated
      usage_stats.island_version = prompt.island_version
      eval_queue.put((sample,  usage_stats))
      #chosen_evaluator.analyse(
      #    sample, prompt.island_id, prompt.version_generated, self.label)
    #logging.info(f'sampler {self.sampler_id} got {len(samples)} samples')

