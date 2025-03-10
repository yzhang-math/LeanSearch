--@funsearch.evolve
theorem amc12a_2021_p8
  (d : ℕ → ℕ)
  (h₀ : d 0 = 0)
  (h₁ : d 1 = 0)
  (h₂ : d 2 = 1)
  (h₃ : ∀ n≥3, d n = d (n - 1) + d (n - 3)) :
  Even (d 2021) ∧ Odd (d 2022) ∧ Even (d 2023) := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
