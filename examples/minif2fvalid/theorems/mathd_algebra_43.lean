--@funsearch.evolve
theorem mathd_algebra_43 (a b : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = a * x + b) (h₁ : f 7 = 4)
  (h₂ : f 6 = 3) : f 3 = 0 := by
  simp_all only
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
