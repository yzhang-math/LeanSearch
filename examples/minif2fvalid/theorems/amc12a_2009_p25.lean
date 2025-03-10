--@funsearch.evolve
theorem amc12a_2009_p25 (a : ℕ → ℝ) (h₀ : a 1 = 1) (h₁ : a 2 = 1 / Real.sqrt 3)
  (h₂ : ∀ n, 1 ≤ n → a (n + 2) = (a n + a (n + 1)) / (1 - a n * a (n + 1))) : abs (a 2009) = 0 := by
  sorry

-- Geometry probem that shouldn't be formalized like this.

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
