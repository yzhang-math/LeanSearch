--@funsearch.evolve
theorem mathd_algebra_214 (a : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = a * (x - 2) ^ 2 + 3) (h₁ : f 4 = 4) :
  f 6 = 7 := by
  simp_all only [rpow_two]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
