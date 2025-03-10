--@funsearch.evolve
theorem mathd_algebra_126 (x y : ℝ) (h₀ : 2 * 3 = x - 9) (h₁ : 2 * -5 = y + 1) : x = 15 ∧ y = -11 := by
  simp_all only [mul_neg]
  apply And.intro
  · linarith
  · linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
